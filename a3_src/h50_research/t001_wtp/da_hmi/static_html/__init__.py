# -*- coding: utf-8 -*-
"""
Development automation user interface experiment using static html.

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


import functools
import uuid
import json
import os

import bs4
import lys


L = lys.L


# -----------------------------------------------------------------------------
@functools.lru_cache(maxsize = 16, typed = False)
def _load_lines(filepath):
    """
    Return the content of the specified text file as a tuple of lines

    Cached for performance.

    """
    with open(filepath, 'rt') as file:
        lines = tuple(line for line in file)
    return lines


# -----------------------------------------------------------------------------
def _format_excerpt(excerpt_type, excerpt_text):
    """
    Return an excerpt formatted as HTML.

    """
    # TODO: pygments syntax highlighting?
    return excerpt_text


# -----------------------------------------------------------------------------
def _html_design_docs(rootpath_doc, relpath_file):
    """
    Return the path to the HTML design documentation for the specified file.

    """
    reldir_file   = os.path.splitext(relpath_file)[0]
    filepath_docs = os.path.join(rootpath_doc, reldir_file, 'design.html')
    return filepath_docs


# -----------------------------------------------------------------------------
def _accordion_row(title, content):
    """
    Return HTML for a CSS-only collapsible accordion row.

    """
    uid = uuid.uuid1().hex
    return L.div(class_ = 'accordion') / (
            L.input(type   = 'checkbox',
                    class_ = 'accordion',
                    id     = uid),
            L.label(class_ = 'accordion',
                    for_   = uid) / (
                L.div(class_ = 'accordion_content') / (title, content)))


# -----------------------------------------------------------------------------
def _excerpt(rootpath_src,
             rootpath_doc,
             relpath_file,
             line,
             column):
    """
    Return the HTML for a single (collapsible) excerpt.

    """
    filepath_src = os.path.join(rootpath_src, relpath_file)
    filename_src = os.path.basename(filepath_src)
    filepath_doc = _html_design_docs(rootpath_doc, relpath_file)
    link_address = 'file:///{path}#{line:04.0f}'.format(
                                            path = filepath_doc,
                                            line = line)
    link_text    = '{name}:{line:04.0f}:{col:02.0f}'.format(
                                            name = filename_src,
                                            line = line,
                                            col  = column)

    start_line   = line - 1
    end_line     = line + 4
    list_lines   = _load_lines(filepath_src)[start_line:end_line]
    title        = L.a(href=link_address) / (link_text)
    content      = L.div / ((line, L.br) for line in list_lines)
    return _accordion_row(title, content)


# -----------------------------------------------------------------------------
def _excerpts_from_file(rootpath_src,
                        rootpath_doc,
                        relpath_file,
                        locations):
    """
    Return the HTML for all (collapsible) excerpts from a file.

    """
    filepath_doc = _html_design_docs(rootpath_doc, relpath_file)
    link_address = 'file:///{path}'.format(path = filepath_doc)
    link_text    = relpath_file
    title        = L.a(href=link_address) / (link_text)
    content      = list()
    for line, column in locations:
        content.append(
            _excerpt(rootpath_src,
                     rootpath_doc,
                     relpath_file,
                     line,
                     column))
    return _accordion_row(title, content)


# -----------------------------------------------------------------------------
def _excerpts_for_all_references_to_identifier(rootpath_src,
                                               rootpath_doc,
                                               identifier,
                                               references):
    """
    Return the HTML for all files with...

    """

    title   = identifier
    content = list()
    for relpath_file, locations in references.items():
        content.append(
            _excerpts_from_file(rootpath_src,
                                rootpath_doc,
                                relpath_file,
                                locations))
    return _accordion_row(title, content)


# -----------------------------------------------------------------------------
def _generate():
    """
    Generate HTML

    """
    rootpath_src = '/home/wtp/dev/hiai/b0_dev/'
    rootpath_doc = '/home/wtp/dev/hiai/b0_dev/a4_tmp/branch/build'

    relfilepath_self  = __file__ if __file__ else sys.argv[0]
    dirpath_self      = os.path.dirname(os.path.realpath(relfilepath_self))
    dirpath_data      = os.path.join(dirpath_self, 'static', 'data')
    filepath_data     = os.path.join(dirpath_data, 'job.line_index.jseq')
    with open(filepath_data, 'rt') as file:
        data = [json.loads(line) for line in file]

    content = list()
    for line_of_json in data:
        for identifier, references in line_of_json.items():
            content.append(
                _cross_references_for_identifier(rootpath_src,
                                                 rootpath_doc,
                                                 identifier,
                                                 references))

    doc = L.html / (
        L.head(lang = 'en') / (
            L.meta(charset = 'utf-8')),
            L.link(rel     = 'stylesheet',
                   href    = './static/css/trace.css'),
        L.body / (content))
    return doc



# -----------------------------------------------------------------------------
def generate():
    """
    Generate HTML

    """
    relfilepath_self = __file__ if __file__ else sys.argv[0]
    dirpath_self     = os.path.dirname(os.path.realpath(relfilepath_self))
    ugly_html        = str(_generate())
    pretty_html      = bs4.BeautifulSoup(ugly_html, 'html.parser').prettify()
    filepath_html    = os.path.join(dirpath_self, 'index.html')

    with open(filepath_html, 'wt') as file:
        file.write(pretty_html)
    print(filepath_html)


# {
#     "i00033_halt_the_build_immediately_a_failure_is_detected": {
#         "a3_src/h70_internal/da/doc/build.rspec.yaml": {
#             "(87, 4)": {
#                 "('i00033_halt_the_build_immediately_a_failure_is_detected',)": [
#                     [
#                         "The system SHOULD halt the build as soon as a failing test is detected.",
#                         {"notes":
#                             "We are required to minimise the time elapsed between the introduction of \
#                             a regression or other error and the developer responsible being made aware of it."},
#                         {"type": "guidance"},
#                         {"state": "draft"}]
#                     ]
#                 }}}}


# # -----------------------------------------------------------------------------
# def gen_references(data):
#     """
#     """
#     for filepath in data.keys():
#         yield {
#             'filepath': filepath,
#             'lines':    list(lines for lines in data[filepath])
#         }

# # -----------------------------------------------------------------------------
# def _gen_items(raw):
#     """
#     """
#     for item in raw:
#         for key in item.keys():
#             filepaths = list()
#             for filepath in item[key].keys():
#                 filepaths.append(filepath)

#             yield {
#                 '_id':       key,
#                 'filepaths': filepaths
#             }

# # -----------------------------------------------------------------------------
# def generate():
#     """
#     Generate HTML

#     """
#     dirpath_data      = os.path.join(dirpath_self, 'static', 'data')
#     filepath_data     = os.path.join(dirpath_data, 'job.line_index.jseq')
#     with open(filepath_data, 'rt') as file:
#         data = [json.loads(line) for line in file]

#     env   = jinja2.Environment(
#                     loader = jinja2.PackageLoader('static_html', 'templates'))
#     tpl   = env.get_template('trace.jinja2.html')
#     html  = tpl.render(data = data)


