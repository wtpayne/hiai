# -*- coding: utf-8 -*-
"""
Unit tests for the da.lwc.run module.

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


import pytest

import da.lwc.run


# -----------------------------------------------------------------------------
@pytest.fixture
def patch_subprocess_call(monkeypatch):
    """
    Replace subprocess.call with a dummy noop function call.

    """
    def noop(_):
        return 0

    monkeypatch.setattr(da.lwc.run, '_subprocess_call', noop)


# =============================================================================
class SpecifyPython2:
    """
    Specify the da.lwc.run.python2() function.

    """

    def it_is_callable(self):
        """
        The python2() function is callable.

        """
        assert callable(da.lwc.run.python2)


# =============================================================================
class SpecifyPython3:
    """
    Specify the da.lwc.run.python3() function.

    """

    def it_is_callable(self):
        """
        The python3() function is callable.

        """
        assert callable(da.lwc.run.python3)


# =============================================================================
class SpecifyBash:
    """
    Specify the da.lwc.run.bash() function.

    """

    def it_is_callable(self):
        """
        The bash() function is callable.

        """
        assert callable(da.lwc.run.bash)


# =============================================================================
class SpecifySubl:
    """
    Specify the da.lwc.run.subl() function.

    """

    def it_is_callable(self, patch_subprocess_call):    # pylint: disable=W0613
        """
        The subl() function is callable.

        """
        assert da.lwc.run.subl() == 0
