# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.pytest module.

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
class SpecifyCoro:
    """
    Specify the da.check.pytest.coro() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_something(self):
        """
        The coro() function returns a value that is not None.

        """
        import da.check.pytest
        assert da.check.pytest.coro(None, None) is not None


# =============================================================================
class Specify_ReportUnitTestFailure:
    """
    Specify the da.check.pytest._report_unit_test_failure() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _report_unit_test_failure() function is callable.

        """
        import da.check.pytest
        assert callable(da.check.pytest._report_unit_test_failure)


# =============================================================================
class Specify_CheckStaticCoverage:
    """
    Specify the da.check.pytest._check_static_coverage() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _check_static_coverage() function is callable.

        """
        import da.check.pytest
        assert callable(da.check.pytest._check_static_coverage)
