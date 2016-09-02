# -*- coding: utf-8 -*-
"""
Dependency management functions.

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
import shutil
import subprocess

import da.exception
import da.log
import da.lwc
import da.lwc.discover
import da.lwc.env
import da.lwc.run
import da.util


# -----------------------------------------------------------------------------
@da.log.trace
def build(dirpath_lwc_root, dirpath_log, dep_build_cfg):
    """
    Build dependencies for the current runtime environment.

    For all dependencies that support it, build executables
    that are compatible with the current runtime environment.

    """
    limitation = dep_build_cfg['limitation']
    exclusion  = dep_build_cfg['exclusion']

    # Not all dependencies are captured in the dependencies_register.
    # To the best of my knowledge, the host environment will also need
    # the python-dev package; lxml; and lapack/blas installed. Maybe
    # others too that I am not aware of.
    #
    # As soon as we get our virtualisation solution working we will have
    # to do some experiments and see if we can get a truly external-dependency
    # free build.
    #
    register   = da.lwc.env.dependencies_register(
                                        dirpath_lwc_root = dirpath_lwc_root)
    keylist = sorted(register.keys())
    keylist.remove('setuptools')
    keylist.insert(0, 'setuptools')

    for key in keylist:

        # Skip dependency module if it matches our exclusion criteria.
        if (exclusion is not None) and re.match(exclusion, key):
            continue

        # Skip dependency module if it does not match our limitation criteria.
        if (limitation is not None) and (not re.match(limitation, key)):
            continue

        if dep_build_cfg['enable_dep_fetch_src']:
            logging.debug('Fetch source for: %s', key)
            _fetch_dependency_source_files(register[key])

        if dep_build_cfg['enable_dep_build']:
            logging.debug('Build: %s', key)
            _build_dependency(register[key], dirpath_log, dirpath_lwc_root)

    # Log missing configuration and documentation
    # dirpath_env    = da.lwc.discover.path('env')
    # dirpath_depsrc = os.path.join(dirpath_env, 'src')
    # dirpath_depdoc = os.path.join(dirpath_env, 'doc')
    # cfg_set = set(keylist)
    # src_set = set((name for (name, _) in da.util.iter_dirs(dirpath_depsrc)))
    # doc_set = set((name for (name, _) in da.util.iter_dirs(dirpath_depdoc)))
    # for name in src_set - cfg_set:
    #     logging.warn('No cfg for: ' + name)
    # for name in src_set - doc_set:
    #     logging.warn('No doc for: ' + name)
    return


# -----------------------------------------------------------------------------
@da.log.trace
def _fetch_dependency_source_files(dep):
    """
    Fetch and update source files for the specified dependency.

    Makes sure that the source design documents for the specified
    dependency comply with the version specified in the env.depmap.json
    configuration file.

    """
    if dep['config']['method'] == 'manual':
        return

    version = _get_version(dep)

    configuration_tool = dep['config']['tool']
    if configuration_tool == 'git':

        import git
        import da.vcs as _vcs  # Rename to prevent conflict w/outer da import.
        try:

            da.util.ensure_dir_exists(dep['dirpath_src'])
            _vcs.delete_untracked_files(dep['dirpath_src'])
            _vcs.ensure_cloned(dirpath_local = dep['dirpath_src'],
                               url_remote    = dep['config']['url'],
                               ref           = version)
        except git.GitCommandError:
            logging.warning('Attempt to fetch failed for: %s', dep['name'])
        except AssertionError as error:
            logging.error('Failed to configure %s', dep['name'])
            raise error

    elif configuration_tool == 'darcs':
        raise RuntimeError(
            'Darcs auto-checkout not yet supported')

    elif configuration_tool == 'hg':
        raise RuntimeError(
            'Mercurial auto-checkout not yet supported')

    elif configuration_tool == 'svn':
        raise RuntimeError(
            'Subversion auto-checkout not yet supported')

    elif configuration_tool == 'manual':
        raise RuntimeError(
            'Cannot auto-checkout unless a tool is specified.')

    else:
        raise RuntimeError(
            'Did not recognise auto-checkout tool for {dep}'.format(dep = dep))


# -----------------------------------------------------------------------------
@da.log.trace
def _get_version(dep):
    """
    Return the version of the dependency to build.

    """
    policy = dep['policy']
    is_fixed_version = policy.startswith('ver_')
    if is_fixed_version:
        policy_parts = policy.split('_')
        version = policy_parts[1]
        return version

    # TODO: Automatic dependency upgrades.
    #
    # At the moment, we only handle a single policy type for our dependencies:
    # downloading and building a user-defined version. In the future, we may
    # wish to automate the process of upgrading dependencies by downloading
    # and building the latest release (lexicograpically largest vcs tag that
    # is formatted like an x.y.z semantic version number); or even the latest
    # commit from a specified branch.
    #
    # Suggested policy naming convention:
    #   - latest_<BRANCH_NAME>      - Most recent commit on specified branch.
    #   - greatest_semver_tag       - Tag with highest ranked semantic version.
    #   - greatest_<MAJOR>.<MINOR>  - Tag with highest version in MAJOR.MINOR.


# -----------------------------------------------------------------------------
@da.log.trace
def _build_dependency(dep, dirpath_log, dirpath_lwc_root):
    """
    Construct the dependency from its design documents.

    """
    if dep['build']['method'] == 'manual':
        logging.debug('Manual build. (Skip)')
        return

    elif dep['build']['tool'] == 'python_distutils':
        logging.debug('Build python library using distutils')
        _build_python_library(
                    dep              = dep,
                    dirpath_log      = dirpath_log,
                    extra_args       = None,
                    dirpath_lwc_root = dirpath_lwc_root)

    elif dep['build']['tool'] == 'python_setuptools':
        logging.debug('Build python library using setuptools')
        _build_python_library(
                    dep              = dep,
                    dirpath_log      = dirpath_log,
                    extra_args       = ['--single-version-externally-managed'],
                    dirpath_lwc_root = dirpath_lwc_root)

    # Commands to build CMAKE:
    # ./bootstrap --no-qt-gui
    #             --prefix={OUTPUT_DIR}
    #             --datadir=data
    #             --docdir=doc
    #             --mandir=man
    #             --xdgdatadir=xdg && make && make install

    else:
        raise RuntimeError(
                    'Did not recognise build tool for {dep}'.format(
                                                                dep = dep))


# -----------------------------------------------------------------------------
@da.log.trace
def _build_python_library(dep, dirpath_log, extra_args, dirpath_lwc_root):
    """
    Build the specified application or library using distutils. (Python 2 & 3).

    """
    # Path to dependency source files
    dirpath_src = dep['dirpath_src']

    # Path to root of environment & version specific dependency folder
    dirpath_dep = dep['dirpath_dep']

    # Ensure that the log directory exists
    if not os.path.isdir(dirpath_log):
        os.makedirs(dirpath_log)

    # Ensure that we are performing a clean build by removing the temporary
    # in-source build directory that is created by distutils by default.
    dirpath_build = os.path.join(dirpath_src, 'build')
    if os.path.isdir(dirpath_build):
        logging.debug('Remove previous temporary build directory.')
        shutil.rmtree(dirpath_build)

    # Ensure that the setup.py script is present.
    dep_id = dep['name']
    filepath_setup_script = os.path.join(dirpath_src, 'setup.py')
    if not os.path.isfile(filepath_setup_script):
        raise RuntimeError(
                'Could not find setup script for {dep}: {path}'.format(
                                        dep  = dep_id,
                                        path = filepath_setup_script))

    for interface in ('lib_python2', 'lib_python3'):
        logging.debug('Attempt to build python interface: %s', interface)
        if interface not in dep['iface']:
            continue
        if interface == 'lib_python2':
            python_fcn = da.lwc.run.python2
        elif interface == 'lib_python3':
            python_fcn = da.lwc.run.python3

        # If we already have files in the output directory, remove them so that
        # we may reduce the risk of unwanted files contaminating our output.
        dirpath_dst = os.path.join(dirpath_dep, dep['path'][interface])
        if os.path.isdir(dirpath_dst):
            logging.debug('Remove previous installation directory.')
            shutil.rmtree(dirpath_dst)
        if os.path.isdir(dirpath_dst):
            raise RuntimeError(
                'Failed to remove previous installation dir: {dir}'.format(
                                                            dir = dirpath_dst))
        os.makedirs(dirpath_dst)

        log_files = _prep_log_files(dirpath_log, dep_id, interface)

        # Select the right python binary to use.
        logging.debug('Build & install %s to: %s', dep_id, dirpath_dst)

        _call_python_build_command(python_fcn,
                                   filepath_setup_script,
                                   dirpath_src,
                                   dirpath_dst,
                                   extra_args,
                                   log_files,
                                   dirpath_lwc_root)

    # Once we are finished, we remove the (temporary) build sub-directory in
    # order that we may return the source tree back to the state in which we
    # found it.
    _remove_temp_dir_or_throw(dirpath_build)

    # Calculate checksum of input files.
    # Calculate checksum of output files.
    # Get semantic version of input files from repo.
    # Get version ID of input files from repo.


# -----------------------------------------------------------------------------
@da.log.trace
def _prep_log_files(dirpath_log, dep_id, interface):
    """
    Return a tuple of build log filepaths.

    Ensure that the files don't exist (to prevent congusion with previous
    builds.)

    """
    # Delete old log-files (if any exist) so we won't be confused or
    # misled by them.
    filepath_log_stderr = os.path.join(dirpath_log,
                                '{dep}.{iface}.stderr.log'.format(
                                                        dep   = dep_id,
                                                        iface = interface))

    filepath_log_stdout = os.path.join(dirpath_log,
                                '{dep}.{iface}.stdout.log'.format(
                                                        dep   = dep_id,
                                                        iface = interface))

    filepath_log_files  = os.path.join(dirpath_log,
                                '{dep}.{iface}.install_files.log'.format(
                                                        dep   = dep_id,
                                                        iface = interface))

    if os.path.isfile(filepath_log_stderr):
        os.unlink(filepath_log_stderr)

    if os.path.isfile(filepath_log_stdout):
        os.unlink(filepath_log_stdout)

    if os.path.isfile(filepath_log_files):
        os.unlink(filepath_log_files)

    return (filepath_log_stderr, filepath_log_stdout, filepath_log_files)


# -----------------------------------------------------------------------------
@da.log.trace
def _call_python_build_command(python_fcn,              # pylint: disable=R0913
                               filepath_setup_script,
                               dirpath_src,
                               dirpath_dst,
                               extra_args,
                               log_files,
                               dirpath_lwc_root):
    """
    Call the python build command.

    """
    (filepath_log_stderr, filepath_log_stdout, filepath_log_files) = log_files
    try:
        with open(filepath_log_stderr, 'w') as fp_stderr_log:
            with open(filepath_log_stdout, 'w') as fp_stdout_log:

                # TODO: WRITE THE COMMAND TO A LOG FILE SO WE CAN REPRODUCE
                # TODO: SPEND SOME MORE TIME THINKING ABOUT HOW THE CONCEPT
                #       OF INTERFACES INTERSECTS WITH SETUPTOOLS CONCEPTS

                # python setup.py config --with-includepath=/path/includes/

                build_command = [
                    filepath_setup_script,
                    'install',
                    '--record='           + filepath_log_files,
                    '--install-base='     + dirpath_dst,
                    '--install-platbase=' + dirpath_dst,
                    '--install-purelib='  + dirpath_dst,
                    '--install-platlib='  + dirpath_dst,
                    '--install-scripts='  + dirpath_dst,
                    '--install-headers='  + dirpath_dst,
                    '--install-data='     + dirpath_dst]
                if extra_args is not None:
                    build_command = build_command + extra_args

                logging.debug('Build: ' + ' '.join(build_command))
                python_fcn(
                        build_command,
                        cwd              = dirpath_src,
                        stdout           = fp_stdout_log,
                        stderr           = fp_stderr_log,
                        dirpath_lwc_root = dirpath_lwc_root)

    # If there was an error, tell the developer.
    except subprocess.CalledProcessError as err:
        raise da.exception.AbortWithoutStackTrace(
            message     = 'Dependency build failed:\n{msg}'.format(
                                                        msg = str(err)),
            filepath    = filepath_log_stderr,
            line_number = -1)


# -----------------------------------------------------------------------------
@da.log.trace
def _remove_temp_dir_or_throw(dirpath):
    """
    Delete the specified directory or throw if the deletion attempt failed.

    """
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)

    if os.path.isdir(dirpath):
        raise RuntimeError(
            'Failed to delete temporary directory: {dir}'.format(
                                                        dir = dirpath))
