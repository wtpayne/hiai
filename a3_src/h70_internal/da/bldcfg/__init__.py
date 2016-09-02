# -*- coding: utf-8 -*-
"""
Build Configuration package.

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

from . import bldcfg


__all__ = ()

# Pylint rule C0103 (invalid-name) disabled by design decision.
# load_cfg and is_in_restricted_build are functions, not constants,
# so a compliant (all-caps) name would be misleading.
load_cfg               = bldcfg.load_cfg                # pylint: disable=C0103
is_in_restricted_build = bldcfg.is_in_restricted_build  # pylint: disable=C0103
DATEFMT_DATETIME_UTC   = bldcfg.DATEFMT_DATETIME_UTC
