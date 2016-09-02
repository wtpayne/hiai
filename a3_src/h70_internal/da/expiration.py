# -*- coding: utf-8 -*-
"""
Expiration date management module.

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
import os
import re

import da.util


_DIRNAME_EXPIRATION    = 'expiration'
_FILEEXT_EXPIRATION    = 'expiration_date'
_DATEFMT_EXPIRATION    = '%Y%m%d%H%M'
_REGEX_EXPIRATION_FILE = r'^[0-9]{12}\.[a-z_]{3,60}\.%s$' % _FILEEXT_EXPIRATION


# -----------------------------------------------------------------------------
def _filename(current_time, timedelta_expiration, identifier):
    """
    Return the expiration marker filename for the specified "current" datetime.

    """
    current_hour = datetime.datetime(
                                year   = current_time.year,
                                month  = current_time.month,
                                day    = current_time.day,
                                hour   = current_time.hour,
                                minute = 0,
                                second = 0,
                                tzinfo = current_time.tzinfo)
    datetime_expiration    = current_hour + timedelta_expiration
    sz_datetime_expiration = datetime_expiration.strftime(_DATEFMT_EXPIRATION)
    filename_expiration    = '{expiration}.{identifier}.{fileext}'.format(
                                expiration = sz_datetime_expiration,
                                identifier = identifier,
                                fileext    = _FILEEXT_EXPIRATION)
    return filename_expiration


# -----------------------------------------------------------------------------
def set_expiration_date(dirpath_build_cms,
                        identifier,
                        current_time,
                        timedelta_expiration):
    """
    Set the expiration date for the specified CMS entry.

    """
    # Make sure the expiration-dates directory exists.
    dirpath_expiration = os.path.join(dirpath_build_cms, _DIRNAME_EXPIRATION)
    da.util.ensure_dir_exists(dirpath_expiration)

    # Set the new expiration date.
    filename_expiration = _filename(
                                current_time, timedelta_expiration, identifier)
    filepath_expiration = os.path.join(dirpath_expiration, filename_expiration)
    with open(filepath_expiration, 'wb'):
        pass

    # Delete existing expiration dates with the same owner.
    for (path, _, file_id) in _iter_expiration_files(dirpath_expiration):

        is_same_file = (path == filepath_expiration)
        if is_same_file:
            continue

        # ID indicates who set the expiration - so they can reset too.
        is_same_id = (file_id == identifier)
        if is_same_id:
            os.remove(path)


# -----------------------------------------------------------------------------
def has_expired(dirpath_build_cms, time_now):
    """
    Return true if the specified build has expired and may be safely deleted.

    Builds which are no longer required by any test or archival process are
    deleted to reduce waste. Processes may indicate if they require a build
    to be kept alive for a time by setting an expiration date.

    A process is only deemed to have expired if all expiration dates which
    have been set are in the past.

    """
    for (_, expiration, _) in _iter_expiration_files(
                                            os.path.join(dirpath_build_cms,
                                                         _DIRNAME_EXPIRATION)):
        if (expiration is not None) and (expiration > time_now):
            return False
    return True


# -----------------------------------------------------------------------------
def _iter_expiration_files(dirpath_expiration):
    """
    Yield tuples with expiration data for all files in the specified directory.

    Expiration dates are set by creating files in a specified expiration
    directory in the configuration management system. This function iterates
    over all such files in the specified expiration directory, yielding a
    tuple for each expiration file found.

    The tuple contains (path, expiration_date, owner).

    """
    if not os.path.isdir(dirpath_expiration):
        return
    regex_expiration_file = re.compile(_REGEX_EXPIRATION_FILE)
    for name in os.listdir(dirpath_expiration):
        path = os.path.join(dirpath_expiration, name)
        if not (    os.path.isfile(path)
                and re.match(regex_expiration_file, name)):
            raise RuntimeError(
                   'Unexpected file found in expiration folder: %s.', path)
        (sz_file_expiration, file_owner, _) = name.split('.')
        file_expiration = datetime.datetime.strptime(
                                    sz_file_expiration, _DATEFMT_EXPIRATION)
        yield (path, file_expiration, file_owner)
