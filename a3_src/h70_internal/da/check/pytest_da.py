# -*- coding: utf-8 -*-
"""
Plugin to adapt and configure py.test for use with development automation.

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

import figleaf


# -----------------------------------------------------------------------------
def pytest_addoption(parser):
    """
    Add DA options to the pytest command line.

    """
    group = parser.getgroup('DA', 'Development Automation options.')
    group.addoption('--coverage-log', action = 'store',
                                       type   = 'string')


# -----------------------------------------------------------------------------
def pytest_sessionstart(session):                       # pylint: disable=W0613
    """
    Start figleaf coverage reporting.

    """
    figleaf.start()


# -----------------------------------------------------------------------------
def pytest_runtest_setup(item):
    """
    Notify figleaf that a new testcase/section is about to start.

    """
    figleaf.start_section(item.nodeid)


# -----------------------------------------------------------------------------
def pytest_runtest_teardown(item, nextitem):            # pylint: disable=W0613
    """
    Notify figleaf that the current testcase/section has just ended.

    """
    figleaf.stop_section()


# -----------------------------------------------------------------------------
def pytest_sessionfinish(session, exitstatus):          # pylint: disable=W0613
    """
    Write out figleaf coverage report for the test session.

    """
    figleaf.stop()
    filepath_coverage_log = session.config.known_args_namespace.coverage_log
    with open(filepath_coverage_log, 'wb') as file:
        figleaf.dump_pickled_coverage(file)
