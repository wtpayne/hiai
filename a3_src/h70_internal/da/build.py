# -*- coding: utf-8 -*-
"""
The build module is responsible for top level control over the build process.

The build process is responsible for generating a
set of built output artifacts in accordance with a
single specified design configuration.

If a nonconformity in the design is detected, the
build halts and a report is issued.

The build module supports compilation; testing;
documentation generation; running simulations for
performance analysis and any operation which takes
a set of input files and processes them to produce
a set of output files. It is particularly applicable
when the input and output files need to be
configuration-controlled and the operation itself
needs to be reproduceable.

In each case, the input is known as the design
configuration and is represented by a set
of design documents and identified by the git SHA-1
digest.)

This contrasts with the metabuild module, which is
responsible for generating and evaluating multiple
competing design configurations.

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


import ast
import contextlib
import datetime
import json
import logging
import os

import da.bldcfg
import da.check.bulk_data
import da.check.constants
import da.check.dependencies
import da.check.pycodestyle
import da.check.pycomplexity
import da.check.pydocstyle
import da.check.pylint
import da.check.pytest
import da.check.pytype
import da.check.schema
import da.cms
import da.compile.clang
import da.compile.gcc
import da.constants
import da.dep
import da.docgen.design
import da.exception
import da.index
import da.log
import da.lwc
import da.lwc.file
import da.monitor
import da.team


# -----------------------------------------------------------------------------
@da.log.trace
def main(cfg):
    """
    Run a build and return the resulting status code.

    The build.main() function is responsible for
    top level control over the build process.

    The build process takes as input a set of design
    documents. If any nonconformities are detected,
    it issues a report and halts; else it produces
    or updates a set of built artifacts.

    The build.main() function can be configured to
    restrict the set of design documents used as
    build inputs as well as the processing steps
    applied to them.

    In this way we can restrict the build to selected
    products or components, and can apply only the
    specific processing steps that we choose, which
    enables us to get rapid feedback on areas that
    are giving us problems. Even when performing
    complete builds, build inputs and processing
    steps are sequenced to maximise the probability
    of discovering nonconformities early.

    Build processing steps are grouped into two
    sequential phases: The first phase consists of
    steps which accept build units individually,
    and the second phase consists of steps which
    cannot be decomposed down to the level of
    individual units.

    For the first phase of the build, the
    _sequence_build_inputs() generator selects
    design documents from the current configuration
    and sequences them so that the build detects
    nonconformities as early as possible. The
    _unit_processing() coroutine then configures
    and applies unit-by-unit processing steps
    such as static analysis and unit testing.

    For the second phase of the build, the
    _integrated_processing() function selects and
    applies build processing steps which are not
    tied to individual build units, such as report
    generation and test data validation.

    Errors and nonconformities are handled by the
    da.monitor.BuildMonitor class, which contains
    logic for selcting between Jidoka (fail-fast)
    or robust (comprehensive reporting) nonconformity
    response strategies.

    ---
    type: function

    args:
        cfg:    A mapping holding the build configuration.

    returns:
        status: The value da.constants.BUILD_COMPLETED
                is returned upon successful completion.
                An exception is thrown otherwise.
    ...

    """
    _log_build_configuration(cfg)
    build_monitor = da.monitor.BuildMonitor(cfg)

    # First build phase -- process individual build units / design documents.
    build_inputs    = _sequence_build_inputs(cfg, build_monitor)
    unit_processing = _unit_processing(cfg, build_monitor)
    build_data      = None
    for unit in build_inputs:
        build_monitor.report_progress(unit)
        build_data = unit_processing.send(unit)

    # Second build phase -- process the design as an integrated whole.
    _integrated_processing(cfg, build_monitor, build_data)

    logging.debug('Build process ran to completion')
    build_monitor.notify_build_end()
    return da.constants.BUILD_COMPLETED


# -----------------------------------------------------------------------------
def _log_build_configuration(cfg):
    """
    Log the build configuration to a file.

    ---
    type: function

    args:
        cfg: A mapping holding the build configuration.

    ...

    """
    dirpath_branch_log = cfg['paths']['dirpath_branch_log']
    filepath_cfg_log   = os.path.join(dirpath_branch_log, 'cfg.log.json')
    with open(filepath_cfg_log, 'w') as file:
        json.dump(
            obj       = cfg,
            fp        = file,
            default   = cfgserialiser,
            indent    = 4,
            sort_keys = True)
    return None


# -----------------------------------------------------------------------------
def cfgserialiser(date_obj):
    """
    JSON Serialiser for CFG objects.

    This function is used by json.dump to serialise
    build configuration data. It is required because
    the build configuration data structure contains
    datetime objects which are not supported by the
    standard JSON serialiser function.

    ---
    type: function

    args:
        date_obj:   An instance of a datetime.datetime
                    object.

    returns:
        date_str:   A ISO-8601 string representation of
                    the supplied date.
    ...

    """
    if isinstance(date_obj, datetime.datetime):
        date_str = date_obj.isoformat()
        return date_str
    else:
        raise TypeError


# -----------------------------------------------------------------------------
def _sequence_build_inputs(cfg, build_monitor):
    """
    Yield filtered and prioritised build units.

    The build process is a little unusual in that
    it is *not* designed to minimise the overall
    build time,  but rather to minimise the time
    taken to detect a nonconformity after an
    incremental change. A key design goal is to
    detect 95% of nonconformities within the first
    5 seconds of a development build.

    This frees the developer from actively monitoring
    the build after the first few seconds; he may
    then shift his attention to the next task with
    only a 1-in-20 chance of being interrupted by
    a nonconformity report issued in the latter
    stages of the build.

    We assume that more than 95% of edit-build-test
    loop iterations are performed after relatively
    small incremental changes; that more than 75%
    of those changes introduce a nonconformity or
    regression; and that more than 95% of any new
    nonconformities are detected by checks performed
    at or close to the 'unit' level in the V model
    (both static and dynamic).

    Each build unit consists of a single design
    document plus all of it's supporting documents:
    specifications, tests, header files and so on.

    Build unit are selected and prioritised based
    on when they were last modified and by the
    assessed risk of a nonconformity or error.

    The build can be configured to limit the build
    units that are generated so that only particular
    products or projects are built.

    Yielded build units will often include open
    file handles. This generator ensures that each
    of these handles will be closed at the end of
    each iteration.

    ---
    type: generator

    args:
        cfg:            A mapping holding the build configuration.

        build_monitor:  A reference to the build monitoring and
                        progress reporting coroutine.


    yields:
        build_unit:     A mapping with information about a single
                        detailed design document (source file)
                        together with it's supporting specifications
                        and tests. The sequence of yielded build
                        units determines how the build is prioritised.
    ...

    """
    iter_prioritised = _gen_prioritised_filepaths(cfg)
    iter_normalised  = _normalise_filepaths(iter_prioritised, build_monitor)
    iter_restricted  = _restrict_filepaths(cfg, iter_normalised)
    for filepath_design_doc in iter_restricted:

        with _load_design_doc(
                cfg, filepath_design_doc, build_monitor) as part_loaded:

            with _load_supporting_docs(
                    cfg, part_loaded, build_monitor) as build_unit:

                yield build_unit


# -----------------------------------------------------------------------------
def _gen_prioritised_filepaths(cfg):
    """
    Yield a sequence of candidate build input filepaths in priority order.

    ---
    type: generator

    args:
        cfg:            A mapping holding the build configuration.

    yields:
        filepath:       A filepath string pointing to a file in the
                        build isolation area (isolated_src).
    ...

    """
    # Files most recently changed in LWC. (Very short list)
    dirpath_lwc_root         = cfg['paths']['dirpath_lwc_root']
    dirpath_isolated_src     = cfg['paths']['dirpath_isolated_src']
    changed_files            = cfg['changed_files']
    check_changed_files_only = cfg['options']['check_changed_files_only']
    changed_files = _replace_all(string_list = changed_files,
                                 old         = dirpath_lwc_root,
                                 new         = dirpath_isolated_src)

    for filepath in changed_files:
        if not os.path.isdir(filepath):
            yield filepath

    # build_date = datetime.datetime.strptime(cfg['timestamp']['datetime_utc'],
    #                                         da.bldcfg.DATEFMT_DATETIME_UTC)
    # recent_changes = []
    # for lwc_path in da.vcs.files_changed_since(
    #                     timestamp    = da.day.monday_week_of_the(build_date),
    #                     dirpath_root = dirpath_lwc_root):
    #     yield lwc_path.replace(dirpath_lwc_root, dirpath_isolated_src)

    if check_changed_files_only:
        return

    changed_files = set(changed_files)
    for filepath in da.lwc.discover.gen_src_files(dirpath_isolated_src):
        if filepath not in changed_files:
            yield filepath


# -----------------------------------------------------------------------------
def _replace_all(string_list, old, new):
    """
    Call the string replace function on all strings in a list.

    ---
    type: function

    args:
        string_list:    A list of strings.

        old:            The string to be replaced.

        new:            The string to replace it with.

    returns:
        modified_list:  A list of strings where, for each string
                        in the list, all instances of the old string
                        have been replaced by the new string.
    ...

    """
    return [string.replace(old, new) for string in string_list]


# -----------------------------------------------------------------------------
def _normalise_filepaths(iter_filepaths, build_monitor):
    """
    Yield a sequence of normalised (design document) filepaths.

    Filepaths are normalised by converting filepaths
    for supporting documents into the filepath of
    the design document that they support.

    Duplicates are then removed, leaving a sequence
    of filepaths of design documents which are to
    be included in the build; one for each build
    unit.

    Files which are not design documents or do not
    support a design document (i.e. are not part
    of any build unit) are skipped.

    ---
    type: generator

    args:
        iter_filepaths: An iterable yielding a sequence of filepaths.
                        These filepaths may refer either to primary
                        design documents or to secondary supporting
                        documents such as tests or specifications.

        build_monitor:  A reference to the build monitoring and
                        progress reporting coroutine.

    yields:
        filepath:       A design document filepath. Duplicate
                        filepaths are removed and supporting
                        document filepaths are normalised.
    ...

    """
    deduplication = set()
    for filepath in iter_filepaths:

        # Ignore files for which we cannot determine a design document.
        if (    da.lwc.file.is_test_data(filepath)
             or da.lwc.file.is_test_config(filepath)):
            continue

        # Filepaths of supporting documents are
        # converted into the filepath of the design
        # document that they support. This gives
        # us a string that we can use to identify
        # each unique build unit.
        #
        if da.lwc.file.is_specification_file(filepath):
            filepath_design = da.lwc.file.design_filepath_for(filepath)
            if os.path.isfile(filepath_design):
                filepath = filepath_design
            else:
                build_monitor.report_nonconformity(
                    tool   = 'da.build',
                    msg_id = da.check.constants.BUILD_MISSING_DESIGN_FILE,
                    msg    = 'Missing design file for spec: {path}'.format(
                                                            path = filepath),
                    path   = filepath)

        # Ignore duplicates.
        if filepath in deduplication:
            continue
        else:
            deduplication.add(filepath)
            yield filepath

    return


# -----------------------------------------------------------------------------
def _restrict_filepaths(cfg, iter_filepaths):
    """
    Yield filepaths, skipping those eliminated by any in-force restrictions.

    If no restriction is specified, all supplied
    filespaths are yielded unchanged and in order.

    ---
    type: coroutine

    args:
        cfg:            A mapping holding the build configuration.

        iter_filepaths: An iterable yielding a sequence of design document
                        filepaths.

    yields:
        filepath:       A design document filepath. Filepaths which
                        are excluded by the configuration (cfg) are
                        skipped.
    ...

    """
    restriction = cfg['scope']['restriction']
    if not restriction:
        for filepath in iter_filepaths:
            yield filepath
    else:
        logging.info('Build restriction: %s', restriction)
        dirpath_isolated_src = cfg['paths']['dirpath_isolated_src']
        for filepath in iter_filepaths:
            relpath = os.path.relpath(filepath, dirpath_isolated_src)
            if da.bldcfg.bldcfg.is_in_restricted_build(relpath, restriction):
                yield filepath


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _load_design_doc(cfg, filepath, build_monitor):
    """
    Context manager to load the design document into a build unit.

    ---
    type: context_manager

    args:
        cfg:            A mapping holding the build configuration.

        filepath:       A design document filepath.

        build_monitor:  A reference to the build monitoring and
                        progress reporting coroutine.

    yields:
        build_unit:     A mapping with information about a single
                        detailed design document (source file)
                        together with it's supporting specifications
                        and tests.
    ...

    """
    rootpath_log = cfg['paths']['dirpath_branch_log']

    # TODO: If possible (python >= 3.2) use tokenize.open to open
    #       files, so PEP 263 encoding markers are interpreted.
    #       We will need to go through and update all the processes
    #       that make use of the file handle though ...
    #
    with open(filepath, 'rb') as file:
        content       = file.read().decode('utf-8')
        relpath       = os.path.relpath(filepath,
                                        cfg['paths']['dirpath_isolated_src'])
        (relpath_dir, filename) = os.path.split(relpath)
        dirpath_log             = os.path.join(
                                            rootpath_log,
                                            relpath_dir,
                                            filename.replace('.', '_'))
        build_unit = {
            'filepath':     filepath,
            'relpath':      relpath,
            'file':         file,
            'content':      content,
            'dirpath_log':  dirpath_log
        }

        # Add build_unit['ast'] if file parses OK...
        build_unit = _try_parse(build_unit, build_monitor)

        # Yield with open filepath...
        yield build_unit

    return


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _load_supporting_docs(cfg, build_unit, build_monitor):
    """
    Context manager to load supporting documents into a build unit.

    ---
    type: context_manager

    args:
        cfg:            A mapping holding the build configuration.

        build_unit:     A mapping with information about a single
                        detailed design document (source file)
                        together with it's supporting specifications
                        and tests.

        build_monitor:  A reference to the build monitoring and
                        progress reporting coroutine.

    yields:
        build_unit:     A mapping with information about a single
                        detailed design document (source file)
                        together with it's supporting specifications
                        and tests.
    ...

    """
    filepath             = build_unit['filepath']
    filepath_spec        = da.lwc.file.specification_filepath_for(filepath)
    has_supporting_docs  = (     da.lwc.file.is_design_file(filepath)
                             and os.path.isfile(filepath_spec))

    if has_supporting_docs:
        with open(filepath_spec, 'rb') as file:
            content = file.read().decode('utf-8')
            build_unit['spec'] = {
                'filepath': filepath_spec,
                'relpath':  os.path.relpath(
                                        filepath_spec,
                                        cfg['paths']['dirpath_isolated_src']),
                'file':     file,
                'content':  content
            }

            # Add build_unit['spec']['ast'] if file parses OK...
            build_unit['spec'] = _try_parse(build_unit['spec'], build_monitor)

            # Yield with open filepath_spec...
            yield build_unit

    else:

        yield build_unit

    return


# -----------------------------------------------------------------------------
def _try_parse(build_unit_part, build_monitor):
    """
    Return build_unit_part with added 'ast' field, else report a nonconformity.

    This function attempts to parse the file specified
    by build_unit_part['filepath']. If it is successful,
    it stores the resulting AST in build_unit_part['ast'].
    If it is not successful, it reports a nonconformity
    via the supplied build_monitor reference. In either
    case, a reference to the supplied build_unit_part
    dict is returned.

    The build_unit_part can either be a reference to
    an entire build_unit structure or a reference to
    the build_unit['spec'] part.

    ---
    type: function

    args:

        build_unit_part:    Either a reference to an entire
                            build_unit struct, or a reference
                            to the build_unit['spec'] part.

        build_monitor:      A reference to the build monitoring and
                            progress reporting coroutine.

    returns:

        build_unit_part:    Either a reference to an entire
                            build_unit struct, or a reference
                            to the build_unit['spec'] part.
    ...

    """
    filepath = build_unit_part['filepath']
    if da.lwc.file.is_python_file(filepath):

        try:

            build_unit_part['ast'] = ast.parse(build_unit_part['content'])

        except SyntaxError as err:

            # Draw a caret under the error location
            # so it is easy for the user to spot
            # where the error is.
            #
            idx_newline = str(err.text)[0:int(err.offset)].rfind('\n')
            col = err.offset - (idx_newline + 1)
            location_indicator = (' ' * col) + '^'
            msg = 'Syntax error:\n{msg}\n{loc}'.format(
                                            msg = err.text,
                                            loc = location_indicator)

            build_monitor.report_nonconformity(
                tool   = 'da.build',
                msg_id = da.check.constants.BUILD_SPEC_SYNTAX_ERROR,
                msg    = msg,
                path   = filepath,
                line   = err.lineno,
                col    = col)

    return build_unit_part


# -----------------------------------------------------------------------------
@da.util.coroutine
def _unit_processing(cfg, build_monitor):               # pylint: disable=R0912
    """
    Recieve and process individual build units.

    This coroutine is a key component in the build
    system. It is responsible for the selection,
    configuration and sequencing of those processing
    steps which are applied to individual build
    units. The processing steps themselves are
    implemented as a set of subsidiary coroutines.

    Pylint rule R0912 (too many branches) is disabled
    for this function because the use of if statements
    to apply configuration values feels justified
    and legible and I do not believe that it poses
    any obstacle to either maintenance or test.

    ---
    type: coroutine

    args:
        cfg:            A mapping holding the build configuration.

        build_monitor:  A reference to the build monitoring and
                        progress reporting coroutine.

    yields:
        build_data:     A mapping holding build data accumulated
                        during the preceeding unit processing
                        phase (e.g. incremental index data for
                        reports and traceability).
    ...

    """
    dirpath_src = cfg['paths']['dirpath_isolated_src']
    steps       = cfg['steps']

    chk_pytest  = da.check.pytest.coro(
                                    dirpath_src      = dirpath_src,
                                    build_monitor    = build_monitor)

    chk_pylint  = da.check.pylint.coro(
                                    dirpath_lwc_root = dirpath_src,
                                    build_monitor    = build_monitor)

    chk_pytype  = da.check.pytype.coro(
                                    dirpath_lwc_root = dirpath_src,
                                    build_monitor    = build_monitor)

    indexer     = da.index.index_coro(
                                    dirpath_lwc_root = dirpath_src)

    chk_deps    = da.check.dependencies.coro(
                                    dirpath_lwc_root = dirpath_src,
                                    build_monitor    = build_monitor)

    bld_clang   = da.compile.clang.coro(build_monitor)
    bld_gcc     = da.compile.gcc.coro(build_monitor)
    chk_complex = da.check.pycomplexity.coro(build_monitor)
    chk_data    = da.check.schema.coro(build_monitor)
    chk_pycode  = da.check.pycodestyle.coro(build_monitor)
    chk_pydoc   = da.check.pydocstyle.coro(build_monitor)
    doc_design  = da.docgen.design.coro(cfg)

    report_data = None
    while True:

        build_unit = (yield report_data)

        # We run unit tests first to make the
        # test-modify-test loop as tight as
        # possible.
        if steps['enable_test_python_unittest']:
            chk_pytest.send(build_unit)

        if steps['enable_static_test_python_complexity']:
            chk_complex.send(build_unit)

        if steps['enable_static_test_python_codestyle']:
            chk_pycode.send(build_unit)

        if steps['enable_static_test_python_docstyle']:
            chk_pydoc.send(build_unit)

        # Pylint static analysis and MyPy type
        # checking are the slowest python-specific
        # steps, so we leave them until after the
        # other python-specific stuff.
        if steps['enable_static_test_python_pylint']:
            chk_pylint.send(build_unit)

        if steps['enable_static_test_python_typecheck']:
            chk_pytype.send(build_unit)

        # C/C++ compilation with gcc.
        if steps['enable_compile_gcc']:
            bld_gcc.send(build_unit)

        # C/C++ compilation with clang.
        if steps['enable_compile_clang']:
            bld_clang.send(build_unit)

        # Generate design documentation.
        if steps['enable_generate_design_docs']:
            doc_design.send(build_unit)

        # Data validation has to come before
        # indexing -- perhaps both should be
        # enabled together?
        if steps['enable_static_data_validation']:
            chk_data.send(build_unit)

        # Static indexing... early or late?
        # TODO: Consider switching this on/off with reporting??
        if steps['enable_static_indexing']:
            report_data = indexer.send(build_unit)
        else:
            report_data = None

        chk_deps.send(build_unit)


# -----------------------------------------------------------------------------
def _integrated_processing(cfg,
                           build_monitor,
                           build_data):                 # pylint: disable=R0912
    """
    Carry out build steps which treat the design as an integrated whole.

    This function implements the second major phase
    of the build process. It is responsible for the
    selection, configuration and sequencing of those
    processing steps which are applied to the design
    as an integrated whole. The processing steps
    themselves are implemented as a set of subsidiary
    functions.

    These non-decomposable functions include test
    data integrity checking; report generation and
    the registration of built artifacts with the
    configuration management system.

    ---
    type: function

    args:
        cfg:            A mapping holding the build configuration.

        build_monitor:  A reference to the build monitoring and
                        progress reporting coroutine.

        build_data:     A mapping holding build data accumulated
                        during the preceeding unit processing
                        phase (e.g. incremental index data for
                        reports and traceability).
    ...

    """
    if cfg['steps']['enable_bulk_data_checks']:
        da.check.bulk_data.check_all(cfg, build_monitor)

    if cfg['steps']['enable_report_generation']:
        # Delay importing the report module as it has heavyweight dependencies.
        import da.report as _report
        _report.build(cfg, build_data)

    # Iff the build ran to completion, register artifacts with the local CMS.
    if cfg['options']['enable_cms_registration']:
        da.cms.register(cfg)

    return
