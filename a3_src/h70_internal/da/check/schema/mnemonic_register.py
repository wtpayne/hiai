# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for the mnemonic register.

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
def get():
    """
    Return the data validation schema for the mnemonic register.

    """
    common            = da.check.schema.common
    return Schema({
        'title':        common.TITLE_TEXT,
        'introduction': common.PARAGRAPH_TEXT,
        'register':     [common.LOWERCASE_NAME],
        Extra:          Reject
    })
