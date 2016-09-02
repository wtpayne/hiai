# -*- coding: utf-8 -*-
"""
Validation schema for common data elements.

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


import da.idclass
from good import (All,
                  Any,
                  Coerce,
                  Match,
                  Optional,
                  Required,
                  Schema,
                  Extra,
                  Reject)


TITLE_TEXT          = Schema(Match(r'[A-Z]{1}[\w,. -]{2,74}\.',
                             expected = 'Title text'))

SUMMARY_TEXT        = Schema(Match(r'[A-Z]{1}[\w,.\n -]{8,256}',
                             expected = 'Summary text'))

PARAGRAPH_TEXT      = Schema(Match(r'[A-Z]{1}[\w,.\n :;-]{8,1024}',
                             expected = 'Paragraph text'))

LOWERCASE_NAME      = Schema(Match(r'[a-z0-9_ ]',
                             expected = 'Lowercase underscore delimited name'))

LOWERCASE_PATH      = Schema(Match(r'[a-z0-9_/]',
                             expected = 'Lowercase file path'))

URL                 = Schema(Match(r'[A-Za-z0-9_/:]',
                             expected = 'URL'))

EMAIL_ADDRESS       = Schema(Match(
                        r'(^[A-Za-z0-9-+_.]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$)',
                             expected = 'Email address'))

GIT_COMMIT_ISH      = Schema(Match(r'[A-Za-z0-9_]',
                             expected = 'Git commit-ish'))

BUILD_RESTRICTION   = Schema([str])

LOG_LEVEL           = Schema(Any('CRITICAL',
                                 'ERROR',
                                 'WARNING',
                                 'INFO',
                                 'DEBUG'))

DATE_YYYYMMDD       = All(int,
                          Coerce(str),
                          Match(r'[0-9]{8}', expected = 'yyyymmdd'))


# -----------------------------------------------------------------------------
def idclass_schema(dirpath_lwc_root = None):
    """
    Return a table of idclass schemata.

    """
    return dict((name, Schema(Match(regex, expected = 'id: ' + name)))
        for (name, regex) in da.idclass.regex_table(dirpath_lwc_root).items())


# -----------------------------------------------------------------------------
def requirement_item_schema(idclass_tab):
    """
    Return the data specification schema for a requirement line-item.

    """
    item_id = idclass_tab['item']

    requirement_line_item = Schema([
        SUMMARY_TEXT,
        Optional({
            'notes':                    PARAGRAPH_TEXT,
            Extra:                      Reject
        }),
        Required({
            Required('type'):           Any('guidance',
                                            'mandate',
                                            'information'),
            Extra:                      Reject
        }),
        Required({
            Required('state'):          Any('draft'),
            Extra:                      Reject
        }),
        Optional({
            Required('ref'):            [item_id],
            Extra:                      Reject
        }),
        {
            Extra:                      Reject
        }
    ])

    return requirement_line_item


# -----------------------------------------------------------------------------
def requirement_set_schema(idclass_tab):
    """
    Return the data specification schema for a set of requirement line-items.

    """
    item_id         = idclass_tab['item']
    requirement_set = Schema({
        Required(item_id):  requirement_item_schema(idclass_tab)
    })

    return requirement_set
