# -*- coding: utf-8 -*-
"""
Unit tests for the da.memo module.

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


from . import spec_memo


num_calls = 0


# -----------------------------------------------------------------------------
def count_calls():
    spec_memo.num_calls += 1


# =============================================================================
class SpecifyVar:
    """
    Specify the da.memo.var() function

    """

    # -------------------------------------------------------------------------
    def it_calls_the_wrapped_function_once(self):
        """
        The var() function only calls the wrapped function once.

        """
        import da.memo
        @da.memo.var
        def return_42():
            count_calls()
            return 42

        spec_memo.num_calls = 0
        assert return_42() == 42
        assert spec_memo.num_calls == 1

        assert return_42() == 42
        assert spec_memo.num_calls == 1


# =============================================================================
class SpecifyConst:
    """
    Specify the da.memo.const() function

    """
    # -------------------------------------------------------------------------
    def it_calls_the_wrapped_function_once(self):
        """
        The const() function only calls the wrapped function once.

        """
        import da.memo
        @da.memo.const
        def return_42():
            count_calls()
            return 42

        spec_memo.num_calls = 0
        assert return_42() == 42
        assert spec_memo.num_calls == 1

        assert return_42() == 42
        assert spec_memo.num_calls == 1
