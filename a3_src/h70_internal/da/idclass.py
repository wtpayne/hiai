# -*- coding: utf-8 -*-
"""
Module for controlled item identifier handling.

This module contains functions to build regular expressions which may
be used to search for and validate the controlled item identifiers
which are listed in the idclass register.

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


import re

import da.register


# -----------------------------------------------------------------------------
def regex_table(dirpath_lwc_root):
    """
    Build table of regular expressions to detect controlled item identifiers.

    """
    register = da.register.load(register_name    = 'idclass',
                                dirpath_lwc_root = dirpath_lwc_root)
    tab = {}
    for (idclass, spec) in register.items():
        if 'expr' in spec:
            expr = spec['expr']
        else:
            expr = r"\b{pfx}[0-9]{{{dgt}}}_[a-z0-9_]{{2,100}}".format(
                                                            pfx = spec['pfix'],
                                                            dgt = spec['dgts'])
        tab[idclass] = expr
    tab = {key: re.compile(val) for key, val in tab.items()}
    return tab
