# -*- coding: utf-8 -*-
"""
Item register functions.

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

import os

import da.lwc.discover
import da.memo


# -----------------------------------------------------------------------------
@da.memo.var
def load(register_name, dirpath_lwc_root = None):
    """
    Return data read from the specified register.

    """
    dirpath_registry  = da.lwc.discover.path(
                                        key              = 'registry',
                                        dirpath_lwc_root = dirpath_lwc_root)

    # Try to load YAML file
    filename_yaml = '{name}.register.yaml'.format(name = register_name)
    filepath_yaml = os.path.join(dirpath_registry, filename_yaml)
    if os.path.isfile(filepath_yaml):
        import yaml
        with open(filepath_yaml, 'r') as file:
            return yaml.safe_load(file)['register']

    # Try to load JSON file
    filename_json = '{name}.register.json'.format(name = register_name)
    filepath_json = os.path.join(dirpath_registry, filename_json)
    if os.path.isfile(filepath_json):
        import json
        with open(filepath_json, 'r') as file:
            return json.load(file)['register']

    raise RuntimeError('Could not find register: ' + register_name)
