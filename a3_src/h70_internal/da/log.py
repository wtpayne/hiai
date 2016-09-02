# -*- coding: utf-8 -*-
"""
Logging module configuration & customisation.

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

import functools
import logging
import sys
import os

import da.util


# ------------------------------------------------------------------------------
def trace(func):
    """
    Tracelog function decorator.

    """
    @functools.wraps(func)
    def wrapper(*args, **kwds):
        """
        Wrap an arbitrary function, logging entry & exit.

        """
        logging.debug('ENTER %s.%s()', func.__module__, func.__name__)
        retval = func(*args, **kwds)
        logging.debug('EXIT  %s.%s()', func.__module__, func.__name__)
        return retval
    return wrapper


# =============================================================================
class JseqFormatter(logging.Formatter):
    """
    Custom Logging Formatter class for outputting JSON Sequence (JSEQ) files.

    """

    def __init__(self):
        """
        Return a new instance of the JseqFormatter class.

        """
        super(JseqFormatter, self).__init__(
            fmt     = '{"l":%(levelname)s,'      +
                      ' "m":"%(module)s",'       +
                      ' "f":"%(funcName)s",'     +
                      ' "s":"%(message)s"}',
            datefmt = '%H%M%S')

    def format(self, record):
        """
        Format the specified record as text.

        Wraps logging.Formatter.format

        """
        return super(JseqFormatter, self).format(record)

    # Pylint rule C0103 (invalid-name) has been
    # disabled in this instance because the
    # design of this class is predetermined by
    # the architecture of the logging library
    # and is not under our control.
    def formatTime(self, record, datefmt):              # pylint: disable=C0103
        """
        Return the creation time of the specified LogRecord as formatted text.

        Wraps logging.Formatter.formatTime

        """
        return super(JseqFormatter, self).formatTime(record, datefmt)

    # Pylint rule C0103 (invalid-name) has been
    # disabled in this instance because the
    # design of this class is predetermined by
    # the architecture of the logging library
    # and is not under our control.
    def formatException(self, exc_info):                # pylint: disable=C0103
        """
        Format and return the specified exception information as a string.

        Wraps logging.Formatter.formatException

        """
        return super(JseqFormatter, self).formatException(exc_info)


# -----------------------------------------------------------------------------
def configure(dirpath_log, loglevel_overall, loglevel_console, loglevel_file):
    """
    Configure loggers and log handlers.

    """
    # Configure root logger so we can use logging-module-level log functions.
    logger = logging.getLogger()
    logger.setLevel(loglevel_overall)

    # TODO: NEED A CUSTOM LOG HANDLER TO USE CLICK ECHO INTERFACE ...

    # Simple uncluttered logging to console ...
    # (Consider adding custom handler for click CLI integration ...)
    logconsole = logging.StreamHandler(stream = sys.stderr)
    logconsole.setLevel(loglevel_console)
    logconsole.setFormatter(logging.Formatter(
                                        fmt     = '%(asctime)s - %(message)s',
                                        datefmt = '%H%M%S'))
    logger.addHandler(logconsole)

    # JSON-object-per-line logging to file for machine consumption
    da.util.ensure_dir_exists(dirpath_log)
    filepath_jseq = os.path.join(dirpath_log, 'build.log.jseq')
    logjseq       = logging.FileHandler(
        filename = filepath_jseq,
        mode     = 'w',               # Clear log file before each build
        encoding = 'utf-8')
    logjseq.setLevel(loglevel_file)
    logjseq.setFormatter(JseqFormatter())
    logger.addHandler(logjseq)
