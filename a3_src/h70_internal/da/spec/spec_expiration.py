# -*- coding: utf-8 -*-
"""
Unit tests for the da.expiration module.

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
class SpecifySetExpirationDate:
    """
    Specify the da.expiration.set_expiration_date() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The set_expiration_date() function is callable.

        """
        import da.expiration
        assert callable(da.expiration.set_expiration_date)


# =============================================================================
class SpecifyHasExpired:
    """
    Specify the da.expiration.has_expired() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The has_expired() function is callable.

        """
        import da.expiration
        assert callable(da.expiration.has_expired)


# =============================================================================
class Specify_Filename:
    """
    Specify the da.expiration.filename() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_filename_with_the_expiration_date(self):
        """
        The filename() function returns a filename with the expiration date.

        """
        import datetime
        import da.expiration
        filename = da.expiration._filename(
                        current_time         = datetime.datetime(year   = 2015,
                                                                 month  = 10,
                                                                 day    = 21,
                                                                 hour   = 11,
                                                                 minute = 45),
                        timedelta_expiration = datetime.timedelta(days  = 1),
                        identifier           = 'test_identifier')
        assert filename == '201510221100.test_identifier.expiration_date'
