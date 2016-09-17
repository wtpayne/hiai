# -*- coding: utf-8 -*-
"""
Module containing pylint checking coroutines.

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

import pylint.lint
import pylint.reporters

import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(dirpath_lwc_root, error_handler):
    """
    Send errors to error_handler if supplied files not compliant with pylint.

    """
    dirpath_internal = da.lwc.discover.path(
                                    key = 'internal',
                                    dirpath_lwc_root = dirpath_lwc_root)
    dirpath_check    = os.path.join(dirpath_internal, 'da', 'check')

    while True:
        build_element = (yield)
        filepath      = build_element['filepath']

        # Ignore non-python design documents.
        if not da.lwc.file.is_python_file(filepath):
            continue

        # Ignore experimental design documents.
        if da.lwc.file.is_experimental(filepath):
            continue

        _run_lint(filepath      = filepath,
                  pylint_args   = _args_for_design_docs(dirpath_check),
                  error_handler = error_handler)

        if 'spec' in build_element:
            _run_lint(filepath      = build_element['spec']['filepath'],
                      pylint_args   = _args_for_specifications(dirpath_check),
                      error_handler = error_handler)


# -----------------------------------------------------------------------------
def _run_lint(filepath, pylint_args, error_handler):
    """
    Run pylint.

    """
    pylint_args.append(filepath)
    reporter = pylint.reporters.CollectingReporter()
    pylint.lint.Run(pylint_args, reporter = reporter, exit = False)
    for msg in reporter.messages:
        error_handler.send({
            'tool':   'pylint',
            'msg_id': msg.msg_id,
            'msg':    msg.symbol,
            'file':   filepath,
            'line':   msg.line,
            'col':    msg.column
        })

        # TODO: Consider additional fields for customised reporting
        #       for each tool
        # html.escape(msg.msg or '')
        # msg.category,
        # msg.module,
        # msg.obj,
        # msg.path,
        # msg.symbol,


# -----------------------------------------------------------------------------
def _args_for_specifications(dirpath_check):
    """
    Return pylint args suitable for linting product specification documents.

    Several whitespace related rules (C0326, C0330,
    W0311) are disabled to permit the vertical
    alignment of operators and operands on consecutive
    lines. This allows us to visually group related
    statements and to readily identify discrepanices.

    Rules I0011, I0012, I0020 and W0511 are disabled
    pending a decision about how to integrate violations
    of these rules into the development process.

    Rules E1129, E0401 and W0622 are disabled because
    of false or inappropriate alarms.

    """
    filepath_pylintrc = os.path.join(dirpath_check, 'specification.pylintrc')
    return [
        '--rcfile={file}'.format(file = filepath_pylintrc),
        '--reports=no',
        '--ignore=a0_env'
        '--enable=all',

        # Specification tests for the same function
        # are grouped together in class blocks. This
        # is done to facilitate traceability rather
        # than to make use of object-oriented development
        # techniques. Many class and object oriented
        # design rules are therefore not applicable
        # to specification documents.
        #
        '--disable=R0201',  # no-self-use
        '--disable=R0903',  # too-few-public-methods

        # Test fixtures are bound to the test function
        # by giving an argument the same name as the
        # fixture function. When the fixture function
        # sits in the same file as the test function
        # then it will redefine the outer name (the
        # fixture function) in the course of its normal
        # (and exoected) operation.
        #
        '--disable=W0621',  # redefined-outer-name

        # Tests are clearer if we can use assert
        # function() == True
        #
        '--disable=C0121',  # singleton-comparison

        # Test fixtures need to access protected
        # methods.
        #
        '--disable=W0212',  # protected-access


        '--disable=C0103',  # invalid-name        - TBD
        '--disable=C0111',  # missing-docstring   - TBD


        '--disable=C0326',  # bad-whitespace      - Vertical alignment.
        '--disable=C0330',  # bad-continuation    - Vertical alignment.
        '--disable=W0311',  # bad-indentation     - Vertical alignment.
        '--disable=I0011',  # locally-disabled    - TBD
        '--disable=I0012',  # locally-enabled     - TBD
        '--disable=I0020',  # suppressed-message  - TBD
        '--disable=W0511',  # fixme               - TBD
        '--disable=E1129',  # not-context-manager - False alarms?
        '--disable=E0401',  # import-error        - False alarms?
        '--disable=W0622']  # redefined-builtin   - False alarms?


# -----------------------------------------------------------------------------
def _args_for_design_docs(dirpath_check):
    """
    Return pylint args suitable for linting product design documents.

    Several whitespace related rules (C0326, C0330,
    W0311) are disabled to permit the vertical
    alignment of operators and operands on consecutive
    lines. This allows us to visually group related
    statements and to readily identify discrepanices.

    Rules I0011, I0012, I0020 and W0511 are disabled
    pending a decision about how to integrate violations
    of these rules into the development process.

    Rules E1129, E0401 and W0622 are disabled because
    of false or inappropriate alarms.

    """
    filepath_pylintrc = os.path.join(dirpath_check, 'design.pylintrc')
    return [
        '--rcfile={file}'.format(file = filepath_pylintrc),
        '--reports=no',
        '--ignore=a0_env'
        '--enable=all',
        '--disable=C0326',  # bad-whitespace      - Vertical alignment.
        '--disable=C0330',  # bad-continuation    - Vertical alignment.
        '--disable=W0311',  # bad-indentation     - Vertical alignment.
        '--disable=I0011',  # locally-disabled    - TBD
        '--disable=I0012',  # locally-enabled     - TBD
        '--disable=I0020',  # suppressed-message  - TBD
        '--disable=W0511',  # fixme               - TBD
        '--disable=E1129',  # not-context-manager - False alarms?
        '--disable=E0401',  # import-error        - False alarms?
        '--disable=W0622']  # redefined-builtin   - False alarms?
