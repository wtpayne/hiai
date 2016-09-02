# -*- coding: utf-8 -*-
"""
Unit tests for the da.build module.

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
class SpecifyCfgserialiser:
    """
    Specify the da.build.cfgserialiser() function.

    """

    # -------------------------------------------------------------------------
    def it_serialises_dates_as_iso8601_format_strings(self):
        """
        cfgserialiser returns ISO 8601 format date strings from datetime input.

        """
        import da.build
        import datetime
        assert da.build.cfgserialiser(
                    datetime.datetime(year   = 2015,
                                      month  = 10,
                                      day    = 21,
                                      hour   = 7,
                                      minute = 28)) == '2015-10-21T07:28:00'

    # -------------------------------------------------------------------------
    def it_raises_type_error_when_given_something_other_than_a_datetime(self):
        """
        cfgserialiser raises a Type Error when given non-datetime inputs.

        """
        import da.build
        import pytest
        with pytest.raises(TypeError):
            da.build.cfgserialiser(None)


# =============================================================================
class SpecifyMain:
    """
    Specify the da.build.main() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The main() function is callable.

        """
        import da.build
        assert callable(da.build.main)
