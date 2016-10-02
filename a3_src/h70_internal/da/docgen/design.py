# -*- coding: utf-8 -*-
"""
Module for design documentation generation.

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


import os.path

import pygments
import pygments.lexers
import pygments.formatters

import da.lwc
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(cfg):
    """
    Generate design docs for each build unit sent to this coroutine.

    """
    rootpath_log = cfg['paths']['dirpath_branch_log']
    while True:

        build_unit = (yield)
        filepath   = build_unit['filepath']

        if not da.lwc.file.is_python_file(filepath):
            continue

        (relpath_dir, filename) = os.path.split(build_unit['relpath'])
        dirpath_doc             = os.path.join(
                                            rootpath_log,
                                            relpath_dir,
                                            filename.replace('.', '_'))
        filepath_doc        = os.path.join(dirpath_doc, 'design.html')
        html                = _render(build_unit)
        da.util.ensure_dir_exists(dirpath_doc)
        with open(filepath_doc, 'wt') as file:
            file.write(html)


# -----------------------------------------------------------------------------
def _render(build_unit):
    """
    Generate HTML for the specified build unit.

    """
    filename  = os.path.basename(build_unit['filepath'])
    lexer     = pygments.lexers.get_lexer_for_filename(filename)
    formatter = pygments.formatters.HtmlFormatter()     # pylint: disable=E1101
    html      = pygments.highlight(
                    code      = build_unit['content'],
                    lexer     = lexer,
                    formatter = formatter)

    return html
