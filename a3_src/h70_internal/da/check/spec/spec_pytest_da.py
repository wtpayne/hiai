# -*- coding: utf-8 -*-
"""
Unit tests for the da.pytest_trace_cov module.

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
class SpecifyPytestAddoption:
    """
    Specify the da.check.pytest_da.pytest_addoption() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The pytest_addoption() function is callable.

        """
        import da.check.pytest_da
        assert callable(da.check.pytest_da.pytest_addoption)


# =============================================================================
class SpecifyPytestSessionstart:
    """
    Specify the da.check.pytest_da.pytest_sessionstart() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The pytest_sessionstart() function is callable.

        """
        import da.check.pytest_da
        assert callable(da.check.pytest_da.pytest_sessionstart)


# =============================================================================
class SpecifyPytestRuntestSetup:
    """
    Specify the da.check.pytest_da.pytest_runtest_setup() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The pytest_runtest_setup() function is callable.

        """
        import da.check.pytest_da
        assert callable(da.check.pytest_da.pytest_runtest_setup)


# =============================================================================
class SpecifyPytestRuntestTeardown:
    """
    Specify the da.check.pytest_da.pytest_runtest_teardown() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The pytest_runtest_teardown() function is callable.

        """
        import da.check.pytest_da
        assert callable(da.check.pytest_da.pytest_runtest_teardown)


# =============================================================================
class SpecifyPytestSessionfinish:
    """
    Specify the da.check.pytest_da.pytest_sessionfinish() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The pytest_sessionfinish() function is callable.

        """
        import da.check.pytest_da
        assert callable(da.check.pytest_da.pytest_sessionfinish)
