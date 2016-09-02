# -*- coding: utf-8 -*-
"""
Build operations.

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
import itertools
import json
import logging
import os

import click

import da.bldcfg
import da.check.pycodestyle
import da.check.pydocstyle
import da.check.pylint
import da.check.pytest
import da.check.pycomplexity
import da.check.schema
import da.cms
import da.compile.clang
import da.compile.gcc
import da.constants
import da.dep
import da.docgen.api
import da.docgen.design
import da.exception
import da.index
import da.log
import da.lwc
import da.lwc.file
import da.team


# -----------------------------------------------------------------------------
@da.log.trace
def main(cfg):
    """
    Run a build and return the resulting status code.

    The build.main() function is responsible for top level control over
    the build process. The build process takes as input a set of design
    documents and produces as output a set of artifacts.

    The build.main() function can be configured to restrict the set of
    design documents used as build inputs as well as the processing steps
    applied to them.

    In this way we can restrict the build to selected products or components,
    and can apply only the specific processing steps that we choose, which
    enables us to get rapid feedback on areas that are giving us problems.

    The _build_inputs() generator function selects design documents from
    the current configuration and sequences them to detect nonconformities
    as early as possible.

    The _build_process() coroutine selects the processing steps applied
    by the build and and sequences them to detect nonconformities as early
    as possible.

    Errors and nonconformities are handled by the _error_handler coroutine,
    which contains logic for selcting between Jidoka (fail-fast) or robust
    (comprehensive reporting) nonconformity response strategies.

    ---
    type: function
    args:
        cfg: A mapping holding the build configuration.
    ...
    """
    _log_build_configuration(cfg)

    build_monitor = _build_monitor(cfg)
    error_handler = _error_handler(cfg)
    build_inputs  = _build_inputs(cfg)
    build_process = _build_process(cfg, error_handler)
    build_data    = None

    # Pass design documents through the build process.
    for build_element in build_inputs:
        build_monitor.send(build_element)
        build_data = build_process.send(build_element)

    # Delay importing report module as it has large dependencies.
    if cfg['steps']['enable_report_generation']:
        import da.report as _report
        _report.build(cfg, build_data)
        error_handler.send('PHASE_END')

    # Iff the build ran to completion, register artifacts with the local CMS.
    if cfg['options']['enable_cms_registration']:
        da.cms.register(cfg)

    error_handler.send('BUILD_END')
    build_monitor.send('BUILD_END')
    logging.debug('Build process ran to completion')

    return da.constants.BUILD_COMPLETED


# -----------------------------------------------------------------------------
def _build_inputs(cfg):
    """
    Yield filtered and prioritised build elements.

    Each build element consists of a single design document
    plus all of it's supporting documents: specifications,
    tests, header files and so on.

    Build elements are selected and prioritised based on
    when they were last modified and by the assessed risk
    of a nonconformity or error.

    The build can be configured to limit the build elements
    that are generated so that only particular products or
    projects are built.

    Yielded build elements will often include open file
    handles. This generator ensures that each of these
    handles will be closed at the end of each iteration.

    """
    iter_prioritised = _gen_prioritised_filepaths(cfg)
    iter_normalised  = _normalise_filepaths(iter_prioritised)
    iter_restricted  = _restrict_filepaths(cfg, iter_normalised)
    for filepath_design_doc in iter_restricted:
        with _load_design_doc(cfg, filepath_design_doc) as part_loaded:
            with _load_supporting_docs(cfg, part_loaded) as build_element:
                yield build_element


# -----------------------------------------------------------------------------
def _gen_prioritised_filepaths(cfg):
    """
    Yield a sequence of candidate build input filepaths in priority order.

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

    """
    return [string.replace(old, new) for string in string_list]


# -----------------------------------------------------------------------------
def _normalise_filepaths(iter_filepaths):
    """
    Yield a sequence of normalised (design document) filepaths.

    Filepaths are normalised by converting filepaths for supporting documents
    into the filepath of the design document that they support.

    Duplicates are then removed, leaving a sequence of filepaths of design
    documents which are to be included in the build; one for each build
    element.

    Files which are not design documents or do not support a design document
    (i.e. are not part of any build element) are skipped.

    """
    deduplication = set()
    for filepath in iter_filepaths:

        # Ignore files for which we cannot determine a design document.
        if (    da.lwc.file.is_test_data(filepath)
             or da.lwc.file.is_test_config(filepath)):
            continue

        # Filepaths of supporting documents are converted into the filepath of
        # the design document that they support. This gives us a string that
        # we can use to identify each unique build element.
        if da.lwc.file.is_specification_file(filepath):
            filepath = da.lwc.file.design_filepath_for(filepath)

        # Ignore duplicates.
        if filepath in deduplication:
            continue
        else:
            deduplication.add(filepath)
            yield filepath


# -----------------------------------------------------------------------------
def _restrict_filepaths(cfg, iter_filepaths):
    """
    Yield filepaths, skipping those eliminated by any in-force resrtrictions.

    If no restriction is specified, all supplied filespaths are yielded
    unchanged and in order.

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
def _load_design_doc(cfg, filepath):
    """
    Context manager to load the design document into a build element.

    """
    rootpath_log = cfg['paths']['dirpath_branch_log']

    # TODO: If possible (python >= 3.2) use tokenize.open to open
    #       files, so PEP 263 encoding markers are interpreted.
    #       We will need to go through and update all the processes
    #       that make use of the file handle though ...
    with open(filepath, 'rb') as file:
        content       = file.read().decode('utf-8')
        relpath       = os.path.relpath(filepath,
                                        cfg['paths']['dirpath_isolated_src'])
        dirpath_log   = os.path.join(rootpath_log,
                                     os.path.splitext(relpath)[0])
        build_element = {
            'filepath':     filepath,
            'relpath':      relpath,
            'file':         file,
            'content':      content,
            'dirpath_log':  dirpath_log
        }

        if da.lwc.file.is_python_file(filepath):
            build_element['ast'] = ast.parse(content)

        yield build_element


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _load_supporting_docs(cfg, build_element):
    """
    Context manager to load supporting documents into a build element.

    """
    filepath             = build_element['filepath']
    filepath_spec        = da.lwc.file.specification_filepath_for(filepath)
    has_supporting_docs  = (     da.lwc.file.is_design_file(filepath)
                             and os.path.isfile(filepath_spec))

    if has_supporting_docs:
        with open(filepath_spec, 'rb') as file:
            content = file.read().decode('utf-8')
            build_element['spec'] = {
                'filepath': filepath_spec,
                'relpath':  os.path.relpath(
                                        filepath_spec,
                                        cfg['paths']['dirpath_isolated_src']),
                'file':     file,
                'content':  content
            }
            if da.lwc.file.is_python_file(filepath_spec):
                build_element['spec']['ast'] = ast.parse(content)
            yield build_element

    else:
        yield build_element


