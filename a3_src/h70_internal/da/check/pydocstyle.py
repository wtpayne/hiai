# -*- coding: utf-8 -*-
"""
Module containing PEP-257 checking coroutines.

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


import logging

import pydocstyle

import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(build_monitor):
    """
    Send errors to build_monitor if supplied files not compliant with pep257.

    """
    ignore_list = [

        'D200',  # Rule D200 (One-line docstring should
                 # fit on one line) has been disabled so
                 # a uniform formatting can be applid to
                 # docstrings irrespective of length.
                 # (I.e. triple-quoted docstrings with
                 # quotes on separate lines).

        'D203',  # Rule D203 (1 blank line required before
                 # class docstring) has been disabled
                 # because it contradicts with rule D211
                 # (No blank lines allowed before class
                 # docstring), and it was felt that a
                 # uniform format for both class and
                 # function docstrings was desirable.

        'D212'   # Rule D212 (Multi-line docstring summary
                 # should start at the first line) has been
                 # disabled so that we can put a pep263
                 # encoding marker above the docstring.
                 # Rule D213 (Multi-line docstring summary
                 # should start at the second line) has
                 # been left enabled.

    ]
    pydocstyle.log.setLevel(logging.INFO)
    checker = pydocstyle.PEP257Checker()
    while True:

        build_unit = (yield)
        filepath   = build_unit['filepath']

        # Ignore non-python design documents.
        if not da.lwc.file.is_python_file(filepath):
            continue

        # Ignore experimental design documents.
        if da.lwc.file.is_experimental(filepath):
            continue

        for error in checker.check_source(build_unit['content'], filepath):
            if error.code in ignore_list:
                continue

            message = '{short_desc}\n{explanation}'.format(
                                            short_desc  = error.short_desc,
                                            explanation = error.explanation)

            build_monitor.report_nonconformity(
                tool    = 'da.check.pydocstyle',
                msg_id  = error.code,
                msg     = message,
                path    = filepath,
                line    = error.line)
            #   doc     = error.explanation
            #   lines   = error.lines
            #   def     = error.definition
