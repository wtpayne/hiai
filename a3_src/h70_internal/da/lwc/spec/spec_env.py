# -*- coding: utf-8 -*-
"""
Unit tests for the da.env module.

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
class SpecifyApiPath:
    """
    Specify the da.lwc.env.api_path() function.

    """

    def it_is_callable(self):
        """
        The api_path() function is callable.

        """
        import da.lwc.env
        assert callable(da.lwc.env.api_path)


# =============================================================================
class SpecifyCliPath:
    """
    Specify the da.lwc.env.cli_path() function.

    """

    def it_is_callable(self):
        """
        The cli_path() function is callable.

        """
        import da.lwc.env
        assert callable(da.lwc.env.cli_path)


# =============================================================================
class SpecifyGuiPath:
    """
    Specify the da.lwc.env.gui_path() function.

    """

    def it_is_callable(self):
        """
        The gui_path() function is callable.

        """
        import da.lwc.env
        assert callable(da.lwc.env.gui_path)


# =============================================================================
class SpecifyDependenciesRegister:
    """
    Specify the da.lwc.env.dependencies_register() function.

    """

    def it_is_callable(self):
        """
        The dependencies_register() function is callable.

        """
        import da.lwc.env
        assert callable(da.lwc.env.dependencies_register)


# =============================================================================
class SpecifyPythonImportPath:
    """
    Specify the da.lwc.env.python_import_path() function.

    """

    def it_is_callable(self):
        """
        The python_import_path() function is callable.

        """
        import da.lwc.env
        assert callable(da.lwc.env.python_import_path)


# =============================================================================
class Specify_IfaceForCurrentPythonRt:
    """
    Specify the da.lwc.env._iface_for_current_python_rt() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_lib_python3(self):
        """
        When run in the (python3) test runner, it returns the lib_python3

        Assumes tests are running under python3.x

        """
        import da.lwc.env
        assert da.lwc.env._iface_for_current_python_rt() == 'lib_python3'
