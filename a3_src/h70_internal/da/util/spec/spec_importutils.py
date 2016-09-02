# -*- coding: utf-8 -*-
"""
Unit tests for the da.util.importutils module.

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
class SpecifyImportFcn:
    """
    Specify the da.util.importutils.import_fcn() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_callable(self):
        """
        When given a valid module.function string it returns a callable.

        """
        import da.util.importutils
        assert callable(da.util.importutils.import_fcn('sys.exit'))


# =============================================================================
class SpecifyImportModuleFile:
    """
    Specify the da.util.importutils.import_module_file() function.

    """

    def it_is_callable(self):
        """
        The import_module_file() function is callable.

        """
        import da.util.importutils
        assert callable(da.util.importutils.import_module_file)


# =============================================================================
class SpecifyImportFromDir:
    """
    Specify the da.util.importutils.import_from_dir() function.

    """

    def it_is_callable(self):
        """
        The import_from_dir() function is callable.

        """
        import da.util.importutils
        assert callable(da.util.importutils.import_from_dir)
