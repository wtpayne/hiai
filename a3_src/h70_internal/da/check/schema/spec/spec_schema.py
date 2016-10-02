# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.schema package.

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


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'module')
def load():
    """
    Return a mapping from identifier-class-name to validating schema.

    """
    import io
    import textwrap
    import yaml

    def _load(raw_text):
        return yaml.load(io.BytesIO(textwrap.dedent(raw_text).encode()))

    return _load


# =============================================================================
class SpecifyCoro:
    """
    Specify the da.check.schema.coro() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_something(self, dirpath_lwc_root):
        """
        The da.check.schema.checker_coro returns something.

        """
        import da.check.schema
        coro = da.check.schema.coro(build_monitor    = None,
                                    dirpath_lwc_root = dirpath_lwc_root)
        assert coro is not None
