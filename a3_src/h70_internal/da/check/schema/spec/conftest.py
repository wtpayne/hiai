# -*- coding: utf-8 -*-
"""
Package containing test fixtures for schema validation tests.

---
type:
    python_package

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
def dirpath_lwc_root():
    """
    Return the directory path to the root of the local working copy.

    """
    import da.lwc.discover
    return da.lwc.discover.path('root')


# -----------------------------------------------------------------------------
# W0621 redefined-outer-name is disabled. The parameter dirpath_lwc_root is
# not actually redefining the function definition of the same name (above) but
# rather calling it (the function) via the magic of py.test fixtures.
@pytest.fixture(scope = 'module')
def idclass_tab(dirpath_lwc_root):                      # pylint: disable=W0621
    """
    Return a mapping from identifier-class-name to validating schema.

    """
    import da.check.schema.common
    return da.check.schema.common.idclass_schema(dirpath_lwc_root)


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
        """
        Return data deserialised from the provided YAML format text.

        """
        return yaml.load(io.BytesIO(textwrap.dedent(raw_text).encode()))

    return _load
