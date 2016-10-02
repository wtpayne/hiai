# -*- coding: utf-8 -*-
"""
Module containing pycodestyle (pep8) checking coroutines.

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


import pycodestyle

import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(build_monitor):
    """
    Send errors to build_monitor if supplied files not compliant with pep8.

    """
    # Several whitespace related rules are relaxed
    # to permit the vertical alignment of operators
    # and operands on consecutive lines. This allows
    # us to visually group related statements and
    # to readily identify discrepanices.
    #
    ignore_list = [
        'E126',  # Allow semantically meaningful indentation.
        'E127',  # Allow semantically meaningful indentation.
        'E128',  # Allow semantically meaningful indentation.
        'E201',  # Allow vertically aligned parameters.
        'E202',  # Allow vertically aligned parameters.
        'E221',  # Allow vertically aligned sequence of assignment statements.
        'E241',  # Allow vertically aligned dictionary values.
        'E251',  # Allow vertically aligned keyword/parameter assignment.
        'E272',  # Allow vertically aligned if x in y statements.
        'W503'   # Allow operators on LHS as per math convention.
    ]

    # =========================================================================
    class ReportAdapter(pycodestyle.StandardReport):
        """
        Reporting Adapter class for pycodestyle (pep8) checks.

        """

        def get_file_results(self):
            """
            Redirect error messages to the build_monitor coroutine.

            """
            for (line, col, msg_id, msg, doc) in self._deferred_print:
                doc = '    ' + doc.strip()  # Fixup indentation
                build_monitor.report_nonconformity(
                    tool    = 'da.check.pycodestyle',
                    msg_id  = msg_id,
                    msg     = msg + '\n\n' + doc,
                    path    = filepath,
                    line    = line,
                    col     = col)

    style = pycodestyle.StyleGuide(quiet = False, ignore = ignore_list)
    style.init_report(reporter = ReportAdapter)  # Inject custom reporting.

    # Run main file-processing loop: recieve file
    # paths from outside the coroutine and send
    # them one at a time to the pep8 module.
    #
    while True:

        build_unit = (yield)
        filepath   = build_unit['filepath']

        # Ignore non-python design documents.
        if not da.lwc.file.is_python_file(filepath):
            continue

        # Ignore experimental design documents.
        if da.lwc.file.is_experimental(filepath):
            continue

        style.check_files((filepath,))
