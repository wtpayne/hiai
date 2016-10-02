# -*- coding: utf-8 -*-
"""
Runtime configuration and launch logic for third party tools.

This module contains logic to configure and launch third-party tools;
setting environment variables and configuration files as required to
assure interoperability with DA norms and processes.

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

import copy
import logging
import os
import sys
import subprocess

import da.lwc.discover
import da.lwc.env


# -----------------------------------------------------------------------------
def python2(arglist,                                    # pylint: disable=R0913
            stdout           = None,
            stderr           = None,
            cwd              = None,
            env              = None,
            dirpath_lwc_root = None):
    """
    Launch the python 2 interpreter in a subprocess.

    Set the PYTHONPATH environment variable so DA dependencies can be used.

    """
    return _python(
                arglist,
                dependency_id       = 'pyrun2',
                libraries_interface = 'lib_python2',
                stdout              = stdout,
                stderr              = stderr,
                cwd                 = cwd,
                env                 = env,
                dirpath_lwc_root    = dirpath_lwc_root)


# -----------------------------------------------------------------------------
def python3(arglist,                                    # pylint: disable=R0913
            stdout           = None,
            stderr           = None,
            cwd              = None,
            env              = None,
            dirpath_lwc_root = None):
    """
    Launch the python 3 interpreter in a subprocess.

    Set the PYTHONPATH environment variable so DA dependencies can be used.

    """
    return _python(
                arglist,
                dependency_id       = 'pyrun3',
                libraries_interface = 'lib_python3',
                stdout              = stdout,
                stderr              = stderr,
                cwd                 = cwd,
                env                 = env,
                dirpath_lwc_root    = dirpath_lwc_root)


# -----------------------------------------------------------------------------
def _python(arglist,                                    # pylint: disable=R0913
            dependency_id,
            libraries_interface,
            stdout           = None,
            stderr           = None,
            cwd              = None,
            env              = None,
            dirpath_lwc_root = None):
    """
    Launch the python interpreter in a subprocess.

    Set the PYTHONPATH environment variable so DA dependencies can be used.

    """
    if env is None:
        python_import_path = da.lwc.env.python_import_path(
                                iface_name       = libraries_interface,
                                dirpath_lwc_root = dirpath_lwc_root)
        env = copy.copy(os.environ)
        env['PYTHONPATH'] = os.pathsep.join(python_import_path)
        # env['PATH']       = ''

    filepath_python = os.path.join(da.lwc.env.cli_path(
                                dependency_id    = dependency_id,
                                application_name = 'pyrun',
                                dirpath_lwc_root = dirpath_lwc_root))
    try:
        return _subprocess_call(
                    [filepath_python] + arglist,
                    stdout = stdout,
                    stderr = stderr,
                    cwd    = cwd,
                    env    = env)
    except OSError:
        # TODO: This is the exception that you get when you don't have an
        #       environment -- try to print a helpful error message here.
        raise


# -----------------------------------------------------------------------------
def bash(dirpath_lwc_root = None):
    """
    Launch the bash interpreter in a subprocess.

    Set the PATH and PYTHONPATH environment variables so DA dependencies can
    be used.

    """
    dirpath_env = da.lwc.discover.path(
                                'current_env',
                                dirpath_lwc_root = dirpath_lwc_root)
    register    = da.lwc.env.dependencies_register(
                                dirpath_lwc_root = dirpath_lwc_root)
    path_cli    = []

    for dependency_data in register.values():
        for app_name in dependency_data['cli']:
            relpath_app  = dependency_data['cli'][app_name]
            filepath_app = os.path.join(dirpath_env,
                                        dependency_data['dirname'],
                                        dependency_data['policy'],
                                        relpath_app)
            dirpath_app = os.path.normpath(os.path.dirname(filepath_app))
            path_cli.append(dirpath_app)

    env               = copy.copy(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(sys.path)
    env['PATH']       = os.pathsep.join([env['PATH']] + path_cli)
    bash_command      = ['/bin/bash']
    status            = _subprocess_call(bash_command, env = env)
    return status


# -----------------------------------------------------------------------------
def subl(filepath = None, line_number = 1, dirpath_lwc_root = None):
    """
    Open the specified file in Sublime Text.

    """
    if dirpath_lwc_root is None:
        dirpath_lwc_root = da.lwc.discover.path(key = 'root')

    filepath_subl = da.lwc.env.cli_path(
                                dependency_id    = 'subl',
                                application_name = 'sublime_text',
                                dirpath_lwc_root = dirpath_lwc_root)

    if filepath is None:
        logging.debug('Run sublime text')
        return _subprocess_call([filepath_subl])

    # The stack trace that is retrieved during the
    # handling of an Exception thrown from within
    # one of PyRun's built-in libraries may have
    # a stack trace that contains filenames of the
    # form "<pyrun>/filename.py". It is not possible
    # to open such files in the editor.
    #
    # Although this is an anomalous condition, we
    # do not expect the developer to take any
    # remedial action when it is encountered. We
    # therefore refrain from throwing an exception
    # and instead simply log the fact that it has
    # occurred and return normally.
    #
    # It is conceivable that other similar conditions
    # may be encountered, so as a piece of defensive
    # programming, we also take the same action if
    # the filepath parameter does not indicate a
    # valid file.
    if filepath.startswith('<pyrun>') or not os.path.isfile(filepath):
        logging.warning('Cannot open file: "%s"', filepath)
        return 1

    argument = '{filepath}:{line_number}'.format(
                                        filepath    = filepath,
                                        line_number = line_number)
    logging.debug('Open file in sublime text: %s', argument)
    return _subprocess_call([filepath_subl, '-a', argument])


# -----------------------------------------------------------------------------
def _subprocess_call(*args, **kwargs):
    """
    Wrap subprocess.call so we have somewhere we can monkey-patch during test.

    """
    return subprocess.call(*args, **kwargs)
