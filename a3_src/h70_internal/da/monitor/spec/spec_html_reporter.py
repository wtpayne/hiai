# -*- coding: utf-8 -*-
"""
Unit tests for the da.monitor.html_reporter module.

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

# =============================================================================
class SpecifyCoro:
    """
    Specify the da.monitor.html_reporter.coro() function.

    """

    def it_is_callable(self, tmpdir):
        """
        The coro() coroutine is callable.

        """
        dirpath_log     = str(tmpdir)
        filepath_report = os.path.join(str(tmpdir), 'report.html')

        import da.monitor.html_reporter
        coro = da.monitor.html_reporter.coro(filepath_report, dirpath_log)
        coro.send(da.constants.BUILD_COMPLETED)
        assert os.path.isfile(filepath_report)
