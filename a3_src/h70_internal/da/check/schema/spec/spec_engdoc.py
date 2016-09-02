# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.schema.engdoc module.

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
class SpecifyMetadata:
    """
    Specify the da.check.schema.engdoc.metadata() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_callable(self):
        """
        The get() function returns a callable.

        """
        import da.check.schema.engdoc
        schema = da.check.schema.engdoc.metadata()
        assert callable(schema)


# =============================================================================
class SpecifySectionContent:
    """
    Specify the da.check.schema.engdoc.section_content() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_callable(self):
        """
        The get() function returns a callable.

        """
        import da.check.schema.engdoc
        schema = da.check.schema.engdoc.section_content()
        assert callable(schema)


# =============================================================================
class SpecifyValidate:
    """
    Specify the da.check.schema.engdoc.validate() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The validate() function is callable.

        """
        import da.check.schema.engdoc
        assert callable(da.check.schema.engdoc.validate)
