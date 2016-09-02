# -*- coding: utf-8 -*-
"""
Commit message writing and reading.

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

import textwrap

import yaml

import da.util


# -----------------------------------------------------------------------------
def parse(message):
    """
    Return data parsed from the specified commit message.

    """
    commit_msg = {
        'work_summary':     None,
        'work_notes':       None,
        'work_start_time':  None,
        'job_id':           None,
        'job_description':  None,
        'counterparty_id':  None,
        'project_id':       None,
        'mandate':          []
    }
    encoded_data = yaml.safe_load(next(da.util.iter_yaml_docs(message), ''))
    if encoded_data is not None:
        commit_msg.update(encoded_data)
    return commit_msg


# -----------------------------------------------------------------------------
def compose(daybook_entry, work_start_time):
    """
    Return a new commit message composed using daybook_entry information.

    """
    # Work out the details of the current job:
    # counterparty; project and job identifier
    # information.
    work_summary = daybook_entry['work_summary']
    work_notes   = daybook_entry['work_notes']
    cntrpty_id   = daybook_entry['counterparty_id']
    project_id   = daybook_entry['project_id']
    job_id       = daybook_entry['job_id']
    (job_num, _) = job_id.split(sep = '_', maxsplit = 1)

    # Format the commit message as a YAML document
    # with some customised pretty-printing to make
    # it easier to read.
    #
    # The resulting text will still be valid YAML -
    # but we take extra care over line-wrapping and
    # paragraph indentation to make it look attractive
    # and legible in the git log output.
    #
    # The page width is limited to a rather restrictive
    # 60 characters so that commit messages can appear
    # without wrapping in the pop-up boxes used by
    # the github 'blame' tool.
    page_width   = 60
    indent_size  = 17
    para_width   = page_width - indent_size
    para_prefix  = ' ' * indent_size
    list_prefix  = ' ' * 2

    def _para(text):
        """
        Return a nicely indented YAML format text block.

        """
        return textwrap.indent(
                    text   = textwrap.fill(text = text, width = para_width),
                    prefix = para_prefix).lstrip()

    def _list(listdata):
        """
        Return a nicely indented YAML format list.

        """
        return textwrap.indent(
                    text   = yaml.dump(listdata, default_flow_style = False),
                    prefix = list_prefix)

    commit_msg = textwrap.dedent("""
    {job}|{work_summary_line}

    ---
    work_summary:    {work_summary}

    work_notes:      {work_notes}

    work_start_time: {work_start_time}

    job_id:          {job_id}

    job_description: {job_description}

    counterparty_id: {counterparty_id}
    project_id:      {project_id}
    mandate:
    {mandate_list}
    ...

    """).format(
            job               = job_num,
            work_summary_line = work_summary,
            work_summary      = _para(work_summary),
            work_notes        = _para(work_notes),
            work_start_time   = work_start_time,
            job_id            = _para(job_id),
            job_description   = _para(daybook_entry['job_description']),
            counterparty_id   = _para(cntrpty_id),
            project_id        = _para(project_id),
            mandate_list      = _list(daybook_entry['mandate']))

    return commit_msg
