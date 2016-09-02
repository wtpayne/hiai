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


import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(error_handler):
    """
    Send errors to error_handler if supplied files does not compile with clang.

    """
    while True:

        build_element = (yield)
        filepath      = build_element['filepath']

        if not da.lwc.file.is_cpp_file(filepath):
            continue

        error_handler.send({
            'tool':   'clang',
            'msg_id': 'C001',
            'msg':    'Not implemented yet',
            'file':   filepath,
            'line':   1,
            'col':    1,
            'doc':    'Clang compilation not yet implemented.'
        })
