# -*- coding: utf-8 -*-
"""
Day-of-week manipulation functions functions.

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

import datetime


_IDX_MONDAY        = 0
_IDX_TUESDAY       = 1
_IDX_WEDNESDAY     = 2
_IDX_THURSDAY      = 3
_IDX_FRIDAY        = 4
_IDX_SATURDAY      = 5
_IDX_SUNDAY        = 6

_DAYS_IN_WEEK      = 7
_DAYS_IN_FORTNIGHT = 2 * _DAYS_IN_WEEK
_MONTHS_IN_YEAR    = 12


# -----------------------------------------------------------------------------
def monday_week_of_the(date):
    """
    Return the date of the Monday of the week containing the specified date.

    """
    return _date_weekday_week_containing(date    = date,
                                         weekday = _IDX_MONDAY)


# -----------------------------------------------------------------------------
def tuesday_week_of_the(date):
    """
    Return the date of the Tuesday of the week containing the specified date.

    """
    return _date_weekday_week_containing(date    = date,
                                         weekday = _IDX_TUESDAY)


# -----------------------------------------------------------------------------
def wednesday_week_of_the(date):
    """
    Return the date of the Wednesday of the week containing the specified date.

    """
    return _date_weekday_week_containing(date    = date,
                                         weekday = _IDX_WEDNESDAY)


# -----------------------------------------------------------------------------
def thursday_week_of_the(date):
    """
    Return the date of the Thursday of the week containing the specified date.

    """
    return _date_weekday_week_containing(date    = date,
                                         weekday = _IDX_THURSDAY)


# -----------------------------------------------------------------------------
def friday_week_of_the(date):
    """
    Return the date of the Friday of the week containing the specified date.

    """
    return _date_weekday_week_containing(date    = date,
                                         weekday = _IDX_FRIDAY)


# -----------------------------------------------------------------------------
def saturday_week_of_the(date):
    """
    Return the date of the Saturday of the week containing the specified date.

    """
    return _date_weekday_week_containing(date    = date,
                                         weekday = _IDX_SATURDAY)


# -----------------------------------------------------------------------------
def sunday_week_of_the(date):
    """
    Return the date of the Sunday of the week containing the specified date.

    """
    return _date_weekday_week_containing(date    = date,
                                         weekday = _IDX_SUNDAY)


# -----------------------------------------------------------------------------
def monday_following(date):
    """
    Return the date of the first Monday after the specified date.

    """
    return _first_instance_weekday_after(date    = date,
                                         weekday = _IDX_MONDAY)


# -----------------------------------------------------------------------------
def tuesday_following(date):
    """
    Return the date of the first Tuesday after the specified date.

    """
    return _first_instance_weekday_after(date    = date,
                                         weekday = _IDX_TUESDAY)


# -----------------------------------------------------------------------------
def wednesday_following(date):
    """
    Return the date of the first Wednesday after the specified date.

    """
    return _first_instance_weekday_after(date    = date,
                                         weekday = _IDX_WEDNESDAY)


# -----------------------------------------------------------------------------
def thursday_following(date):
    """
    Return the date of the first Thursday after the specified date.

    """
    return _first_instance_weekday_after(date    = date,
                                         weekday = _IDX_THURSDAY)


# -----------------------------------------------------------------------------
def friday_following(date):
    """
    Return the date of the first Friday after the specified date.

    """
    return _first_instance_weekday_after(date    = date,
                                         weekday = _IDX_FRIDAY)


# -----------------------------------------------------------------------------
def saturday_following(date):
    """
    Return the date of the first Saturday after the specified date.

    """
    return _first_instance_weekday_after(date    = date,
                                         weekday = _IDX_SATURDAY)


# -----------------------------------------------------------------------------
def sunday_following(date):
    """
    Return the date of the first Sunday after the specified date.

    """
    return _first_instance_weekday_after(date    = date,
                                         weekday = _IDX_SUNDAY)


# -----------------------------------------------------------------------------
def first_thursday_of_month(year, month):
    """
    Return the date of the first Thursday of the specified month.

    """
    month_start_date = datetime.date(year = year, month = month, day = 1)
    return thursday_following(month_start_date)


# -----------------------------------------------------------------------------
def second_thursday_of_month(year, month):
    """
    Return the date of the second Thursday of the specified month.

    """
    first_thursday  = first_thursday_of_month(year, month)
    return first_thursday + datetime.timedelta(days = _DAYS_IN_WEEK)


# -----------------------------------------------------------------------------
def third_thursday_of_month(year, month):
    """
    Return the date of the third Thursday of the specified month.

    """
    first_thursday  = first_thursday_of_month(year, month)
    return first_thursday + datetime.timedelta(days = _DAYS_IN_FORTNIGHT)


# -----------------------------------------------------------------------------
def last_thursday_of_month(year, month):
    """
    Return the date of the last Thursday of the specified month.

    """
    month_after             = (month % _MONTHS_IN_YEAR) + 1
    year_of_month_after     = year + 1 if month_after == 1 else year
    first_thurs_month_after = first_thursday_of_month(
                                          year  = year_of_month_after,
                                          month = month_after)
    one_week                = datetime.timedelta(days = _DAYS_IN_WEEK)
    date_of_last_thurs      = first_thurs_month_after - one_week
    return date_of_last_thurs


# -----------------------------------------------------------------------------
def _first_instance_weekday_after(date, weekday):
    """
    Return the date of the specified weekday following the specified date.

    Return the next occurring instance of the specified weekday that follows
    the specified date.

    """
    return date + datetime.timedelta(
                        days = ((weekday - date.weekday()) % _DAYS_IN_WEEK))


# -----------------------------------------------------------------------------
def _date_weekday_week_containing(date, weekday):
    """
    Return the date of the given weekday in the week containing specified date.

    """
    return date + datetime.timedelta(days = weekday - date.weekday())
