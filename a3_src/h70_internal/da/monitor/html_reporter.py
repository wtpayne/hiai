# -*- coding: utf-8 -*-
"""
The html_reporter module reports build progress to a static html file.

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


import os.path
import textwrap

import da.constants
import da.util


# -------------------------------------------------------------------------
@da.util.coroutine
def coro(filepath_build_report, dirpath_branch_log):
    """
    Coroutine for reporting build progress to a static html file.

    """
    with open(filepath_build_report, 'wt') as file:

        file.write(
            textwrap.dedent(
                """\
                <html>
                <head>
                </head>
                <body>
                """))
        file.flush()

        while True:
            build_unit = (yield)
            if build_unit == da.constants.BUILD_COMPLETED:
                break

            # HTML entry for each build unit...
            relpath      = build_unit['relpath']
            dirpath_doc  = os.path.join(dirpath_branch_log, relpath)
            filepath_doc = os.path.join(dirpath_doc, 'design.html')
            url_doc      = 'file://{filepath}'.format(
                                                filepath = filepath_doc)
            link         = '<a href="{url}">{name}</a>'.format(
                                                url  = url_doc,
                                                name = relpath)
            file.write(link + '<br>\n')
            file.flush()

        file.write('</body>\n')
        file.write('</html>\n')
        file.flush()

    _ = (yield)  # Prevent StopIteration from being raised.
