# -*- coding: utf-8 -*-
"""
Configuration Management System.

This module is responsible for the build and release
process whereby built artifacts are deployed to UAT
and PRD and/or archived for future reference.

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


import datetime
import logging
import os
import re
import shutil

import da
import da.bldcfg
import da.expiration
import da.util


# Archival strategy:
#   Release     16 years.
#   Year End     8 years.
#   Quarterly    4 years.
#   Timebox End  2 years.
#   Daily        2 months.
#   Default      2 days.
_DAYS_PER_YEAR       = 365
_DAYS_PER_MONTH      = 30
_EXP_RELEASE_BLD     = datetime.timedelta(days  = 16 * _DAYS_PER_YEAR)
_EXP_YEAR_END_BLD    = datetime.timedelta(days  = 8  * _DAYS_PER_YEAR)
_EXP_QUARTERLY_BLD   = datetime.timedelta(days  = 4  * _DAYS_PER_YEAR)
_EXP_TIMEBOX_END_BLD = datetime.timedelta(days  = 2  * _DAYS_PER_YEAR)
_EXP_DAILY_BLD       = datetime.timedelta(days  = 2  * _DAYS_PER_MONTH)
_EXP_RECORDED_BLD    = datetime.timedelta(days  = 2)
_EXP_DEFAULT         = datetime.timedelta(hours = 8)


# -----------------------------------------------------------------------------
def register(cfg):
    """
    Register build outputs with the local Configuration Management System.

    """
    build_id           = cfg['build_id']
    dirpath_branch_cms = cfg['paths']['dirpath_branch_cms']
    dirpath_build_cms  = os.path.join(dirpath_branch_cms, build_id)

    da.util.ensure_dir_exists(dirpath_build_cms)
    os.sync()

    # Archive results.
    archive_plan = {
        'index':  'copy',
        'log':    'copy',
        '1report': 'copy',
    }
    dirpath_branch_tmp = cfg['paths']['dirpath_branch_tmp']
    for name in sorted(os.listdir(dirpath_branch_tmp)):

        if name not in archive_plan:
            continue

        action = archive_plan[name]

        if action == 'copy':
            dirpath_src = os.path.join(dirpath_branch_tmp, name)
            dirpath_dst = os.path.join(dirpath_build_cms,  name)
            if os.path.isdir(dirpath_src):
                shutil.copytree(dirpath_src, dirpath_dst)
            else:
                shutil.copyfile(dirpath_src, dirpath_dst)

    # Set the expiration date on the CMS.
    build_time = cfg['timestamp']['datetime_utc']
    expiration = datetime.timedelta(
                    days = cfg['options']['cms_expiration_days'])

    da.expiration.set_expiration_date(
                    dirpath_build_cms    = dirpath_build_cms,
                    identifier           = 'cms',
                    current_time         = build_time,
                    timedelta_expiration = expiration)

    # Delete expired builds.
    if cfg['options']['enable_cms_delete_old_builds']:
        rootpath_cms = cfg['paths']['rootpath_cms']
        for dirpath_prev_build in _gen_all_previous_builds(rootpath_cms):
            if da.expiration.has_expired(
                                    dirpath_build_cms = dirpath_prev_build,
                                    time_now          = build_time):
                shutil.rmtree(dirpath_prev_build)


# -----------------------------------------------------------------------------
def _gen_all_previous_builds(rootpath_cms):
    """
    Yield basic information about all previous builds.

    """
    for dirpath_year in _gen_cms_path_year(rootpath_cms):
        logging.debug('CMS year: %s', dirpath_year)
        for dirpath_timebox in _gen_cms_path_timebox(dirpath_year):
            logging.debug('CMS timebox: %s', dirpath_timebox)
            for dirpath_bldcfg in _gen_cms_path_bldcfg(dirpath_timebox):
                logging.debug('CMS bldcfg: %s', dirpath_bldcfg)
                for dirpath_branch in _gen_cms_path_branch(dirpath_bldcfg):
                    logging.debug('CMS branch: %s', dirpath_branch)
                    for dirpath_build in _gen_cms_path_build(dirpath_branch):
                        logging.debug('CMS build: %s', dirpath_build)
                        yield dirpath_build


# -----------------------------------------------------------------------------
def _gen_cms_path_year(rootpath_cms):
    """
    Yield valid year "YYYY" folders in the CMS filesystem hierarchy.

    """
    regex_year = re.compile(r'^[0-9]{4}$')
    for name in sorted(os.listdir(rootpath_cms)):
        if name == '.gitignore':
            continue
        path = os.path.join(rootpath_cms, name)
        if not (os.path.isdir(path) and re.match(regex_year, name)):
            raise RuntimeError('Unexpected (year) folder in CMS: %s.', path)
        yield path


# -----------------------------------------------------------------------------
def _gen_cms_path_timebox(dirpath_year):
    """
    Yield valid time-box "YYMMA/B" folders in the CMS filesystem hierarchy.

    """
    regex_timebox = re.compile(r'^[0-9]{4}[A-B]{1}$')
    for name in sorted(os.listdir(dirpath_year)):
        path = os.path.join(dirpath_year, name)
        if not (os.path.isdir(path) and re.match(regex_timebox, name)):
            raise RuntimeError('Unexpected (timebox) folder in CMS: %s.', path)
        yield path


# -----------------------------------------------------------------------------
def _gen_cms_path_bldcfg(dirpath_timebox):
    """
    Yield valid build-config-id folders in the CMS filesystem hierarchy.

    """
    regex_bldcfg = re.compile(r'^[a-z0-9_]{2,64}$')
    for name in sorted(os.listdir(dirpath_timebox)):
        path = os.path.join(dirpath_timebox, name)
        if not (os.path.isdir(path) and re.match(regex_bldcfg, name)):
            raise RuntimeError('Unexpected (bldcfg) folder in CMS: %s.',
                                                                    repr(name))
        yield path


# -----------------------------------------------------------------------------
def _gen_cms_path_branch(dirpath_bldcfg):
    """
    Yield valid per-branch folders in the CMS filesystem hierarchy.

    """
    regex_branch = re.compile(r'^[a-z0-9_]{2,64}$')
    for name in sorted(os.listdir(dirpath_bldcfg)):
        path = os.path.join(dirpath_bldcfg, name)
        if not (os.path.isdir(path) and re.match(regex_branch, name)):
            raise RuntimeError('Unexpected (branch) folder in CMS: %s.', path)
        yield path


# -----------------------------------------------------------------------------
def _gen_cms_path_build(dirpath_branch):
    """
    Yield valid per-build folders in the CMS filesystem hierarchy.

    """
    regex_build = re.compile(
        r'^[0-9]{4}[AB]{1}\.[0-9]{2}\.[0-9]{4}\..*\.[a-f0-9]{8}$')
    for name in sorted(os.listdir(dirpath_branch)):
        path = os.path.join(dirpath_branch, name)
        if not (os.path.isdir(path) and re.match(regex_build, name)):
            raise RuntimeError('Unexpected (build) folder in CMS: %s.', path)
        yield path
