# -*- coding: utf-8 -*-
"""
Unit tests for the da.dep module.

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


# =============================================================================
class SpecifyBuild:
    """
    Specify the da.dep.build() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The build() function is callable.

        """
        import da.dep
        assert callable(da.dep.build)


# =============================================================================
class Specify_GetVersion:
    """
    Specify the da.dep._get_version() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_the_policy_version_string(self):
        """
        When given a dict with a policy field, it returns the version string.

        """
        import da.dep
        assert da.dep._get_version({'policy': 'ver_foo'}) == 'foo'
