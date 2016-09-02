# -*- coding: utf-8 -*-
"""
Memoization utility functions.

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

import functools


# ------------------------------------------------------------------------------
def var(func):
    """
    Standard memoization function for simple functions.

    Memoization decorator for a function that
    returns different values if it is given
    different input variables.

    """
    memo_cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Return cache contents if present else the function return value.

        Memoization wrapper for a function that
        returns different values if it is given
        different input variables.

        """
        key = (args, repr(kwargs))
        if key not in memo_cache:
            memo_cache[key] = func(*args, **kwargs)
        return memo_cache[key]

    return wrapper


# ------------------------------------------------------------------------------
def const(func):
    """
    Simplified memoization function for constant functions that take no args.

    Memoization decorator for a function that
    returns a constant value irrespective of
    input.

    """
    memo_cache = []

    @functools.wraps(func)
    def wrapper():
        """
        Return cache contents if present else the function return value.

        """
        if not memo_cache:
            memo_cache[:] = [func()]
        return memo_cache[0]

    return wrapper
