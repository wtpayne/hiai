# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for the identifier class register.

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
                  Required,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def get(idclass_tab):
    """
    Return the data specification schema for requiremnts specifications.

    """
    common  = da.check.schema.common
    item_id = idclass_tab['item']

    return Schema({
        Required('title'):  common.TITLE_TEXT,
        Required(item_id):  common.requirement_item_schema(idclass_tab),
        Extra:              Reject
    })
