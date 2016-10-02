# -*- coding: utf-8 -*-
"""
Module containing mypy type checking coroutines.

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


import itertools
import os
import subprocess

import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(dirpath_lwc_root, build_monitor):
    """
    Send errors to build_monitor if supplied files not compliant with pep8.

    """
    filepath_mypy = da.lwc.env.cli_path(
                                dependency_id    = 'mypy',
                                application_name = 'mypy',
                                dirpath_lwc_root = dirpath_lwc_root)

    # TODO: Figure out a way of correctly
    #       installing MyPy so that we do
    #       not need this typeshed path
    #       hack business.
    dirpath_typeshed = os.path.abspath(
                            os.path.join(
                                os.path.dirname(filepath_mypy),
                                '../lib/mypy/typeshed'))

    # Run main file-processing loop: recieve file
    # paths from outside the coroutine and send
    # them one at a time to mypy.
    #
    while True:

        build_unit = (yield)
        filepath   = build_unit['filepath']

        # Ignore non-python design documents.
        if not da.lwc.file.is_python_file(filepath):
            continue

        # Ignore experimental design documents.
        if da.lwc.file.is_experimental(filepath):
            continue

        # Call mypy
        #
        # --junit-xml=FILE
        mypy_command = [
            filepath_mypy,
            '--silent-imports',
            '--show-column-numbers',
            '--custom-typeshed-dir={dir}'.format(dir = dirpath_typeshed),
            filepath]

        process  = subprocess.Popen(mypy_command,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
        out, err = process.communicate()
        exitcode = process.returncode

        # Temprarily disabled while I figure out how
        # to parse MyPy output / Use the MyPy API.
        #
        if exitcode is None:
            for line in itertools.chain(out, err):
                build_monitor.report_nonconformity(
                    tool    = 'da.check.pytype',
                    msg_id  = '999',
                    msg     = line,
                    path    = filepath)
