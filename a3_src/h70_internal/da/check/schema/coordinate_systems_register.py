# -*- coding: utf-8 -*-
"""
Package containing data validation schema for the coordinate systems register.

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
def get(idclass_tab):
    """
    Return the data validation schema for the dependencies register.

    """
    common               = da.check.schema.common
    coordinate_system_id = idclass_tab['coordinate_system']

    return Schema({
        'title':                        common.TITLE_TEXT,

        'introduction':                 common.PARAGRAPH_TEXT,

        'register': {

            coordinate_system_id: {
                'name':                 common.SUMMARY_TEXT,
                'mnemonic':             common.LOWERCASE_NAME,
                'description':          common.PARAGRAPH_TEXT,
                'definition':           common.PARAGRAPH_TEXT
            }

        },
        Extra:                          Reject
    })
