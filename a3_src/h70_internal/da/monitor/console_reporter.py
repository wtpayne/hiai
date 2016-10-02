# -*- coding: utf-8 -*-
"""
The console_reporter module reports build progress to the console.

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


import contextlib
import datetime
import itertools
import os
import os.path

import click
import py

import da
import da.constants
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(cfg, url_build_report):
    """
    Coroutine for reporting build progress to the command line interface.

    """
    _print_cli_header(
        build_id         = cfg['build_id'],
        commit_summary   = cfg['defined_baseline']['commit_summary'],
        url_build_report = url_build_report)

    # For the progress bar to work fully, we
    # need an estimate of the total number of
    # build units that we will be processing
    # in the build.
    #
    # Build units are (in general) generated
    # lazily, so this information is not
    # readily available at the start of the
    # build.
    #
    # To generate an estimate for this figure,
    # we use a cache to store the number (count)
    # of build_units processed in previous builds,
    # indexed by build configuration id and branch
    # name, so we can retrieve the matching count
    # -- on the assumption that little of
    # significance has changed.
    #
    # It won't always be correct, but it should
    # not often be wrong by much. Good enough.
    #
    with _cache_context(
                dirpath_cache = cfg['paths']['rootpath_tmp'],
                branch_name   = cfg['safe_branch_name'],
                cfg_name      = cfg['cfg_name']) as cache:

        # TODO: Configure progressbar on/off;
        # TODO: Consider curses based UI.
        build_unit = (yield)
        iunit      = 0
        if build_unit != da.constants.BUILD_COMPLETED:
            with click.progressbar(
                    length         = cache['num_build_units'],
                    show_eta       = False,
                    show_percent   = False,
                    show_pos       = True,
                    item_show_func = lambda _: build_unit['relpath'].split(
                                                    os.sep, maxsplit = 1)[1],
                    label          = _pad_key('Progress:')) as progressbar:
                for iunit in itertools.count(0):
                    if build_unit == da.constants.BUILD_COMPLETED:
                        break
                    else:
                        progressbar.update(1)
                    build_unit = (yield)

        # Update the cache.
        cache['num_build_units'] = iunit

    _print_cli_footer(
        start_time = cfg['timestamp']['datetime_utc'],
        end_time   = datetime.datetime.utcnow())
    os.sync()

    _ = (yield)  # Prevent StopIteration from being raised.


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _cache_context(dirpath_cache, branch_name, cfg_name):
    """
    Yield build cache data as a context object, saving any changes upon exit.

    """
    filepath = os.path.join(dirpath_cache, 'build_monitor_cache.json')
    key      = '{branch_name}.{cfg_name}'.format(branch_name = branch_name,
                                                 cfg_name    = cfg_name)

    if os.path.isfile(filepath):
        cache = da.util.load(filepath)
    else:
        cache = dict()

    if key not in cache or 'num_build_units' not in cache[key]:
        cache[key] = { 'num_build_units': 130 }

    yield cache[key]

    da.util.save(filepath, cache)


# -----------------------------------------------------------------------------
def _print_cli_header(build_id, commit_summary, url_build_report):
    """
    Print a build-process header to the console.

    """
    click.clear()
    _msg('Build id:',    build_id)          # Identify the build
    _msg('Last commit:', commit_summary)    # Provide some human-scale context.
    _msg('Report:',      url_build_report)  # Link to more detailed info.


# -----------------------------------------------------------------------------
def _print_cli_footer(start_time, end_time):
    """
    Print a build-process footer to the console.

    """
    delta_secs = (end_time - start_time).total_seconds()
    _msg('Completed in:', '{secs:0.0f}s.'.format(secs = delta_secs))


# -----------------------------------------------------------------------------
def print_all_nonconformities(nonconformity_list):
    """
    Log every nonconformity in the list.

    TODO: LOG NONCONFORMITY IN A FILE SOMEWHERE

    """
    click.echo('')
    nonconformity_count = len(nonconformity_list)
    termwriter          = py.io.TerminalWriter()        # pylint: disable=E1101
    for (idx, nonconformity) in enumerate(nonconformity_list):
        termwriter.sep(
            '-', 'Nonconformity {idx} / {total}'.format(
                                                idx   = idx + 1,
                                                total = nonconformity_count))
        _print_one_nonconformity(nonconformity)
    termwriter.sep('-', 'End of nonconformity report')


# -----------------------------------------------------------------------------
def _print_one_nonconformity(nonconformity):
    """
    Log one nonconformity.

    """
    # message = ('{tool}:{msg_id}: {msg:40s} - {path}:{line}\n'.format(
    #     tool    = err['tool'],
    #     msg_id  = err['msg_id'],
    #     msg     = err['msg'],
    #     path    = filepath_mod,
    #     line    = err['line']))
    # click.secho(message, fg='blue')

    noncon_id   = '{tool}.{msg_id}'.format(
                                        tool   = nonconformity['tool'],
                                        msg_id = nonconformity['msg_id'])

    _blue_msg('Id:',   noncon_id)
    _blue_msg('Path:', nonconformity['path'])

    line = nonconformity['line']
    if line is not None:
        _blue_msg('Line:', line)

    click.secho(
            'Msg:\n\n{msg}\n'.format(msg = nonconformity['msg']), fg = 'blue')


# -----------------------------------------------------------------------------
def _msg(key, value = None):
    """
    Write a key: value pair to the console.

    """
    click.echo('{key}  {value}'.format(key   = _pad_key(key),
                                       value = value if value else ''))


# -----------------------------------------------------------------------------
def _blue_msg(key, value = None):
    """
    Write a key: value pair to the console in blue.

    """
    click.secho(
        '{key}  {value}'.format(key   = _pad_key(key),
                                value = value if value else ''), fg = 'blue')


# -----------------------------------------------------------------------------
def _pad_key(key):
    """
    Return a key string padded out to 14 characters.

    """
    return '{key:14s}'.format(key = key)