# -----------------------------------------------------------------------------
@da.util.coroutine
def _build_process(cfg, error_handler):                 # pylint: disable=R0912
    """
    Configure and return the build function (a closure).

    Build steps are implemented as coroutines, all of which are initialised
    when the _build_process() function is called at the start of the build
    process.

    This function returns a closure, _build_function(), which has access to
    all of the initialised build steps.

    When called with a build_element argument, _build_function()
    will pass the build_element to each of the build steps in turn,
    allowing the build element to be validated, documented and compiled.

    Most build_elements represent individual units and their associated
    tests, but some will also represent subsystems and systems at less
    fine-grained levels of integration.

    Pylint rule R0912 (too many branches) is disabled for this function
    because the use of if statements to apply configuration values feels
    justified and legible and I do not believe that it poses any obstacle
    to either maintenance or test.

    """
    dirpath_src = cfg['paths']['dirpath_isolated_src']
    steps       = cfg['steps']

    chk_pytest  = da.check.pytest.coro(
                                    dirpath_src      = dirpath_src,
                                    error_handler    = error_handler)

    chk_pylint  = da.check.pylint.coro(
                                    dirpath_lwc_root = dirpath_src,
                                    error_handler    = error_handler)

    indexer     = da.index.index_coro(
                                    dirpath_lwc_root = dirpath_src)

    chk_data    = da.check.schema.coro(error_handler)
    chk_complex = da.check.pycomplexity.coro(error_handler)
    chk_pycode  = da.check.pycodestyle.coro(error_handler)
    chk_pydoc   = da.check.pydocstyle.coro(error_handler)
    doc_design  = da.docgen.design.coro(cfg, error_handler)
    doc_api     = da.docgen.api.coro(error_handler)
    bld_gcc     = da.compile.gcc.coro(error_handler)
    bld_clang   = da.compile.clang.coro(error_handler)

    report_data = None
    while True:

        build_element = (yield report_data)

        # We run unit tests first to make the
        # test-modify-test loop as tight as
        # possible.
        if steps['enable_test_python_unittest']:
            chk_pytest.send(build_element)

        if steps['enable_static_test_python_complexity']:
            chk_complex.send(build_element)

        if steps['enable_static_test_python_codestyle']:
            chk_pycode.send(build_element)

        if steps['enable_static_test_python_docstyle']:
            chk_pydoc.send(build_element)

        # Pylint is the slowest python-specific step,
        # so we leave it until last.
        if steps['enable_static_test_python_pylint']:
            chk_pylint.send(build_element)

        # C/C++ compilation with gcc.
        if steps['enable_compile_gcc']:
            bld_gcc.send(build_element)

        # C/C++ compilation with clang.
        if steps['enable_compile_clang']:
            bld_clang.send(build_element)

        # Docco style literate documentation.
        if steps['enable_docgen_design']:
            doc_design.send(build_element)

        # Sphinx/Doxygen style API documentation.
        if steps['enable_docgen_api']:
            doc_api.send(build_element)

        # Data validation has to come before
        # indexing -- perhaps both should be
        # enabled together?
        if steps['enable_static_data_validation']:
            chk_data.send(build_element)

        # Static indexing comes quite early
        # TODO: Consider switching this on/off with reporting??
        if steps['enable_static_indexing']:
            report_data = indexer.send(build_element)
        else:
            report_data = None

        error_handler.send('PHASE_END')


