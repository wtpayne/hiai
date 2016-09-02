# -*- coding: utf-8 -*-
"""
Time-boxed development planning functions.

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

import da.day


_DAYS_IN_WEEK      = 7
_DAYS_IN_FORTNIGHT = 2 * _DAYS_IN_WEEK
_DAYS_IN_YEAR      = 365.242
_DAYS_IN_CENTURY   = 100 * _DAYS_IN_YEAR


# -----------------------------------------------------------------------------
def ident(date):
    """
    Return a timebox id for the specified date.

    """
    thursday            = da.day.thursday_week_of_the(date)
    two_weeks_ago       = thursday - datetime.timedelta(_DAYS_IN_FORTNIGHT)
    in_first_fortnight  = thursday.month != two_weeks_ago.month

    timebox_suffix      = 'A' if in_first_fortnight else 'B'
    timebox_id          = '{year}{month:02}{suffix}'.format(
                                            year   = str(thursday.year)[2:],
                                            month  = thursday.month,
                                            suffix = timebox_suffix)

    return timebox_id


# -----------------------------------------------------------------------------
def timebox_year(date):
    """Return the timebox effective year for the specified date."""
    return da.day.thursday_week_of_the(date).year


# -----------------------------------------------------------------------------
def timebox_dates_for_month(date):
    """
    There are two timeboxes per month - A and B.

       - timebox_a is the first timebox this month.
       - timebox_b is the second timebox this month.

    """
    timebox_a_start = da.day.monday_week_of_the(
                                        da.day.first_thursday_of_month(
                                                                 date.year,
                                                                 date.month))

    timebox_a_end   = da.day.sunday_week_of_the(
                                        da.day.second_thursday_of_month(
                                                                 date.year,
                                                                 date.month))

    timebox_b_start = da.day.monday_week_of_the(
                                        da.day.third_thursday_of_month(
                                                                 date.year,
                                                                 date.month))

    timebox_b_end   = da.day.sunday_week_of_the(
                                        da.day.last_thursday_of_month(
                                                                 date.year,
                                                                 date.month))

    return ((timebox_a_start, timebox_a_end),
            (timebox_b_start, timebox_b_end))


# -----------------------------------------------------------------------------
def timebox_start_date(timebox_id, time_now = None):
    """
    Return the starting date for the specified timebox id.

    """
    if time_now is None:
        time_now = datetime.datetime.now(datetime.timezone.utc)

    time_now = datetime.date(year  = time_now.year,
                             month = time_now.month,
                             day   = time_now.day)

    min_abs_delta_days = datetime.timedelta.max
    for delta_century in [-1, 0, 1]:
        candidate_date = _candidate_timebox_start_date(
                                        timebox_id, time_now, delta_century)
        abs_delta_days = abs(time_now - candidate_date)
        if abs_delta_days < min_abs_delta_days:
            min_abs_delta_days = abs_delta_days
            min_delta_date     = candidate_date

    return min_delta_date


# -----------------------------------------------------------------------------
def _candidate_timebox_start_date(timebox_id, time_now, delta_century):
    """
    Generate a candidate timebox start date for the specified century.

    """
    delta_days        = delta_century * _DAYS_IN_CENTURY
    candidate_century = time_now + datetime.timedelta(days = delta_days)

    first_two_digits  = '{year}'.format(year = candidate_century.year)[0:2]
    last_two_digits   = timebox_id[0:2]

    string_year       = '{first}{last}'.format(first = first_two_digits,
                                               last = last_two_digits)
    string_month      = timebox_id[2:4]

    first_thursday    = da.day.first_thursday_of_month(
                                                    year  = int(string_year),
                                                    month = int(string_month))

    if timebox_id.endswith('A'):
        start_date = da.day.monday_week_of_the(first_thursday)
    elif timebox_id.endswith('B'):
        third_thursday = first_thursday + datetime.timedelta(
                                                    days = _DAYS_IN_FORTNIGHT)
        return da.day.monday_week_of_the(third_thursday)
    else:
        raise RuntimeError('Bad timebox_id {id}'.format(id = timebox_id))

    return start_date
