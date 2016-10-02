# -*- coding: utf-8 -*-
"""
Development Automation bulk data checking package.

---
type:
    python_package

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
import json
import logging
import os
import os.path
import re

import good
import ruamel.yaml

import da.check.schema.common
import da.check.schema.bulk_data_catalog
# import da.check.schema.bulk_data_label
import da.check.constants
import da.idclass
import da.util


# -----------------------------------------------------------------------------
def check_all(cfg, build_monitor):
    """
    Send errors to build_monitor if bulk data filenames fail compliance checks.

    This function is used to ensure consistency in
    bulk data storage.

    All files and directories in bulk data storage
    areas are checked compliance with a standardised
    naming scheme.

    This is intended to ensure consistency and
    facilitate automated data processing methods.

    In contrast with the file_format

    ---
    type: function

    args:
        cfg:            A mapping holding the build configuration.

        build_monitor:  A reference to the build monitoring and
                        progress reporting coroutine.
    ...

    """
    dirpath_src       = cfg['paths']['dirpath_isolated_src']
    dirpath_bulk_data = cfg['paths']['dirpath_bulk_data']
    idclass_regex_tab = da.idclass.regex_table(dirpath_src)
    _check_all_impl(
        dirpath           = dirpath_bulk_data,
        entry_level       = 'data_root',
        dirpath_lwc_root  = cfg['paths']['dirpath_isolated_src'],
        idclass_regex_tab = idclass_regex_tab,
        build_monitor     = build_monitor)
    return


# -----------------------------------------------------------------------------
def _check_all_impl(dirpath,
                    entry_level,
                    dirpath_lwc_root,
                    idclass_regex_tab,
                    build_monitor):
    """
    Send errors to build_monitor if bulk data filenames fail compliance checks.

    This function contains

    ---
    type: function

    args:

        dirpath:            The path to the root of the data storage area
                            that is to be checked.

        level:              The level at which the check is to be performed.

        dirpath_lwc_root:   The path to the root of the local working copy.

        idclass_regex_tab:  A mapping from idclass type ids to compiled
                            regular expression objects that match valid
                            instances of each idclass.

        build_monitor:      A reference to the build monitoring and
                            progress reporting coroutine.
    ...

    """
    data_catalog_filename_regex = (   idclass_regex_tab['timebox'].pattern
                                    + r'\.data_catalog.yaml$')

    data_label_filename_regex   = (   idclass_regex_tab['stream'].pattern
                                    + r'\.label\.jseq$')

    asf_video_filename_regex    = (   idclass_regex_tab['stream'].pattern
                                    + r'\.asf$')

    idclass_schema_tab          = da.check.schema.common.idclass_schema(
                                                            dirpath_lwc_root)

    # Define the processing graph.

    chk_label_file = _label_file_check(build_monitor, idclass_schema_tab)
    chk_asf_video  = _asf_video_check(build_monitor)

    chk_recording_dir       = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_RECORDING,
        valid_names         = {
            data_label_filename_regex:              [chk_label_file],
            asf_video_filename_regex:               [chk_asf_video]
        })

    chk_has_labels = _has_labels_check(build_monitor)

    chk_platform_dir        = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_PLATFORM,
        valid_names         = {
            idclass_regex_tab['recording']:         [chk_recording_dir,
                                                     chk_has_labels]
        })

    chk_mmdd_dir            = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_MMDD_DATE,
        valid_names         = {
            idclass_regex_tab['platform']:          [chk_platform_dir]
        })

    chk_data_catalog = _data_catalog_check(build_monitor, idclass_schema_tab)

    chk_timebox_dir         = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_TIMEBOX,
        valid_names         = {
            r'^[0-9]{4}$':                          [chk_mmdd_dir],
            data_catalog_filename_regex:            [chk_data_catalog],
        })

    chk_has_catalog = _has_catalog_check(build_monitor)

    chk_project_dir         = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_PROJECT,
        valid_names         = {
            r'^[0-9]{4}[AB]$':                      [chk_timebox_dir,
                                                     chk_has_catalog]
        })

    chk_year_dir            = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_YEAR,
        valid_names         = {
            idclass_regex_tab['project']:           [chk_project_dir]
        })

    chk_counterparty_dir    = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_COUNTERPARTY,
        valid_names         = {
            r'^[0-9]{4}$':                          [chk_year_dir]
        })

    chk_data_root_dir       = _generic_check(
        build_monitor       = build_monitor,
        msg_id              = da.check.constants.DATA_NAME_ERR_IN_DATA_ROOT,
        valid_names         = {
            r'^\.gitignore$':                       [None],
            idclass_regex_tab['counterparty']:      [chk_counterparty_dir]
        })

    # Select the entry point into the processing graph.
    if entry_level == 'data_root':
        chk_data_root_dir.send(dirpath)

    elif entry_level == 'counterparty':
        chk_counterparty_dir.send(dirpath)

    elif entry_level == 'year':
        chk_year_dir.send(dirpath)

    elif entry_level == 'project':
        chk_project_dir.send(dirpath)

    elif entry_level == 'timebox':
        chk_timebox_dir.send(dirpath)

    elif entry_level == 'mmdd':
        chk_mmdd_dir.send(dirpath)

    elif entry_level == 'platform':
        chk_platform_dir.send(dirpath)

    elif entry_level == 'recording':
        chk_recording_dir.send(dirpath)

    else:
        raise RuntimeError('Level not recognised.')

    return


# -----------------------------------------------------------------------------
@da.util.coroutine
def _generic_check(build_monitor, msg_id, valid_names):
    """
    Generic file and directory name checking coroutine.

    """
    valid_names = _ensure_compiled(valid_names)

    while True:
        (path) = (yield)

        logging.debug('Check path: %s', path)

        for name in os.listdir(path):

            # Does the current file/directory name
            # match any of the specified patterns?
            #
            match = _matches(name, valid_names)
            if not match:

                badpath = os.path.join(path, name)
                if os.path.isfile(badpath):
                    name_type = 'file'
                else:
                    name_type = 'directory'

                patterns = '\n'.join(key.pattern for key in valid_names.keys())

                msg      = ('Found a {type} called: "{name}"\n'
                            'While looking inside:  "{path}"\n'
                            'It does not match any accepted pattern:\n'
                            '{patterns}').format(type     = name_type,
                                                 name     = name,
                                                 path     = path,
                                                 patterns = patterns)

                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = msg_id,
                    msg    = msg,
                    path   = path,
                    line   = None,
                    col    = None)

            else:
                for subcheck in match:
                    if subcheck is not None:
                        subcheck.send(os.path.join(path, name))


# -----------------------------------------------------------------------------
def _matches(name, valid_names):
    """
    Return a list of matches for the specified name.

    """
    matches = []
    for key in valid_names.keys():
        if key.match(name):
            matches.extend(valid_names[key])
    return matches


# -----------------------------------------------------------------------------
def _ensure_compiled(valid_names):
    """
    Return valid_names dict, ensuring string keys compiled as regex objects.

    The valid_names variable is a dict where keys
    implement key.match(name), and where values
    are coroutines that recieve path objects (and
    yield nothing). These coroutine values are used
    to check any filesystem names that are matched
    by the corresponding keys.

    This function uses the re module to compile any
    string keys it encounters into _sre.SRE_Pattern
    regular expression objects.

    """
    compiled = {}
    for key in valid_names.keys():

        if isinstance(key, str):
            compiled[re.compile(key)] = valid_names[key]

        else:
            compiled[key] = valid_names[key]

    return compiled


# -----------------------------------------------------------------------------
@da.util.coroutine
def _has_labels_check(build_monitor):
    """
    Coroutine to ensure that label files are present.

    """
    while True:
        (path) = (yield)

        # Find all the stream_id for which we have data in this directory.
        stream_id_set = set()
        for name in os.listdir(path):
            stream_id = name.split('.')[0]
            stream_id_set.add(stream_id)

        # For each stream_id that we know about, check that we have labels.
        for stream_id in stream_id_set:
            filepath_label = os.path.join(path, stream_id + '.label.jseq')
            has_labels     = os.path.isfile(filepath_label)
            if not has_labels:
                msg = 'Could not find labels for stream: {stream_id}'.format(
                                                        stream_id = stream_id)
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FILE_LABELFILE_MISSING,
                    msg    = msg,
                    path   = path,
                    line   = None,
                    col    = None)


# -----------------------------------------------------------------------------
@da.util.coroutine
def _has_catalog_check(build_monitor):
    """
    Coroutine to ensure that a data catalog file is present.

    """
    while True:
        (path)           = (yield)
        path_parts       = path.split(os.sep)
        timebox          = path_parts[-1]
        filepath_catalog = os.path.join(path, timebox + '.data_catalog.yaml')
        has_catalog      = os.path.isfile(filepath_catalog)
        if not has_catalog:
            msg = 'Could not find catalog for timebox: {timebox}'.format(
                                                            timebox = timebox)
            build_monitor.report_nonconformity(
                tool   = 'da.check.bulk_data',
                msg_id = da.check.constants.DATA_FILE_CATALOG_MISSING,
                msg    = msg,
                path   = path,
                line   = None,
                col    = None)


# -----------------------------------------------------------------------------
@da.util.coroutine
def _data_catalog_check(build_monitor, idclass_schema_tab):
    """
    Data catalog checking coroutine.

    """
    schema = da.check.schema.bulk_data_catalog.get(idclass_schema_tab)
    while True:
        (filepath_catalog) = (yield)

        with open(filepath_catalog, 'rt') as file:

            # Validate data catalog serialisation format (YAML)
            try:
                catalog = ruamel.yaml.load(file, ruamel.yaml.RoundTripLoader)
            except ruamel.yaml.error.YAMLError as err:
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_YAML,
                    msg    = str(err),
                    path   = filepath_catalog,
                    line   = err.problem_mark.line,     # pylint: disable=E1101
                    col    = err.problem_mark.column)   # pylint: disable=E1101

            # Validate catalog data format using its' schema.
            try:
                schema(catalog)
            except (good.Invalid, good.MultipleInvalid) as err:
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_BAD_CATALOG_FORMAT,
                    msg    = str(err),
                    path   = filepath_catalog,
                    line   = 1,
                    col    = 0)

            # Validate catalog data content.
            path_parts = filepath_catalog.split(os.sep)
            timebox = catalog['identification']['timebox']
            if path_parts[-1] != timebox + '.data_catalog.yaml':
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_BAD_CATALOG_CONTENT,
                    msg    = ('Inconsistent identification details: '
                              'Timebox not consistent with filename.'),
                    path   = filepath_catalog,
                    line   = 1,
                    col    = 0)

            if path_parts[-2] != timebox:
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_BAD_CATALOG_CONTENT,
                    msg    = ('Inconsistent identification details: '
                              'Timebox not consistent with path.'),
                    path   = filepath_catalog,
                    line   = 1,
                    col    = 0)

            if path_parts[-3] != catalog['identification']['project']:
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_BAD_CATALOG_CONTENT,
                    msg    = ('Inconsistent identification details: '
                              'Project not consistent with path.'),
                    path   = filepath_catalog,
                    line   = 1,
                    col    = 0)

            if path_parts[-4] != catalog['identification']['project_year']:
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_BAD_CATALOG_CONTENT,
                    msg    = ('Inconsistent identification details: '
                              'Project year not consistent with path.'),
                    path   = filepath_catalog,
                    line   = 1,
                    col    = 0)

            if path_parts[-5] != catalog['identification']['counterparty']:
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_BAD_CATALOG_CONTENT,
                    msg    = ('Inconsistent identification details: '
                              'Counterparty not consistent with path.'),
                    path   = filepath_catalog,
                    line   = 1,
                    col    = 0)

            # Validate catalog entries
            set_dirpath_rec = set()
            for entry in catalog['catalog']:
                dirpath_rec = os.path.join(os.path.dirname(filepath_catalog),
                                           entry['date'],
                                           entry['plat_cfg'],
                                           entry['rec_serial'])
                _check_catalog_entry(
                        entry            = entry,
                        filepath_catalog = filepath_catalog,
                        dirpath_rec      = dirpath_rec,
                        build_monitor    = build_monitor)
                set_dirpath_rec.add(dirpath_rec)


# -----------------------------------------------------------------------------
def _check_catalog_entry(entry, filepath_catalog, dirpath_rec, build_monitor):
    """
    Function for checking individual data catalog entries.

    """
    if not os.path.isdir(dirpath_rec):

        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_NO_REC_DIR,
            msg    = (   'Could not find recording directory:\n'
                       + '    {path}\n'.format(path = dirpath_rec)
                       + 'That was referenced by the catalog entry:\n'
                       + json.dumps(entry, indent = 4)),
            path   = filepath_catalog,
            line   = entry.lc.line,
            col    = entry.lc.col)

    # Check date consistent with timebox

    for stream in entry['streams'].values():

        _check_stream_utc_times(
                        filepath_catalog = filepath_catalog,
                        stream           = stream,
                        entry            = entry,
                        build_monitor    = build_monitor)

        _check_stream_files(
                        filepath_catalog = filepath_catalog,
                        dirpath_rec      = dirpath_rec,
                        stream           = stream,
                        entry            = entry,
                        build_monitor    = build_monitor)

    # Check tags against tag registry.
    # for tag in tags:
        #
    # tags:
    #   - good_visibility
    #   - large_cargo
    #   - large_derrick
    #   - mild_obstruction
    #   - multiple_hazard
    #   - light_rain
    #   - small_sail


# -----------------------------------------------------------------------------
def _check_stream_utc_times(
                filepath_catalog, stream, entry, build_monitor):
    """
    Function for checking utc times for each data catalog entry stream.

    """
    rec_serial = entry['rec_serial']
    rec_hhmm   = rec_serial.split('_')[-1]

    # UTC start time value-in-range check.
    #
    utc_start = stream['utc_start']
    try:
        time_start = datetime.datetime.strptime(utc_start, '%H%M%S')
    except ValueError:
        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_BAD_UTC_START,
            msg    = 'Invalid utc_start time: {0}'.format(utc_start),
            path   = filepath_catalog,
            line   = stream.lc.line,
            col    = stream.lc.col)

    # UTC end time value-in-range check.
    #
    utc_end = stream['utc_end']
    try:
        time_end = datetime.datetime.strptime(utc_end, '%H%M%S')
    except ValueError:
        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_BAD_UTC_END,
            msg    = 'Invalid utc_end time: {0}'.format(utc_end),
            path   = filepath_catalog,
            line   = stream.lc.line,
            col    = stream.lc.col)

    # UTC start time consistency with the recording serial number.
    #
    if utc_start[0:4] != rec_hhmm:
        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_UTC_CONSISTENCY,
            msg    = (   'utc_start inconsistent with rec_serial:'
                       + 'rec_serial = {0}'.format(rec_serial)
                       + 'utc_start  = {0}'.format(utc_start)),
            path   = filepath_catalog,
            line   = stream.lc.line,
            col    = stream.lc.col)

    # Duration value-in-range check.
    #
    # TODO: HANDLE RECORDINGS THAT CROSS THE MIDNIGHT BOUNDARY.
    #
    duration = time_end - time_start
    if duration < datetime.timedelta(0):
        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_BAD_SIZE_BYTES,
            msg    = (   'utc_start > utc_end:\n'
                       + '    utc_start: {0}\n'.format(utc_start)
                       + '    utc_end:   {0}\n'.format(utc_end)),
            path   = filepath_catalog,
            line   = stream.lc.line,
            col    = stream.lc.col)


# -----------------------------------------------------------------------------
def _check_stream_files(
                filepath_catalog, dirpath_rec, stream, entry, build_monitor):
    """
    Function for checking the files for each data catalog entry stream.

    """
    # Filename check.
    #
    relpath_stream  = stream['path']
    filepath_stream = os.path.normpath(
                            os.path.join(dirpath_rec, relpath_stream))
    if not os.path.isfile(filepath_stream):
        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_NO_STREAM_FILE,
            msg    = (   'Could not find stream file:\n'
                       + '    {path}\n'.format(path = filepath_stream)
                       + 'That was referenced by the catalog entry:\n'
                       + json.dumps(entry, indent = 4)),
            path   = filepath_catalog,
            line   = stream.lc.line,
            col    = stream.lc.col)
        return

    # Data integrity check.
    #
    sha256_stream = da.util.sha256(filepath_stream)
    assert sha256_stream == stream['sha256']
    if sha256_stream != stream['sha256']:
        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_BAD_SHA256,
            msg    = (   'File and catalog checksums do not match:\n'
                       + '    Path:    {0}\n'.format(filepath_stream)
                       + '    File:    {0}\n'.format(sha256_stream)
                       + '    Catalog: {0}\n'.format(stream['sha256'])),
            path   = filepath_catalog,
            line   = stream.lc.line,
            col    = stream.lc.col)

    # Data size check.
    #
    file_size = str(os.stat(filepath_stream).st_size)
    if stream['bytes'] != file_size:
        build_monitor.report_nonconformity(
            tool   = 'da.check.bulk_data',
            msg_id = da.check.constants.DATA_CATALOG_BAD_SIZE_BYTES,
            msg    = (   'File and catalog file sizes do not match:\n'
                       + '    Path:    {0}\n'.format(filepath_stream)
                       + '    File:    {0}\n'.format(file_size)
                       + '    Catalog: {0}\n'.format(stream['bytes'])),
            path   = filepath_catalog,
            line   = stream.lc.line,
            col    = stream.lc.col)

    # TODO: Data size consistent with duration
    #       (Needs to be parameterised by platform configuration)


# -----------------------------------------------------------------------------
@da.util.coroutine
def _label_file_check(build_monitor, idclass_schema_tab):
    """
    Label file checking coroutine.

    """
    schema = da.check.schema.bulk_data_label.get(idclass_schema_tab)
    while True:

        (path) = (yield)

        with open(path, 'rt') as file:
            for (iline, line) in enumerate(file):

                # Validate label serialisation format (JSON)
                #
                try:
                    label = json.loads(line)
                except json.decoder.JSONDecodeError as err:
                    build_monitor.report_nonconformity(
                        tool   = 'da.check.bulk_data',
                        msg_id = da.check.constants.DATA_FMT_JSEQ,
                        msg    = str(err),
                        path   = path,
                        line   = iline,
                        col    = err.colno)
                    continue

                # Validate label data format using its' schema.
                #
                try:
                    schema(label)
                except (good.Invalid, good.MultipleInvalid) as err:
                    build_monitor.report_nonconformity(
                        tool   = 'da.check.bulk_data',
                        msg_id = da.check.constants.DATA_FMT_YAML,
                        msg    = str(err),
                        path   = path,
                        line   = iline,
                        col    = 0)
                    continue

                # TODO: Validate label data content.


# -----------------------------------------------------------------------------
@da.util.coroutine
def _asf_video_check(build_monitor):
    """
    ASF video checking coroutine.

    """
    while True:

        (path) = (yield)

        with open(path, 'rb') as file:
            header = file.read(4)
            if header != b'\x30\x26\xB2\x75':
                build_monitor.report_nonconformity(
                    tool   = 'da.check.bulk_data',
                    msg_id = da.check.constants.DATA_FMT_ASF,
                    msg    = 'ASF format error',
                    path   = path)

        # TODO: Calculate checksum and compare with checksum in catalog.

        # TODO: Read frames and check for frozen / blank / corrupt data.
