# -*- coding: utf-8 -*-
"""
The metabuild module is responsible for orchestrating collections of builds.

A number of different use-cases are supported.

1.  Build and evaluate a single specified design
    configuration in a controlled evironment.

2.  Build and compare a set of competing design
    configurations.

3.  Optimise design parameters by iteratively
    generating and evaluating novel design
    configurations.

4.  Provide continuous feedback by listening for
    file changes and triggering incremental builds
    that run in the background at low priority.

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

import base64
import collections
import contextlib
import hashlib
import importlib
import logging
import os
import pickle
import shutil
import sys

import tblib
import tblib.pickling_support

import da.bldcfg
import da.constants
import da.log
import da.profiling
import da.register
import da.util
import da.vcs


# tblib enables us to pickle tracebacks so we can
# throw exceptions across process boundaries. This
# allows us to throw an exception in the build
# (sub)process and have it propagate up to the
# the top level metabuild process.
#
tblib.pickling_support.install()


# -----------------------------------------------------------------------------
def main(cfg_key, cfg_extras, dirpath_lwc_root):
    """
    Return COMPLETED if all subsidiary builds complete else throw an Exception.

    This function can be configured to support
    a number of different use-cases:

    1.  Build and evaluate a single specified
        design configuration in a controlled
        evironment.

    2.  Build and compare a set of competing
        design configurations.

    3.  Optimise design parameters by iteratively
        generating and evaluating novel design
        configurations.

    4.  Provide continuous feedback by listening
        for file changes and triggering incremental
        builds that run in the background at low
        priority.

    In all cases, we start by taking a baseline
    of the design configuration in its' initial
    unmodified state. If the build fails for any
    reason, the repository is reverted to this
    state. This behaviour is implemented by the
    da.vcs.rollback_context context manager.

    We then load metabuild configuration from the
    user-specified build restriction configuration
    file. This configuration is applied to all
    subsidiary builds.

    We signal the completion of the build with
    an empty text file in the build directory
    named META_BUILD_COMPLETED.

    """
    cfg = da.bldcfg.load_cfg(cfg_key          = cfg_key,
                             cfg_extras       = cfg_extras,
                             dirpath_lwc_root = dirpath_lwc_root)

    # TODO: WHEN THE ONLINE/CONTINUOUS BUILD SERVICE
    #       IS BEING USED, CONFIGURE THINGS SO THAT
    #       WE DO NOT AUTOCOMMIT AND WE DO NOT ROLL
    #       BACK. THIS SHOULD AVOID CHURNING THE GIT
    #       REPOSITORY UNNECESSARILY...
    #
    with _signal_file_context(cfg):
        with da.vcs.rollback_context(dirpath_root = dirpath_lwc_root):
            _metabuild(cfg, dirpath_lwc_root)

    return da.constants.META_BUILD_COMPLETED


# ------------------------------------------------------------------------------
@contextlib.contextmanager
def _signal_file_context(cfg):
    """
    Manage the META_BUILD_COMPLETED signalling file.

    We want a very reliable method of signalling
    to the developer when the build is complete.

    We do this with an empty text file in the
    temporary directory named
      'META_BUILD_COMPLETED'.

    This file is created at the end of the meta
    build.

    At the start of the meta-build, we must check
    for any such files that have been left by
    previous meta-builds and remove them.

    """
    filepath_complete_flag = os.path.join(cfg['paths']['dirpath_meta_tmp'],
                                          'META_BUILD_COMPLETED')
    if os.path.isfile(filepath_complete_flag):
        os.remove(filepath_complete_flag)
    (yield)
    with open(filepath_complete_flag, 'wb'):
        pass


# -----------------------------------------------------------------------------
def _metabuild(cfg, dirpath_lwc_root):
    """
    Return COMPLETED if all subsidiary builds complete else throw an Exception.

    A number of baselines are used to manage the
    design configuration for the duration of the
    metabuild.

    1. unmodified_baseline  - The state of the
                              repository head when
                              the build command was
                              issued. We leave the
                              repository in this
                              state if an exception
                              occurs.

    2. auto_commit_baseline - The state of the
                              repository head after
                              any changes (staged
                              or unstaged) have
                              been committed.

    3. defined_baseline     - One of a list of
                              system configurations
                              defined in the active
                              build restriction
                              configuration file.

    4. delta_configuration  - A 'delta' system
                              configuration that
                              has been generated
                              by a numerical
                              optimisation algorithm
                              on top of one of the
                              defined baselines.

    """
    dirpath_meta_tmp = cfg['paths']['dirpath_meta_tmp']

    _tmp_dir_cleaning(cfg, dirpath_meta_tmp)

    # Note changed files for incremental builds and build prioritisation.
    cfg['changed_files'] = da.vcs.changed_files(dirpath_lwc_root)

    # Create the auto-commit baseline.
    auto_commit_baseline_id = da.vcs.auto_commit(cfg, dirpath_lwc_root)

    commit_info = da.vcs.commit_info(
                                dirpath_root = dirpath_lwc_root,
                                ref          = auto_commit_baseline_id)
    cfg = da.util.merge_dicts(cfg, { 'auto_commit_baseline': commit_info })

    # We want to be able to perform
    # side-by-side comparisons to evaluate
    # competing design proposals; where
    # each proposed design is optimised
    # and tuned so that the comparison
    # is not confounded by poorly selected
    # design parameters.
    #
    # Proposals are given by the build
    # restriction configuration file as
    # a list of 'defined_baselines'.
    #
    # We process each in turn, generating
    # deltas and optimising as needed.
    #
    for defined_baseline_id in cfg['scope']['defined_baselines']:

        commit_info = da.vcs.commit_info(
                                    dirpath_root = dirpath_lwc_root,
                                    ref          = defined_baseline_id)
        cfg = da.util.merge_dicts(cfg, { 'defined_baseline': commit_info })
        safe_branch_name = _safe_branch_name(commit_info['branch'])
        cfg['safe_branch_name'] = safe_branch_name
        cfg = _set_build_paths(cfg, dirpath_meta_tmp, safe_branch_name)

        # Use the hash code as an absolute
        # identifier for the system configuration
        # under test. Relative references such
        # as "HEAD" or "master" will be different
        # for the repository clone in the isolated
        # temporary build directory and so cannot
        # be used.
        #
        system_configuration_under_test = commit_info['hexsha']

        # Isolate a clean copy of the design
        # documents to be built.
        #
        da.vcs.clone_all_design_documents(
            dirpath_lwc_root    = dirpath_lwc_root,
            dirpath_destination = cfg['paths']['dirpath_isolated_src'],
            configuration       = system_configuration_under_test)

        # TODO: Consider eagerly mounting
        #       "a0_env"; "a2_dat" and "a5_cms"
        #       so that they are in the 'correct'
        #       position relative to the isolated
        #       src directory. Alternatively,
        #       consider using an idempotent
        #       ensure-available function
        #       that mounts resources lazily
        #       (on demand).

        # We want to be able to tune each
        # design proposal using a configurable
        # optimisation algorithm and objective
        # function.
        #
        # Both the optimisation algorithm and
        # the objective function are provided
        # by the "optimisation_module" specified
        # in the configuration, which acts as
        # an adapter to the build function
        # itself. The build function is supplied
        # to the optimisation module as a
        # callback so that the system design
        # may be rebuilt and re-evaluated after
        # each "delta" change.
        #
        optimisation_module = cfg['options']['optimisation_module']
        design_optimisation_enabled = optimisation_module is not None
        if design_optimisation_enabled:

            importlib.import_module(optimisation_module).optimise_build(
                                    _build_and_evaluate_design, cfg)

        # When system design optimisation is not configured, we only
        # need to build the null delta.
        #
        else:

            cfg = _set_build_id(cfg, safe_branch_name)
            _build_and_evaluate_design(cfg)

    # Once the subsidiary builds have finished,
    # each proposal should have an associated
    # 'local' optimum that has been discovered.
    #
    # We can now compare performance across
    # these newly discovered local optima
    # and update the management reporting
    # that looks at development progress
    # over time.
    #
    # We delay importing the report module
    # as it has large dependencies.
    #
    import da.report as _report
    _report.metabuild(cfg)


# -----------------------------------------------------------------------------
def _tmp_dir_cleaning(cfg, dirpath_meta_tmp):
    """
    Delete and recreate the tmp dir if we are configured to do so.

    We can delete and recreate the tmp dir if we
    want to do a clean (full) build.

    """
    if (     cfg['options']['clean_tmp_dir']
         and os.path.isdir(dirpath_meta_tmp)):
        shutil.rmtree(dirpath_meta_tmp)
    da.util.ensure_dir_exists(dirpath_meta_tmp)


# -----------------------------------------------------------------------------
def _safe_branch_name(branch_name):
    """
    Return a sanitised version of the branch name.

    The temporary directory needs to be named after
    the branch, but with some sanitisation so that
    it can safely be used on either Windows or
    Linux. Detecting 'os.sep' characters is not
    good enough in this instance because we may
    need to access the directory from a machine
    other than the one on which it was generated.

    """
    if branch_name is None:
        safe_branch_name = 'detached_head'
    else:
        safe_branch_name = \
                    branch_name.lower().replace('/', '_').replace('\\', '_')
    return safe_branch_name


# -----------------------------------------------------------------------------
def _set_build_paths(cfg, dirpath_meta_tmp, safe_branch_name):
    """
    Update the cfg structure with build-specific paths.

    We want to prevent uncontrolled and unwanted
    files from influencing the build, so rather
    than building 'in-place' in the local working
    copy, we build from a clone that we maintain
    within an isolated temporary build directory.

    To support the possibility of using incremental
    builds, the temporary build directories should
    be the same when the system configurations
    being built are similar, but different
    otherwise.

    We assume that different configurations on the
    same branch are similar enough to permit
    incremental builds to be used.

    """
    dirpath_meta_cms   = cfg['paths']['dirpath_meta_cms']
    dirpath_branch_cms = os.path.join(dirpath_meta_cms, safe_branch_name)
    dirpath_branch_tmp = os.path.join(dirpath_meta_tmp, safe_branch_name)
    dirpath_branch_log = os.path.join(dirpath_branch_tmp, 'log')
    dirpath_branch_src = os.path.join(dirpath_branch_tmp, 'src')
    cfg['paths']['dirpath_branch_cms']   = dirpath_branch_cms
    cfg['paths']['dirpath_branch_tmp']   = dirpath_branch_tmp
    cfg['paths']['dirpath_branch_log']   = dirpath_branch_log
    cfg['paths']['dirpath_isolated_src'] = dirpath_branch_src
    return cfg


# -----------------------------------------------------------------------------
def _set_build_id(cfg, safe_branch_name):
    """
    Update the cfg structure with a build id.

    """
    build_id = '{tbox}.{day}.{utc}.{bld}.{branch}.{hash}'.format(
            tbox   = cfg['timestamp']['timebox_id'],
            day    = cfg['timestamp']['day_of_month'],
            utc    = cfg['timestamp']['short_time_utc'],
            bld    = cfg['cfg_name'],
            branch = safe_branch_name,
            hash   = cfg['defined_baseline']['short_hexsha'])
    cfg['build_id']       = build_id
    cfg['build_codename'] = _mnemonic_codeword(
                                        build_id,
                                        dirpath_lwc_root = None)
    return cfg


# -----------------------------------------------------------------------------
def _mnemonic_codeword(text, dirpath_lwc_root = None):
    """
    Return a mnemonic code word calculated from the hash of a text string.

    """
    name_list = da.register.load('mnemonic',
                                 dirpath_lwc_root = dirpath_lwc_root)
    num_names = len(name_list)
    digest    = hashlib.md5(text.encode('utf-8')).hexdigest()
    codeword  = '_'.join([name_list[int(digest[0:4],  16) % num_names],
                          name_list[int(digest[4:8],  16) % num_names],
                          name_list[int(digest[8:12], 16) % num_names]])
    return codeword


# -----------------------------------------------------------------------------
def _build_and_evaluate_design(cfg):
    """
    Build the "current" design proposal and evaluate its performance.

    """
    # We want to treat the build process as an
    # integrated part of the product, so as soon
    # as we know which system configuration is
    # to be built, we launch a new (sub)process
    # so that the remainder of the build process
    # can be taken from that system configuration.
    #

    # We define a pickle file that we use to record
    # the result of the build and make sure that
    # any old files with the same name have been
    # removed from the temporary directory.
    #
    dirpath_branch_tmp   = cfg['paths']['dirpath_branch_tmp']
    filepath_result      = os.path.join(dirpath_branch_tmp, 'result.pickle')
    cfg['paths']['filepath_result'] = filepath_result
    if os.path.isfile(filepath_result):
        os.remove(filepath_result)

    # We pickle the configuration and base64 encode
    # it so we can send it as a command-line parameter
    # to the build process.
    #
    pickled_cfg = base64.b64encode(
                    pickle.dumps(cfg, protocol = da.constants.PICKLE_PROTOCOL))

    # Call the build in a subprocess.
    #
    # NOTE: We communicate with the subprocess
    #       using pickled data -- so there are
    #       potential security concerns here and
    #       we need to be careful to keep this
    #       data secure.
    #
    dirpath_isolated_src = cfg['paths']['dirpath_isolated_src']
    da.lwc.run.python3(['-m', 'da.metabuild', pickled_cfg],
                       dirpath_lwc_root = dirpath_isolated_src)

    # We expect the subprocess to pickle the
    # results (Exception or success) in our
    # defined results file.
    #
    if not os.path.isfile(filepath_result):
        raise RuntimeError(
            'Could not find result file from subsidiary build process. '
            'It seems to have terminated unexpectedly.')
    with open(filepath_result, 'rb', buffering = 1) as file_result:
        result = pickle.load(file_result)

    # Examine output and raise exception if required.
    if result == da.constants.BUILD_COMPLETED:
        return result
    else:
        (_, exception_value, trace_back) = result

        # We want to be able to open our text editor
        # or IDE at the location where an exception
        # was thrown - but we don't want to open
        # the file *inside* the isolation dir, as
        # our changes will simply be overwritten
        # on the next build. Instead, we want to
        # open the *real* source file in our local
        # working copy.
        #
        # To do this, we re-write the contents of
        # the traceback data structure so that
        # references to the isolated source
        # directory get replaced by references
        # to the "outer" local working copy
        # directory.
        #
        dirpath_outer_lwc_root = cfg['paths']['dirpath_lwc_root']
        trace_back_dict        = tblib.Traceback(trace_back).to_dict()
        for obj in da.util.walkobj(trace_back_dict, gen_leaf    = False,
                                                    gen_nonleaf = True,
                                                    gen_path    = False,
                                                    gen_obj     = True):
            if isinstance(obj, collections.Mapping):
                for key in ('co_filename', '__file__'):
                    if key in obj:
                        obj[key] = obj[key].replace(dirpath_isolated_src,
                                                    dirpath_outer_lwc_root)

        raise exception_value.with_traceback(
                    tblib.Traceback.from_dict(trace_back_dict).as_traceback())


# -----------------------------------------------------------------------------
def run_subsidiary_build(argv = None):
    """
    Decode the build configuration, run the build, then encode the result.

    """
    # We expect a single input argument holding
    # a pickled and base64 encoded representation
    # of the meta-build configuration.
    #
    if argv is None:
        argv = sys.argv
    cfg = pickle.loads(base64.b64decode(argv[1]))

    # The constant da.constants.BUILD_COMPLETED is
    # returned if the build is succesful. Otherwise,
    # a pickled exception object is returned.
    #
    try:

        enable_build_profiling = cfg['options']['enable_build_profiling']
        dirpath_branch_log     = cfg['paths']['dirpath_branch_log']
        with da.profiling.context(enable          = enable_build_profiling,
                                  dirpath_bld_log = dirpath_branch_log):

            # Configure logging and log our configuration.
            # We log the configuration right at the
            # beginning so that if something goes
            # wrong we at least have some information
            # upon which we may base our post-mortem
            # investigations.
            #
            # TODO: We should implement a mechanism
            #       so that we can pass a config.log.json
            #       file into the build system and
            #       have it attempt to reproduce the
            #       build.
            #
            dirpath_branch_log = cfg['paths']['dirpath_branch_log']
            loglevel_overall   = cfg['options']['loglevel_overall']
            loglevel_console   = cfg['options']['loglevel_console']
            loglevel_file      = cfg['options']['loglevel_file']
            da.log.configure(
                dirpath_log      = dirpath_branch_log,
                loglevel_overall = logging.getLevelName(loglevel_overall),
                loglevel_console = logging.getLevelName(loglevel_console),
                loglevel_file    = logging.getLevelName(loglevel_file))

            # We call the dependencies build as early
            # as possible because we want to minimise
            # the number of dependencies that have
            # to be satisfied before it can run.
            #
            # This approach makes it easier to bootstrap
            # the build on a new platform (Reduces
            # the number of dependencies that need
            # to be built manually), and also reduces
            # the risk of us irretreivably breaking
            # the build system if we accidentally
            # lose a dependency for whatever reason.
            #
            options = cfg['options']
            steps   = cfg['steps']
            if (steps['enable_dep_fetch_src']) or (steps['enable_dep_build']):
                import da.dep as _dep
                dep_build_cfg    = {
                    'enable_dep_fetch_src':  steps['enable_dep_fetch_src'],
                    'enable_dep_build':      steps['enable_dep_build'],
                    'exclusion':             options['dep_build_exclusion'],
                    'limitation':            options['dep_build_limitation']}
                _dep.build(
                    dirpath_lwc_root = cfg['paths']['dirpath_lwc_root'],
                    dirpath_log      = dirpath_branch_log,
                    dep_build_cfg    = dep_build_cfg)

            # Only import build if we are doing a build -- this allows us to
            # minimise / reduce dependencies.
            if steps['enable_main_build']:
                import da.build as _build
                result = _build.main(cfg = cfg)
            else:
                result = da.constants.BUILD_COMPLETED

    # Pylint rule W0703 (broad-except) disabled. All
    # Exception objects are caught because keeping
    # an explicit list of exception classes is not
    # practical given the evolving and low-maturity
    # nature of much of the software that will be
    # doing the throwing.
    #
    except Exception:                                   # pylint: disable=W0703
        result = sys.exc_info()

    # We expect the result to either be da.constants.BUILD_COMPLETED (0)
    # or an instance of an exception class.
    #
    # We write the serialised result to a temporary
    # file so that the metabuild process can rethrow
    # any exceptions raised in this process.
    #
    # We are not using stdout for this inter-process
    # communication because many of the various
    # third-party build tools that we will be
    # launching will need to use stdout for their
    # own HMI display, so I don't want to redirect
    # it or screw with it in any way. (py.test does
    # some pretty advanced stuff to stdout -- which
    # I especially do not wish to screw with in
    # any way).
    #
    filepath_result = cfg['paths']['filepath_result']
    with open(filepath_result, 'wb', buffering = 1) as file_result:
        pickle.dump(
                result, file_result, protocol = da.constants.PICKLE_PROTOCOL)
    return 0


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(run_subsidiary_build())
