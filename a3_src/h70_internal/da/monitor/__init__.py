# -*- coding: utf-8 -*-
"""
The da.monitor package is responsible for build progress monitoring.

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


import os
import os.path

import da
import da.constants
import da.lwc.run
import da.monitor.console_reporter
import da.monitor.html_reporter
import da.util


# =============================================================================
class BuildMonitor:
    """
    Class for build monitoring and error reporting.

    """

    # -------------------------------------------------------------------------
    def __init__(self, cfg):
        """
        Return an initialised instance of the BuildMonitor class.

        """
        dirpath_branch_log    = cfg['paths']['dirpath_branch_log']
        filepath_build_report = os.path.join(dirpath_branch_log, 'index.html')
        url_build_report      = 'file://{filepath}'.format(
                                            filepath = filepath_build_report)

        da.util.ensure_dir_exists(dirpath_branch_log)
        self.dirpath_branch_log    = dirpath_branch_log
        self.filepath_build_report = filepath_build_report
        self.url_build_report      = url_build_report
        self.cfg                   = cfg
        self.nonconformity_list    = []
        self.html_reporter         = da.monitor.html_reporter.coro(
                                                        filepath_build_report,
                                                        dirpath_branch_log)
        self.console_reporter      = da.monitor.console_reporter.coro(
                                                        cfg,
                                                        url_build_report)

    # -------------------------------------------------------------------------
    def report_progress(self, build_unit):
        """
        Method to handle build monitoring and progress reporting.

        """
        self.html_reporter.send(build_unit)
        self.console_reporter.send(build_unit)

    # -------------------------------------------------------------------------
    # Pylint error R0913 (Too many arguments) has
    # been disabled. This function is called in
    # response to nonconformities that originate
    # from a wide range of tools and checkers;
    # which forces us to accomodate a large number
    # of different parameters. At the same time we
    # want each call to be no more verbose than
    # is absolutely necessary. We achieve this
    # design goal by using a number of optional
    # named parameters, which unfortunately takes
    # us over the upper limit imposed by the style
    # guide.
    #
    def report_nonconformity(                           # pylint: disable=R0913
                        self, tool, msg_id, msg, path, line = 1, col = 0):
        """
        Send a nonconformity data structure to the build monitor.

        This method is responsible for deciding how
        the build process should respond to errors,
        and enables us to configure either a fail-
        fast policy (the first error terminates the
        build) or a robust policy (Wait until either
        the end of the current build phase or the
        end of the entire build before failing).

        If the system has been configured with a
        fail-fast policy, then the first error will
        terminate the build. Otherwise, the errors
        are accumulated in a list until the appropriate
        time for them to be collectively processed.

        """
        # Translate isolation-dir paths back to their original locations.
        path = os.path.normpath(path).replace(
                                    self.cfg['paths']['dirpath_isolated_src'],
                                    self.cfg['paths']['dirpath_lwc_root'])

        if os.path.isdir(path):
            line = None
            col  = None

        elif os.path.isfile(path):
            line = line if line else 1
            if line == -1:
                with open(path) as hfile:
                    line = sum(1 for line_of_text in hfile)

        self.nonconformity_list.append({'tool':   tool,
                                        'msg_id': msg_id,
                                        'msg':    msg,
                                        'path':   path,
                                        'line':   line,
                                        'col':    col})
        if self.cfg['options']['errors_abort_immediately']:
            _log_and_abort(self.cfg, self.nonconformity_list)

    # -------------------------------------------------------------------------
    def notify_build_end(self):
        """
        Log accumulated errors and abort if any errors have been seen.

        """
        self.html_reporter.send(da.constants.BUILD_COMPLETED)
        self.console_reporter.send(da.constants.BUILD_COMPLETED)
        if self.nonconformity_list:
            _log_and_abort(self.cfg, self.nonconformity_list)


# -----------------------------------------------------------------------------
def _log_and_abort(cfg, nonconformity_list):
    """
    Log every nonconformity in the list and abort execution.

    """
    da.monitor.console_reporter.print_all_nonconformities(nonconformity_list)

    if os.path.isfile(nonconformity_list[0]['path']):
            da.lwc.run.subl(
                dirpath_lwc_root = cfg['paths']['dirpath_lwc_root'],
                filepath         = nonconformity_list[0]['path'],
                line_number      = nonconformity_list[0]['line'])
    raise da.exception.AbortSilently()
