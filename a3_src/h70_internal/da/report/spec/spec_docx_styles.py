# -*- coding: utf-8 -*-
"""
Unit tests for the da.report.docx_styles module.

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
class SpecifySetDefaultMargins:
    """
    Specify the da.report.set_default_margins() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The set_default_margins() function is callable.

        """
        import da.report.docx_styles
        assert callable(da.report.docx_styles.set_default_margins)


# =============================================================================
class SpecifySetStyles:
    """
    Specify the da.report.set_styles() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The set_styles() function is callable.

        """
        import da.report.docx_styles
        assert callable(da.report.docx_styles.set_styles)
