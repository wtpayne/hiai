# -*- coding: utf-8 -*-
"""
Unit tests for the da.index module.

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
class SpecifyIterEmbedData:
    """
    Specify the da.index.iter_embed_data() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The iter_embed_data() function is callable.

        """
        import da.index
        assert callable(da.index.iter_embed_data)

# =============================================================================
class SpecifyWrite:
    """
    Specify the da.index.write() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The write() function is callable.

        """
        import da.index
        assert callable(da.index.write)

# =============================================================================
class SpecifyIndexCoro:
    """
    Specify the da.index.index_coro() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The index_coro() function is callable.

        """
        import da.index
        assert callable(da.index.index_coro)


# -----------------------------------------------------------------------------
def it_exists():
    """
    Placeholder test to provide minimal coverage.

    To be replaced when minimum coverage limits are instituted.

    """
    import da.index
    assert da.index._id_matcher_coro(None) is not None
