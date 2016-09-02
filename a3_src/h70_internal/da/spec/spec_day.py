# -*- coding: utf-8 -*-
"""
Unit tests for the da.day module.

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
class SpecifyMondayWeekOfThe:
    """
    Specify the da.day.monday_week_of_the() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The monday_week_of_the() function is callable.

        """
        import da.day
        assert callable(da.day.monday_week_of_the)


# =============================================================================
class SpecifyTuesdayWeekOfThe:
    """
    Specify the da.day.tuesday_week_of_the() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The tuesday_week_of_the() function is callable.

        """
        import da.day
        assert callable(da.day.tuesday_week_of_the)


# =============================================================================
class SpecifyWednesdayWeekOfThe:
    """
    Specify the da.day.wednesday_week_of_the() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The wednesday_week_of_the() function is callable.

        """
        import da.day
        assert callable(da.day.wednesday_week_of_the)


# =============================================================================
class SpecifyThursdayWeekOfThe:
    """
    Specify the da.day.thursday_week_of_the() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The thursday_week_of_the() function is callable.

        """
        import da.day
        assert callable(da.day.thursday_week_of_the)


# =============================================================================
class SpecifyFridayWeekOfThe:
    """
    Specify the da.day.friday_week_of_the() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The friday_week_of_the() function is callable.

        """
        import da.day
        assert callable(da.day.friday_week_of_the)


# =============================================================================
class SpecifySaturdayWeekOfThe:
    """
    Specify the da.day.saturday_week_of_the() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The saturday_week_of_the() function is callable.

        """
        import da.day
        assert callable(da.day.saturday_week_of_the)


# =============================================================================
class SpecifySundayWeekOfThe:
    """
    Specify the da.day.sunday_week_of_the() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The sunday_week_of_the() function is callable.

        """
        import da.day
        assert callable(da.day.sunday_week_of_the)


# =============================================================================
class SpecifyMondayFollowing:
    """
    Specify the da.day.monday_following() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The monday_following() function is callable.

        """
        import da.day
        assert callable(da.day.monday_following)


# =============================================================================
class SpecifyTuesdayFollowing:
    """
    Specify the da.day.tuesday_following() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The tuesday_following() function is callable.

        """
        import da.day
        assert callable(da.day.tuesday_following)


# =============================================================================
class SpecifyWednesdayFollowing:
    """
    Specify the da.day.wednesday_following() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The wednesday_following() function is callable.

        """
        import da.day
        assert callable(da.day.wednesday_following)


# =============================================================================
class SpecifyThursdayFollowing:
    """
    Specify the da.day.thursday_following() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The thursday_following() function is callable.

        """
        import da.day
        assert callable(da.day.thursday_following)


# =============================================================================
class SpecifyFridayFollowing:
    """
    Specify the da.day.friday_following() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The friday_following() function is callable.

        """
        import da.day
        assert callable(da.day.friday_following)


# =============================================================================
class SpecifySaturdayFollowing:
    """
    Specify the da.day.saturday_following() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The saturday_following() function is callable.

        """
        import da.day
        assert callable(da.day.saturday_following)


# =============================================================================
class SpecifySundayFollowing:
    """
    Specify the da.day.sunday_following() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The sunday_following() function is callable.

        """
        import da.day
        assert callable(da.day.sunday_following)


# =============================================================================
class SpecifyFirstThursdayOfMonth:
    """
    Specify the da.day.first_thursday_of_month() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The first_thursday_of_month() function is callable.

        """
        import da.day
        assert callable(da.day.first_thursday_of_month)
        # Just to get a bare minimum of coverage.
        assert da.day.first_thursday_of_month(2000, 1) is not None


# =============================================================================
class SpecifySecondThursdayOfMonth:
    """
    Specify the da.day.second_thursday_of_month() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The second_thursday_of_month() function is callable.

        """
        import da.day
        assert callable(da.day.second_thursday_of_month)


# =============================================================================
class SpecifyThirdThursdayOfMonth:
    """
    Specify the da.day.third_thursday_of_month() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The third_thursday_of_month() function is callable.

        """
        import da.day
        assert callable(da.day.third_thursday_of_month)


# =============================================================================
class SpecifyLastThursdayOfMonth:
    """
    Specify the da.day.last_thursday_of_month() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The last_thursday_of_month() function is callable.

        """
        import da.day
        assert callable(da.day.last_thursday_of_month)
