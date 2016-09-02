# -*- coding: utf-8 -*-
"""
Module for api documentation generation.

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


import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(error_handler):
    """
    Build API documentation for each build element sent to this coroutine.

    """
    while True:

        build_element = (yield)
        filepath      = build_element['filepath']

        if not da.lwc.file.is_python_file(filepath):
            continue

        print('#' * 80)
        print(build_element)
        print('#' * 80)

        error_handler.send({
            'tool':   'docgen.api',
            'msg_id': 'A001',
            'msg':    'Not implemented yet',
            'file':   __file__,
            'line':   1,
            'col':    1,
            'doc':    'api documentation not yet implemented.'
        })
