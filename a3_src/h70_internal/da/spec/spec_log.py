# -*- coding: utf-8 -*-
"""
Unit tests for the da.log module.

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
class SpecifyTrace:
    """
    Specify the da.log.trace() function.

    """

    def it_is_callable(self):
        """
        The trace() function is callable.

        """
        import da.log
        assert callable(da.log.trace)


# =============================================================================
class SpecifyConfigure:
    """
    Specify the da.log.configure() function.

    """

    def it_is_callable(self):
        """
        The configure() function is callable.

        """
        import da.log
        assert callable(da.log.configure)
