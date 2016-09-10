# -*- coding: utf-8 -*-
"""
Module for iterating over html fragments.

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

# import copy

# -----------------------------------------------------------------------------
# def _iter_docx_runs(root):
#     """
#     """
#     pass
#     # for (text, style) in _walk(root):
#     # style = collections.defaultdict(int)
#     # for tag, text in _walk(root):
#     #     if tag is not None:
#     #         style[tag] += 1
#     #     else:

# -----------------------------------------------------------------------------
# def _walk(parent, stack = []):
#     """
#     """
#     stack.append(parent.tag)

#     if parent.text:
#         yield (parent.text, stack)

#     for child in parent:
#         for text, tag in _walk(child, stack):
#             yield text, tag

#     stack.pop()

#     if parent.tail:
#         yield parent.tail, stack

# -----------------------------------------------------------------------------
# def _iter_html_runs(html):
#     """
#     """
#     for text, tag in _iter_raw(html):
#         style.append(copy.copy(style[-1]))
#         style[-1][tag] = True
#         if text:
#             yield text, style

# -----------------------------------------------------------------------------
# def _iter_raw(html):

#     # yield text, tag
#     # root  = cElementTree.fromString(html)
#     # dedup = set()
#     # for element in root.iter():
#     #     if element in dedup:
#     #         continue
#     #     dedup.update([element])

#     #     if element.tag == 'p'
#     #         yield _paragraph(element)
#     #         dedup.update(element.iter())
