# -*- coding: utf-8 -*-
"""
Unit tests for the da.metabuild module.

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
class SpecifyMain:
    """
    Specify the da.metabuild.main() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The main() function is callable.

        """
        import da.metabuild
        assert callable(da.metabuild.main)


# =============================================================================
class SpecifyRunSubsidiaryBuild:
    """
    Specify the da.metabuild.run_subsidiary_build() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The run_subsidiary_build() function is callable.

        """
        import da.metabuild
        assert callable(da.metabuild.run_subsidiary_build)
