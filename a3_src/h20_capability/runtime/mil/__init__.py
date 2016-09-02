# -*- coding: utf-8 -*-
"""
Development Automation System Command Line Interface.

This module handles the Development Automation Command Line Interface. It
makes use of the click library (click.pocoo.org) for input parameter parsing
and command dispatch.

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
import os.path

import yaml


# -----------------------------------------------------------------------------
def main(cfg_name):
    """
    Main.

    """
    cfg = load_cfg(cfg_name, dirpath_cfg = os.path.dirname(__file__))
    return cfg


# -----------------------------------------------------------------------------
def load_cfg(cfg_name, dirpath_cfg):
    """
    Return the specified MIL configuration data.

    """
    filename_cfg = '{name}.milcfg.yaml'.format(name = cfg_name)
    filepath_cfg = os.path.join(dirpath_cfg, filename_cfg)
    if not os.path.isfile(filepath_cfg):
        raise RuntimeError(
                'No MIL config. found with name = "{name}" in {dir}'.format(
                                                        name = cfg_name,
                                                        dir  = dirpath_cfg))
    with open(filepath_cfg, 'r') as file_cfg:
        cfg = yaml.safe_load(file_cfg)
    return cfg
