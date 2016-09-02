# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for daybook logfiles.

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

from good import (All,
                  Extra,
                  Length,
                  Reject,
                  Required,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def job_descriptions(idclass_tab):
    """
    Return the daybook.job_description schema.

    """
    counterparty_id = idclass_tab['counterparty']
    item_id         = idclass_tab['item']
    job_id          = idclass_tab['job']
    project_id      = idclass_tab['project']

    return Schema({
        Required(job_id):   [
            da.check.schema.common.PARAGRAPH_TEXT,
            {
                'counterparty': counterparty_id,
                Extra:          Reject
            },
            {
                'project':      project_id,
                Extra:          Reject
            },
            {
                'mandate':      [item_id],
                Extra:          Reject
            }
        ],
        Extra:  Reject
    })


# -----------------------------------------------------------------------------
def job_comments(idclass_tab):
    """
    Return the daybook.job_description schema.

    """
    job_id = idclass_tab['job']

    return Schema({
        Required(job_id):
            All(list, Length(min = 2, max = 2),
                [da.check.schema.common.SUMMARY_TEXT,
                da.check.schema.common.PARAGRAPH_TEXT])
    })


# -----------------------------------------------------------------------------
def get(idclass_tab):
    """
    Return the daybook schema.

    """
    return Schema({
        Required('agenda'): job_descriptions(idclass_tab),
        Required('chronicle'): {
            Required(da.check.schema.common.DATE_YYYYMMDD): [
                job_comments(idclass_tab)
            ],
            Extra:  Reject
        },
        Extra:  Reject
    })
