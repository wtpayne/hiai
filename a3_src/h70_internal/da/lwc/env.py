# -*- coding: utf-8 -*-
"""
Local working copy runtime environment control.

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
import platform

import da.lwc.discover
import da.register


# -----------------------------------------------------------------------------
def api_path(dependency_id,
             iface_name       = 'lib_python3',
             register         = None,
             dirpath_lwc_root = None):
    """
    Return the path to the specified api.

    """
    return _iface_path(
                dependency_id    = dependency_id,
                iface_type       = 'api',
                iface_name       = iface_name,
                register         = register,
                dirpath_lwc_root = dirpath_lwc_root)


# -----------------------------------------------------------------------------
def cli_path(dependency_id,
             application_name,
             register         = None,
             dirpath_lwc_root = None):
    """
    Return the path to the specified cli binary.

    """
    return _iface_path(
                dependency_id    = dependency_id,
                iface_type       = 'cli',
                iface_name       = application_name,
                register         = register,
                dirpath_lwc_root = dirpath_lwc_root)


# -----------------------------------------------------------------------------
def gui_path(dependency_id,
             application_name,
             register         = None,
             dirpath_lwc_root = None):
    """
    Return the path to the specified gui binary.

    """
    return _iface_path(
                dependency_id    = dependency_id,
                iface_type       = 'gui',
                iface_name       = application_name,
                register         = register,
                dirpath_lwc_root = dirpath_lwc_root)


# -----------------------------------------------------------------------------
def _iface_path(dependency_id,
                iface_type,
                iface_name,
                register         = None,
                dirpath_lwc_root = None):
    """
    Return the path for the specified interface type and dependency id.

    """
    if register is None:
        register = dependencies_register(
                                    dirpath_lwc_root = dirpath_lwc_root)

    try:
        dependency_data = register[dependency_id]
    except KeyError:
        raise RuntimeError(
                'Could not identify dependency: "{dep}".'.format(
                                                        dep = dependency_id))

    dirpath_env = da.lwc.discover.path('current_env',
                                       dirpath_lwc_root = dirpath_lwc_root)

    try:
        relpath_cli = dependency_data[iface_type][iface_name]
    except KeyError:
        raise RuntimeError(
            'Dependency "{dep}" has no {type} with "{name}".'.format(
                                                        dep  = dependency_id,
                                                        type = iface_type,
                                                        name = iface_name))

    return os.path.normpath(os.path.join(dirpath_env,
                                         dependency_data['dirname'],
                                         dependency_data['policy'],
                                         relpath_cli))


# -----------------------------------------------------------------------------
@da.memo.var
def dependencies_register(dirpath_lwc_root = None):
    """
    Return information about the location of dependencies.

    """
    # Add some calculated file-paths to the dependency map.
    dirpath_curr_env = da.lwc.discover.path('current_env', dirpath_lwc_root)
    rootpath_env     = da.lwc.discover.path('env',         dirpath_lwc_root)
    rootpath_env_src = os.path.join(rootpath_env, 'src')
    register         = da.register.load('dependencies')
    for (key, dep) in register.items():
        dirname_dep = dep['dirname']
        dirname_pol = dep['policy']
        dirpath_src = os.path.join(rootpath_env_src, dirname_dep, dirname_pol)
        dirpath_dep = os.path.join(dirpath_curr_env, dirname_dep, dirname_pol)
        register[key]['name']        = key
        register[key]['dirpath_src'] = dirpath_src
        register[key]['dirpath_dep'] = dirpath_dep

    return register


# -----------------------------------------------------------------------------
# TODO: Refactor to reduce number of branches.
#       (Rule disabled to facilitate tightening of the threshold)
@da.memo.var
def python_import_path(iface_name       = None,         # pylint: disable=R0912
                       dirpath_lwc_root = None):
    """
    Return a list of Python import paths configured for the local working copy.

    Dependency information for the current local
    working copy is stored in the dependency map
    file. Different directories are used to store
    python slibraries for python2 and python3.

    """
    if iface_name is None:
        iface_name = _iface_for_current_python_rt()

    dirpath_env = da.lwc.discover.path(
                                'current_env',
                                dirpath_lwc_root = dirpath_lwc_root)

    register    = dependencies_register(
                                dirpath_lwc_root = dirpath_lwc_root)

    # python_path for the specified iface.
    # Replicates some of the logic in function
    # addpackage in site.py
    #
    python_path = []
    for (_, dependency_data) in register.items():
        try:
            relpath_iface = dependency_data['api'][iface_name]
        except KeyError:
            continue
        dirpath_package = os.path.normpath(
                                os.path.join(
                                    dirpath_env,
                                    dependency_data['dirname'],
                                    dependency_data['policy'],
                                    relpath_iface))
        if not os.path.isdir(dirpath_package):
            continue
        eggs = [os.path.join(dirpath_package, name)
                        for name in os.listdir(dirpath_package)
                                                    if name.endswith('.egg')]
        if eggs:
            python_path.extend(eggs)
        else:
            python_path.append(dirpath_package)

    # All top level directories from src are added to the python_path
    dirpath_src = da.lwc.discover.path(
                                    key = 'src',
                                    dirpath_lwc_root = dirpath_lwc_root)
    for (_, dir_list, _) in os.walk(dirpath_src):
        for name in dir_list:
            if name.startswith('.'):
                continue
            python_path.append(os.path.join(dirpath_src, name))
        break

    # Add system python as well.
    #
    # TODO: !WARNING! !DANGEROUS! !REMOVE AS SOON AS POSSIBLE!
    #
    if iface_name == 'lib_python3':
        python_path.append('/usr/lib/python3.4')
        python_path.append('/usr/lib/python3.4/plat-x86_64-linux-gnu')
        python_path.append('/usr/lib/python3.4/lib-dynload')
        python_path.append('/usr/local/lib/python3.4/dist-packages')
        python_path.append('/usr/lib/python3/dist-packages')

    return python_path


# -----------------------------------------------------------------------------
def _iface_for_current_python_rt():
    """
    Return a library interface id compatible with the current Python runtime.

    The interface id is used to determine which
    library version to import, so we can switch
    between python 2.x and python 3.x if required.

    """
    (major, minor, _) = platform.python_version_tuple()
    try:
        return {
            '2': 'lib_python2',
            '3': 'lib_python3'
        }[major]
    except KeyError:
        raise RuntimeError(
            'Python {major}.{minor} not supported.'.format(major = major,
                                                           minor = minor))
