# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for the bulk data catalog.

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

from good import (Extra,
                  Reject,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def get(idclass_schema_tab):
    """
    Return the data validation schema for the codeword register.

    """
    common         = da.check.schema.common

    return Schema({
        'title':                    common.TITLE_TEXT,
        'identification': {
            'counterparty':         idclass_schema_tab['counterparty'],
            'project_year':         common.YEAR_YYYY,
            'project':              idclass_schema_tab['project'],
            'timebox':              common.TIMEBOX
        },
        'catalog': [{
            'date':                 common.DATE_MMDD,
            'plat_cfg':             idclass_schema_tab['platform'],
            'rec_serial':           idclass_schema_tab['recording'],
            'streams': {
                idclass_schema_tab['stream']: {
                    'path':         common.LOWERCASE_PATH,
                    'utc_start':    common.TIME_HHMMSS,
                    'utc_end':      common.TIME_HHMMSS,
                    'bytes':        common.NUMERIC_STRING,
                    'sha256':       common.LOWERCASE_HEX
                }
            },
            'notes':                common.PARAGRAPH_TEXT,
            'tags': [
                                    common.LOWERCASE_NAME
            ]
        }],
        Extra:                      Reject
    })
