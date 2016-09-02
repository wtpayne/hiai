# -*- coding: utf-8 -*-
"""
Unit tests for the da.daybook module.

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
class SpecifyLoad:
    """
    Specify the da.daybook.load() function.

    """

    # -------------------------------------------------------------------------
    def it_loads_a_daybook_that_is_known_to_exist(self):
        """
        Test that we can load a known daybook.

        """
        import da.daybook
        daybook = da.daybook.load(iso_year_id      = '2016',
                                  timebox_id       = '1601A',
                                  team_member_id   = 't000_wtp',
                                  dirpath_lwc_root = None)
        assert daybook is not None


# =============================================================================
class SpecifyLatestEntry:
    """
    Specify the da.daybook.latest_entry() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.daybook
        assert callable(da.daybook.latest_entry)


# =============================================================================
class SpecifyGetLastChronicleEntry:
    """
    Specify the da.daybook.get_last_chronicle_entry() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.daybook
        assert callable(da.daybook.get_last_chronicle_entry)


# =============================================================================
class SpecifyGetJobFromAgenda:
    """
    Specify the da.daybook.get_job_from_agenda() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.daybook
        assert callable(da.daybook.get_job_from_agenda)
