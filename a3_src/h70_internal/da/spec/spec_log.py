# -*- coding: utf-8 -*-
"""
Unit tests for the da.log module.

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


import logging
import os
import re


# =============================================================================
class SpecifyTrace:
    """
    Specify the da.log.trace() function.

    """

    def it_is_callable(self):
        """
        The trace() function is callable.

        """
        import da.log
        assert callable(da.log.trace)


# =============================================================================
class SpecifyConfigure:
    """
    Specify the da.log.configure() function.

    """

    def it_configures_console_and_file_logging(self, tmpdir, capsys):
        """
        The configure() function configures console and file logging.

        """
        import da.log
        dirpath_log = str(tmpdir)
        da.log.configure(dirpath_log      = dirpath_log,
                         loglevel_overall = logging.DEBUG,
                         loglevel_console = logging.DEBUG,
                         loglevel_file    = logging.DEBUG)

        logging.debug('TEST_MESSAGE')

        with open(os.path.join(dirpath_log, 'build.log.jseq')) as file:
            assert file.read() == \
                    '{"l":DEBUG, "m":"spec_log",'\
                    ' "f":"it_configures_console_and_file_logging",'\
                    ' "s":"TEST_MESSAGE"}\n'

        (stdout, stderr) = capsys.readouterr()
        assert stdout == ''
        assert re.match('^[0-9]{6} - TEST_MESSAGE\n$', stderr)


    def it_sets_separate_log_levels_for_console_and_file(self, tmpdir, capsys):
        """
        The configure() function sets separate console and file log levels.

        """
        import da.log
        dirpath_log = str(tmpdir)
        da.log.configure(dirpath_log      = dirpath_log,
                         loglevel_overall = logging.DEBUG,
                         loglevel_console = logging.CRITICAL,
                         loglevel_file    = logging.DEBUG)

        logging.debug('TEST_MESSAGE')

        with open(os.path.join(dirpath_log, 'build.log.jseq')) as file:
            assert file.read() == \
                    '{"l":DEBUG, "m":"spec_log",'\
                    ' "f":"it_sets_separate_log_levels_for_console_and_file",'\
                    ' "s":"TEST_MESSAGE"}\n'

        (stdout, stderr) = capsys.readouterr()
        assert stdout == ''
        assert stderr == ''


# =============================================================================
class SpecifyJseqFormatterFormat:
    """
    Specify the da.log.JseqFormatter.format() method.

    """

    def it_is_callable(self):
        """
        The format() function is callable.

        """
        import da.log
        assert callable(da.log.JseqFormatter.format)


# =============================================================================
class SpecifyJseqFormatterFormattime:
    """
    Specify the da.log.JseqFormatter.formatTime() method.

    """

    def it_is_callable(self):
        """
        The formatTime() function is callable.

        """
        import da.log
        assert callable(da.log.JseqFormatter.formatTime)


# =============================================================================
class SpecifyJseqFormatterFormatexception:
    """
    Specify the da.log.JseqFormatter.formatException() method.

    """

    def it_is_callable(self):
        """
        The formatException() function is callable.

        """
        import da.log
        assert callable(da.log.JseqFormatter.formatException)