# -----------------------------------------------------------------------------
def cfgserialiser(obj):
    """
    JSON Serialiser for CFG objects.

    This function is used by json.dump to serialise
    build configuration data. It is required because
    the build configuration data structure contains
    datetime objects which are not supported by the
    standard JSON serialiser function.

    """
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError


# -----------------------------------------------------------------------------
@da.util.coroutine
def _build_monitor(cfg):
    """
    Coroutine to handle build monitoring and progress reporting.

    This coroutine is responsible for updating dashboards and other
    progress reporting mechanisms.

    """
    dirpath_branch_log    = cfg['paths']['dirpath_branch_log']
    filepath_build_report = os.path.join(dirpath_branch_log, 'index.html')
    url_build_report      = 'file://{filepath}'.format(
                                            filepath = filepath_build_report)
    da.util.ensure_dir_exists(dirpath_branch_log)

    # Print a hyperlink so we can go look at the log files.
    click.clear()
    _msg('Build id:',    cfg['build_id'])
    _msg('Last commit:', cfg['defined_baseline']['commit_summary'])
    _msg('Report:',      url_build_report)

    # TODO: Get estimate from some sort of cache ...
    est_num_elem  = 115

    # TODO: Configure progressbar on/off
    with open(filepath_build_report, 'wt') as file_build_report:
        file_build_report.write('<html>\n')
        file_build_report.write('<head>\n')
        file_build_report.write('</head>\n')
        file_build_report.write('<body>\n')

    with click.progressbar(length = est_num_elem,
                           label = _pad_key('Progress:')) as progressbar:

        ielement = 0
        for ielement in itertools.count(0):

            progressbar.update(1)
            build_element = (yield)
            if build_element == 'BUILD_END':
                break

            relpath = build_element['relpath']
            with open(filepath_build_report, 'at') as file_build_report:
                file_build_report.write(relpath + '<br>\n')
            os.sync()

    # Finalise
    with open(filepath_build_report, 'at') as file_build_report:
        file_build_report.write('</body>\n')
        file_build_report.write('</html>\n')
    if ielement > est_num_elem:
        raise RuntimeError(
            'Est. num. build elem. {est} < {act} (actual)'.format(
                                                est = est_num_elem,
                                                act = ielement))
    os.sync()
    start_time = cfg['timestamp']['datetime_utc']
    end_time   = datetime.datetime.utcnow()
    delta_secs = (end_time - start_time).total_seconds()
    _msg('Completed in:', '{secs:0.0f}s.'.format(secs = delta_secs))

    # Suppress StopIteration...
    _ = (yield)


