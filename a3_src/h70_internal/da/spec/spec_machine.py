# -*- coding: utf-8 -*-
"""
Unit tests for the machine module.

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
class SpecifyMachineId:
    """
    Specify the da.machine.machine_id() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_valid_machine_id(self):
        """
        The machine_id() function returns a valid machine-id string.

        """
        import da.machine
        assert da.machine.machine_id().startswith('z')


# =============================================================================
class SpecifyEnvId:
    """
    Specify the da.machine.env_id() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_valid_environment_id(self):
        """
        The env_id() function returns a valid runtime-environment-id string.

        """
        import da.machine
        assert da.machine.env_id().startswith('e')


# =============================================================================
class SpecifyGethostname:
    """
    Specify the da.machine.gethostname() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_valid_hostname(self):
        """
        The gethostname() function returns a valid hostname string.

        """
        import da.machine
        hostname = da.machine.gethostname()
        assert len(hostname) > 0
