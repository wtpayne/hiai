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

# import BeautifulSoup
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
def _text_excerpt(filepath, start_line, num_lines):
    """
    Return text excerpted from range of lines in a file.

    """
    end_line = start_line + (num_lines - 1)
    return '\n'.join(_load_lines(filepath)[start_line:end_line])


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
def _accordion_row(collapsed, expanded):
    uid = uuid.uuid1().hex
    return L.li / (
        L.label(for_ = uid) / (collapsed),
        L.input(type = 'checkbox', id   = uid),
        L.ol / (L.li / (child) for child in expanded))


# -----------------------------------------------------------------------------
def _html_excerpt(rootpath_src,
                  rootpath_doc,
                  relpath_file,
                  start_line,
                  num_lines):
    """
    Return collapsible HTML for an excerpted reference.

    """
    filepath_src = os.path.join(rootpath_src, relpath_file)
    filepath_doc = _html_design_docs(rootpath_doc, relpath_file)
    link_address = 'file:///{path}#{line:04.0f}'.format(
                                            path = filepath_doc,
                                            line = start_line)
    link_text    = '{path}:{line:04.0f}'.format(
                                            path = relpath_file,
                                            line = start_line)
    excerpt      = _format_excerpt(
                        'unknown',
                        _text_excerpt(filepath_src, start_line, num_lines))

    return _accordion_row(
                collapsed = L.a(href=link_address) / (link_text),
                expanded  = [excerpt])


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

    for line_of_json in data:
        for identifier, references in line_of_json.items():
            for relpath_file, line_numbers in references.items():
                for start_line, num_lines in line_numbers:
                    fragment = _html_excerpt(rootpath_src,
                                             rootpath_doc,
                                             relpath_file,
                                             start_line,
                                             num_lines)
                    return fragment

    # doc = L.html / (_accordion_row(
    #                     collapsed = ['collapsed'],
    #                     expanded  = ['one', 'two']))

    # L = lys.L
    # doc = L.html / (
    #     L.head(lang = 'en') / (
    #         L.meta(charset = 'utf-8')),
    #     L.body / (

    #               ))
    # return doc



# -----------------------------------------------------------------------------
def generate():
    """
    Generate HTML

    """
    print(_generate())


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
#     relfilepath_self  = __file__ if __file__ else sys.argv[0]
#     dirpath_self      = os.path.dirname(os.path.realpath(relfilepath_self))
#     dirpath_data      = os.path.join(dirpath_self, 'static', 'data')
#     filepath_data     = os.path.join(dirpath_data, 'job.line_index.jseq')
#     with open(filepath_data, 'rt') as file:
#         data = [json.loads(line) for line in file]

#     env   = jinja2.Environment(
#                     loader = jinja2.PackageLoader('static_html', 'templates'))
#     tpl   = env.get_template('trace.jinja2.html')
#     html  = tpl.render(data = data)

#     filepath_html = os.path.join(dirpath_self, 'index.html')
#     with open(filepath_html, 'wt') as file:
#         file.write(html)