# -----------------------------------------------------------------------------
def _msg(key, value = None):
    """
    Write a key: value pair to the console.

    """
    print('{key}  {value}'.format(key   = _pad_key(key),
                                  value = value if value else ''))


# -----------------------------------------------------------------------------
def _pad_key(key):
    """
    Return a key string padded out to 15 characters.

    """
    return '{key:14s}'.format(key = key)


# -----------------------------------------------------------------------------
def _log_build_configuration(cfg):
    """
    Log the build configuration to a file.

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


# -----------------------------------------------------------------------------
@da.util.coroutine
def _error_handler(cfg):
    """
    Coroutine to handle errors and nonconformities identified during the build.

    This coroutine is responsible for deciding how the build process should
    respond to errors, and enables us to configure either a fail-fast policy
    (the first error terminates the build) or a robust policy (Waiting until
    either the end of the current build phase or the end of the entire build
    before failing).

    The coroutine expects to be sent either error items or control messages.

    Error items are dicts containing information about the error. If the
    system has been configured with a fail-fast policy, then the first error
    will terminate the build. Otherwise, the errors are accumulated in a list
    until the appropriate time for them to be collectively processed.

    Control messages are strings, either 'PHASE_END' or 'BUILD_END'. The
    receipt of a control message may trigger the termination of the build
    if the build is so configured.

    """
    errors = []
    while True:
        msg = (yield)
        if msg == 'PHASE_END':
            if errors and cfg['options']['errors_abort_at_phase_end']:
                _log_and_abort(cfg, errors)
            else:
                pass  # Silently consume PHASE_END message.

        elif msg == 'BUILD_END':
            if errors and cfg['options']['errors_abort_at_build_end']:
                _log_and_abort(cfg, errors)
            else:
                pass  # Silently consume BUILD_END message.

        else:
            errors.append(msg)
            if cfg['options']['errors_abort_immediately']:
                _log_and_abort(cfg, errors)


# -----------------------------------------------------------------------------
def _log_and_abort(cfg, errors):
    """
    Log every error in the list and raise an exception.

    """
    # TODO: LOG ERROR IN A FILE SOMEWHERE
    # Translate path strings from isolation-dir strings to their original
    # locations.
    message = ''
    for err in errors:
        filepath_raw = err['file']
        filepath_mod = filepath_raw.replace(
                                        cfg['paths']['dirpath_isolated_src'],
                                        cfg['paths']['dirpath_lwc_root'])
        message += ('{tool}:{msg_id}: {msg:40s} - {file}:{line}\n'.format(
            tool    = err['tool'],
            msg_id  = err['msg_id'],
            msg     = err['msg'],
            file    = filepath_mod,
            line    = err['line']))

    filepath_raw = errors[0]['file']
    filepath_mod = filepath_raw.replace(
                                    cfg['paths']['dirpath_isolated_src'],
                                    cfg['paths']['dirpath_lwc_root'])
    raise da.exception.AbortWithoutStackTrace(message     = message,
                                              filepath    = filepath_mod,
                                              line_number = errors[0]['line'])
