# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.dependencies module.

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


import json
import textwrap

import pytest


# =============================================================================
class SpecifyCoro:
    """
    Specify the da.check.dependencies.coro() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The coro() function is callabe.

        """
        import da.check.dependencies
        assert callable(da.check.dependencies.coro)


# -----------------------------------------------------------------------------
@pytest.fixture()
def mock_dependencies_register():
    """
    Return a mock system dependencies register as a string.

    """
    return textwrap.dedent("""\
    {

        "title":                    "Mock system dependencies register.",

        "introduction":             "A fake dependencies register for testing.",

        "register": {

            "entry_key": {
                "desc":             "A dummy dependencies register entry.",
                "notes":            "Used to help test registery functions.",
                "dirname":          "directory_name",
                "policy":           "configuration_policy",
                "api": {
                    "api_name_one": "one/api/path",
                    "api_name_two": "another/api/path"
                },
                "cli": {
                    "cli_name_one": "one/cli/path",
                    "cli_name_two": "another/cli/path"
                },
                "gui": {
                    "gui_name_one": "one/gui/path",
                    "gui_name_two": "another/gui/path"
                },
                "config": {
                    "method":       "automatic",
                    "tool":         "git",
                    "url":          "http://some.git.url"
                },
                "build": {
                    "method":       "automatic",
                    "tool":         "some/bash/script.sh"
                }
            }
        }
    }
    """)


# =============================================================================
class Specify_FormatRegister:
    """
    Specify the da.check.dependencies.format_register_data() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_formatted_system_dependencies_register(
                                            self, mock_dependencies_register):
        """
        The format_register_data() function returns a formatted string.

        """
        import da.check.dependencies
        returned_string = da.check.dependencies._format_register(
                                        json.loads(mock_dependencies_register))
        assert returned_string == mock_dependencies_register
