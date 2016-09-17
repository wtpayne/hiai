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
    Generate design docs for each build element sent to this coroutine.

    """
    while True:

        build_element = (yield)
        filepath      = build_element['filepath']

        if not da.lwc.file.is_python_file(filepath):
            continue

        html         = _render(build_element)

        dirpath_doc  = os.path.join(cfg['paths']['dirpath_branch_log'],
                                    build_element['relpath'])
        filepath_doc = os.path.join(dirpath_doc, 'design.html')
        da.util.ensure_dir_exists(dirpath_doc)
        with open(filepath_doc, 'wt') as file:
            file.write(html)


# -----------------------------------------------------------------------------
def _render(build_element):
    """
    Generate HTML for the specified build element.

    """
    filename  = os.path.basename(build_element['filepath'])
    lexer     = pygments.lexers.get_lexer_for_filename(filename)
    formatter = pygments.formatters.HtmlFormatter()     # pylint: disable=E1101
    html      = pygments.highlight(
                    code      = build_element['content'],
                    lexer     = lexer,
                    formatter = formatter)

    return html
