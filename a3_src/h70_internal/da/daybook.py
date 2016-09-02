# -*- coding: utf-8 -*-
"""
Module for handling daybook files.

Team members maintain an electronic lab notebook called a 'daybook' within
which we keep notes describing our daily activities.

These daybooks are parsed by the build-system so that commit messages with
suitable traceability information may be composed automatically.

A number of daybook files are created for each 2-3 week long time-box period:
One file for each team member. Each of these daybook files are split into two
sections: An agenda listing the jobs scheduled for the current time-box period,
and a chronicle listing the activities which actually took place, day-by-day.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2016 High Integrity Artificial Intelligence Systems"

license:
    "Licensed under the Apache License, Version 2.0 (the License);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."
...
"""

import os

import da.check.schema.common
import da.check.schema.daybook_schema
import da.exception
import da.lwc.discover
import da.util


# -----------------------------------------------------------------------------
def load(iso_year_id, timebox_id, team_member_id, dirpath_lwc_root = None):
    """
    Load the daybook corresponding to the specified user & date.

    """
    rootpath_daybook = da.lwc.discover.path(
                                        key              = 'daybook',
                                        dirpath_lwc_root = dirpath_lwc_root)
    dirpath_daybook  = os.path.join(rootpath_daybook, iso_year_id, timebox_id)
    filename_daybook = '{id}.daybook.yaml'.format(id = team_member_id)
    filepath_daybook = os.path.join(dirpath_daybook, filename_daybook)

    # Load daybook file for current user and timebox-period
    da.util.ensure_file_exists(filepath_daybook)
    daybook = da.util.load(filepath_daybook)
    return (filepath_daybook, daybook)


# -----------------------------------------------------------------------------
def latest_entry(
            iso_year_id, timebox_id, date, team_member_id, dirpath_lwc_root):
    """
    Get the latest day-book entry for the specified user & date.

    """
    (filepath_daybook, daybook) = load(iso_year_id      = iso_year_id,
                                       timebox_id       = timebox_id,
                                       team_member_id   = team_member_id,
                                       dirpath_lwc_root = dirpath_lwc_root)

    def abort_fcn(message):
        """
        Return an AbortWithoutStackTrace pointing to the current daybook.

        """
        return da.exception.AbortWithoutStackTrace(
            message     = 'Issue relating to daybook: {pth}\n{msg}'.format(
                                                        pth = filepath_daybook,
                                                        msg = message),
            filepath    = filepath_daybook,
            line_number = -1)

    # Most likely error is that we don't have an entry for today.
    if daybook is None:
        raise abort_fcn(
                'Please create a daybook for the current timebox period.')

    # Validate the daybook
    idclass_tab    = da.check.schema.common.idclass_schema(dirpath_lwc_root)
    daybook_schema = da.check.schema.daybook_schema.get(idclass_tab)
    daybook        = daybook_schema(daybook)

    # Extract today's latest chronicle entry and add extra information
    # about the job that we cane get from the agenda.
    daybook_entry  = get_last_chronicle_entry(
                                    chronicle = daybook['chronicle'],
                                    date      = date,
                                    abort_fcn = abort_fcn)

    job_data      = get_job_from_agenda(
                                    job_id    = daybook_entry['job_id'],
                                    agenda    = daybook['agenda'],
                                    abort_fcn = abort_fcn)

    daybook_entry.update(job_data)
    return daybook_entry


# -----------------------------------------------------------------------------
def get_last_chronicle_entry(chronicle, date, abort_fcn):
    """
    Return the last chronicle entry on the specified date.

    """
    # Locate today's entries in the chronicle
    if date not in chronicle:
        raise abort_fcn(
                'Please create a chronicle entry for today\'s date.')
    todays_entry = chronicle[date]

    # Locate the current (latest) job that is being worked on today:
    num_jobs_today = len(todays_entry)
    if num_jobs_today == 0:
        raise abort_fcn(
                'Please update the chronicle with jobs being done today.')
    current_job = tuple(todays_entry[-1].items())

    # Get chronicle entry for the current job
    if len(current_job) != 1:
        raise abort_fcn(
                'A malformed job data structure was found in the chronicle.')
    (job_id, job_notes) = current_job[0]

    # Get work notes for the current job
    if len(job_notes) == 0:
        raise abort_fcn('Please chronicle work notes for the current job.')

    return {
        'job_id':       job_id,
        'work_summary': job_notes[0],
        'work_notes':   '\n\n'.join(job_notes[1:])
    }


# -----------------------------------------------------------------------------
def get_job_from_agenda(job_id, agenda, abort_fcn):
    """
    Return the specified job from the agenda.

    """
    # Look up details for the current job id in the agenda.
    if job_id not in agenda:
        raise abort_fcn(
                'Please add the current job ({id}) to the agenda.'.format(
                                                                id = job_id))
    job_data = {}
    for item in agenda[job_id]:

        if not isinstance(item, dict):
            job_data['job_description'] = item

        if 'counterparty' in item:
            job_data['counterparty_id'] = item['counterparty']

        if 'project' in item:
            job_data['project_id'] = item['project']

        if 'mandate' in item:
            job_data['mandate'] = item['mandate']

    # Make sure we have all the details that we need:
    if 'counterparty_id' not in job_data:
        raise abort_fcn(
            'In the agenda, please make a record of the counterparty against'
            ' whom to book job "{job}".'.format(job = job_id))

    if 'project_id' not in job_data:
        raise abort_fcn(
            'In the agenda, please make a record of the project against'
            ' which to book job "{job}".'.format(job = job_id))

    if 'mandate' not in job_data:
        raise abort_fcn(
            'In the agenda, please make a record of the mandate under'
            ' which the job "{job}" is being performed.'.format(job = job_id))

    return job_data
