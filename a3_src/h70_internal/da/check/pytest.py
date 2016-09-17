# -*- coding: utf-8 -*-
"""
Module containing pytest checking coroutines.

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


import contextlib
import json
import os
import re
import sys

import figleaf
import pytest

import da.lwc.file
import da.python_source
import da.util


_REGEX_CAMEL2UNDER = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(dirpath_src, error_handler):
    """
    Send errors to error_handler if the unit tests for supplied modules fail.

    """
    dirpath_internal = da.lwc.discover.path(
                                'internal', dirpath_lwc_root = dirpath_src)
    filepath_ini     = os.path.join(
                                dirpath_internal, 'da', 'check', 'pytest.ini')

    while True:

        build_element = (yield)

        filepath_module = build_element['filepath']

        # Ignore non-python design documents.
        if not da.lwc.file.is_python_file(filepath_module):
            continue

        # Ignore experimental design documents.
        if da.lwc.file.is_experimental(filepath_module):
            continue

        # Check to ensure that the test files, classes and methods are present.
        _check_static_coverage(build_element, error_handler)

        filepath_test = da.lwc.file.specification_filepath_for(filepath_module)
        if not os.path.isfile(filepath_test):
            continue

        # Ensure the test results dir exists.
        dirpath_log = build_element['dirpath_log']
        da.util.ensure_dir_exists(dirpath_log)

        # Define test result files.
        filepath_pytest_log   = os.path.join(dirpath_log, 'pytest.log')
        filepath_pytest_out   = os.path.join(dirpath_log, 'pytest_out.log')
        filepath_pytest_err   = os.path.join(dirpath_log, 'pytest_err.log')
        filepath_junit_xml    = os.path.join(dirpath_log, 'pytest.junit.xml')
        filepath_pytest_json  = os.path.join(dirpath_log, 'pytest.json')
        filepath_cover_pickle = os.path.join(dirpath_log, 'test_cover.pickle')
        filepath_cover_json   = os.path.join(dirpath_log, 'test_cover.json')

        # Run a py.test session for the current module's test cases.
        with _pytest_context(dirpath_cwd     = dirpath_src,
                             filepath_stdout = filepath_pytest_out,
                             filepath_stderr = filepath_pytest_err):
            exit_code = pytest.main(
                            [filepath_test,
                             '-p', 'da.check.pytest_da',
                             '--capture=no',
                             '-c='             + filepath_ini,
                             '--result-log='   + filepath_pytest_log,
                             '--junit-xml='    + filepath_junit_xml,
                             '--json='         + filepath_pytest_json,
                             '--coverage-log=' + filepath_cover_pickle])

        # Communicate any test case failures.
        if exit_code != 0:
            _report_unit_test_failure(filepath_test,
                                      filepath_pytest_json,
                                      dirpath_src,
                                      error_handler)

        # Get coverage data grouped by file.
        with open(filepath_cover_pickle, 'rb') as figleaf_pickle:
            figleaf.load_pickled_coverage(figleaf_pickle)
        coverage    = figleaf.get_data()
        cov_by_file = coverage.gather_files()

        cov_log = dict()
        for key, value in cov_by_file.items():
            cov_log[key] = list(value)

        with open(filepath_cover_json, 'wt') as file_cover_json:
            file_cover_json.write(json.dumps(cov_log,
                                             indent    = 4,
                                             sort_keys = True))

        # Get the design elements in the current document that require
        # test coverage.
        #
        ast_module      = build_element['ast']
        module_name     = da.python_source.get_module_name(filepath_module)
        design_elements = list(da.python_source.gen_ast_paths_depth_first(
                                                    ast_module, module_name))

        # Work out if the coverage provided by the
        # unit tests is sufficient.
        #
        # Initially, we just check to see that
        # *some* coverage is given for each
        # document. (Module-level coverage)
        #
        # As we mature this system, we will
        # (conditionally) extend checks to
        # ensure minimum standards for function-
        # level coverage and line-level coverage.
        #
        if len(design_elements) > 1 and filepath_module not in cov_by_file:
            relpath_module = build_element['relpath']
            error_handler.send({
                'tool':   'pytest',
                'msg_id': 'U101',
                'msg':    'No test coverage for module: ' + relpath_module,
                'file':   filepath_test,
                'line':   1,
                'col':    0
            })
            continue

        # For traceability, we can gather sections
        # (= test cases) and correlate them with
        # AST design elements (= functions and classes)
        # for section_id in coverage.sections:
        # cov_by_test = coverage.gather_sections()


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _pytest_context(dirpath_cwd, filepath_stdout, filepath_stderr):
    """
    Context manager helper for running pytest.

    Change directory to dirpath_cwd, and swap
    stdout and stderr to the specified files,
    then set everything back the way it was
    when done.

    """
    with open(filepath_stdout, 'wt') as file_stdout:
        with open(filepath_stderr, 'wt') as file_stderr:
            prev_wd = os.getcwd()
            os.chdir(dirpath_cwd)
            sys_stdout = sys.stdout
            sys_stderr = sys.stderr
            sys.stdout = file_stdout
            sys.stderr = file_stderr
            yield
            sys.stdout = sys_stdout
            sys.stderr = sys_stderr
            os.chdir(prev_wd)


# -----------------------------------------------------------------------------
def _report_unit_test_failure(filepath_test,
                              filepath_pytest_json,
                              dirpath_src,
                              error_handler):
    """
    Report on the failure of a specific test case.

    """
    with open(filepath_pytest_json, 'rt') as file_pytest_json:
        results = json.load(file_pytest_json)

    for test in results['report']['tests']:

        if test['outcome'] == 'passed':
            continue

        for stage in (test['setup'], test['call'], test['teardown']):

            if stage['outcome'] == 'passed':
                continue

            # Set the default error message, error
            # filepath and error line so if we can't
            # find a more detailed one we can still
            # return some sort of message.
            #
            message  = 'Undetermined test failure: {stage}: {path}.'.format(
                                                        stage = stage['name'],
                                                        path  = filepath_test)
            filepath_err = filepath_test
            line_err     = 0

            # Parse the string in the longrepr
            # field (if it exists) to try to get
            # a more accurate message, filepath
            # and line number for our error report.
            #
            if 'longrepr' in stage:
                message       = stage['longrepr']
                message_lines = message.splitlines()
                if len(message_lines) > 0:
                    last_line = message_lines[-1]
                    if ':' in last_line:
                        (relpath_err, line_err) = last_line.split(':')[0:2]
                        filepath_err = os.path.join(dirpath_src, relpath_err)

            error_handler.send({
                'tool':   'pytest',
                'msg_id': 'U200',
                'msg':    message,
                'file':   filepath_err,
                'line':   line_err,
                'col':    0
            })


# -----------------------------------------------------------------------------
def _check_static_coverage(build_element, error_handler):
    """
    Send an error message to the handler if static coverage is incorrect.

    Static coverage is the test coverage that can
    be determined statically - without running the
    test.

    """
    # If we have no functions to be tested, then
    # we don't require any tests.
    #
    top_level_functions = list(da.python_source.gen_top_level_function_names(
                                                        build_element['ast']))
    if not top_level_functions:
        return

    # If we have at least one function to be tested,
    # then we need a file to put our tests in.
    #
    relpath_module = build_element['relpath']
    if 'spec' not in build_element:
        filepath_module = build_element['filepath']
        filepath_spec   = da.lwc.file.specification_filepath_for(
                                                            filepath_module)
        msg = 'No spec found for module: {name}'.format(name = relpath_module)
        error_handler.send({
            'tool':   'pytest_static_coverage',
            'msg_id': 'U100',
            'msg':    msg,
            'file':   filepath_spec,
            'line':   1,
            'col':    0
        })
        # If we don't have a test file, then our
        # other checks are pretty much meaningless,
        # so we can return early here. This allows
        # the rest of the function to be simpler
        # as it does not have to deal with absent
        # test files.
        #
        return

    (permitted_test_class_names,
     mandatory_test_class_names) = _get_expected_test_class_names(
                                                        top_level_functions)

    test_classes = list(da.python_source.gen_top_level_class_names(
                                                build_element['spec']['ast']))

    # Check that all the class names in our test
    # suite correspond to one of the functions
    # in the module or package under test.
    #
    for test_class in test_classes:
        if test_class not in permitted_test_class_names:
            msg = 'Bad test class: {name} for: {module}'.format(
                                            name   = test_class,
                                            module = relpath_module)
            error_handler.send({
                'tool':   'pytest_static_coverage',
                'msg_id': 'U200',
                'msg':    msg,
                'file':   build_element['spec']['filepath'],
                'line':   1,
                'col':    0
            })

    # Check to make sure that each public function
    # or method in the srcfile has a corresponding
    # class in the test-file.
    #
    missing_classes = list()
    for class_name in mandatory_test_class_names:
        if class_name not in test_classes:
            missing_classes.append(class_name)

    if missing_classes:
        msg = 'Missing test classes {missing}.'.format(
                                            missing = repr(missing_classes))
        error_handler.send({
            'tool':   'pytest_static_coverage',
            'msg_id': 'U200',
            'msg':    msg,
            'file':   build_element['spec']['filepath'],
            'line':   1,
            'col':    0
        })


# -----------------------------------------------------------------------------
def _get_expected_test_class_names(top_level_functions):
    """
    Return permitted and mandatory test class names.

    We organise our tests into classes, one class
    for each function that is being tested. The
    name of the class is determined by converting
    the name of the function from underscore
    delimited style to a PascalCase style.

    We enforce the creation of one mandatory test
    class for each public function, and we allow
    optional test classes for each private functions.
    No other test classes are currently allowed.

    """
    permitted_test_class_names = list()
    mandatory_test_class_names = list()

    for under_name in top_level_functions:

        name_parts  = under_name.split('_')
        pascal_name = ''.join(part.capitalize() or '_' for part in name_parts)
        test_class  = 'Specify{pascal_name}'.format(pascal_name = pascal_name)
        is_private  = under_name.startswith('_')

        permitted_test_class_names.append(test_class)
        if not is_private:
            mandatory_test_class_names.append(test_class)

    return (permitted_test_class_names, mandatory_test_class_names)
