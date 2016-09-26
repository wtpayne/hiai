# -*- coding: utf-8 -*-
"""
Research specific CLI plugin.

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


import importlib
import os
import sys

import click

import da.lwc.discover
import da.util

# Expose "sim" command by adding "main" click.Group to module namespace.
dirpath_research = da.lwc.discover.path('research')
dirpath_sim      = os.path.join(dirpath_research, 't000_wtp')
sim              = da.util.import_from_dir(dirpath_sim, 'sim.cli').cli.main
