# -*- coding: utf-8 -*-
"""
Unit tests for the runtime.mil module.

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


# =============================================================================
class SpecifyMain:
    """
    Specify the runtime.mil.main() function.

    """

    # -------------------------------------------------------------------------
    def it_can_load_default_config(self):
        """
        The main() function can load the default config.

        """
        import runtime.mil
        assert runtime.mil.main('default') is not None


# =============================================================================
class SpecifyLoadCfg:
    """
    Specify the runtime.mil.load_cfg() function.

    """

    # -------------------------------------------------------------------------
    def it_can_load_default_config(self):
        """
        The load_cfg() function can load the default config.

        """
        import runtime.mil
        dirpath_cfg = os.path.dirname(os.path.dirname(__file__))
        cfg_data = runtime.mil.load_cfg('default', dirpath_cfg)
        assert cfg_data is not None
