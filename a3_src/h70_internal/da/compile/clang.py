# -*- coding: utf-8 -*-
"""
Module containing clang compiler support functions.

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


import da.check.constants
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(build_monitor):
    """
    Send errors to build_monitor if supplied files does not compile with clang.

    """
    while True:

        build_unit = (yield)
        filepath   = build_unit['filepath']

        if not da.lwc.file.is_cpp_file(filepath):
            continue

        build_monitor.report_nonconformity(
            tool   = 'da.compile.clang',
            msg_id = da.check.constants.CLANG_UNKNOWN_ERROR,
            msg    = 'Clang compilation not implemented yet',
            path   = filepath)
