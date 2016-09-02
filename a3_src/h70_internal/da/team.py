# -*- coding: utf-8 -*-
"""
Team member utilities.

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

import os
import pwd

import da.register


# -----------------------------------------------------------------------------
def member_id(dirpath_lwc_root = None, user_id = None):
    """
    Return the team member id correspinding to the specified user id.

    Parameters
    ----------

    dirpath_lwc_root : str
        The fully qualified path to the currently active local working copy.

    user_id : str
        The user-id for the team member on the current workstation.

    """
    if user_id is None:
        user_id = _current_user()

    register         = da.register.load(register_name    = 'team',
                                        dirpath_lwc_root = dirpath_lwc_root)
    iter_match       = _generate_matching_members(register, user_id)
    matches          = tuple(iter_match)
    num_match        = len(matches)

    if num_match == 1:
        (matching_id, _) = matches[0]
        return matching_id

    if num_match == 0:
        raise RuntimeError(
                'No matching members found for user: {id}'.format(
                                                                id = user_id))

    if num_match >= 2:
        raise RuntimeError(
                'More than one matching member found for user: {id}'.format(
                                                                id = user_id))


# -----------------------------------------------------------------------------
def _current_user():
    """
    Return the login name of the current user account.

    """
    uid   = os.getuid()
    pwuid = pwd.getpwuid(uid)
    return pwuid.pw_name


# -----------------------------------------------------------------------------
def _generate_matching_members(team_register, user_id):
    """
    Yield members from the team register that match the specified user_id.

    """
    for (team_member_id, member_data) in team_register.items():
        if user_id in member_data["alias"]:
            yield (team_member_id, member_data)
