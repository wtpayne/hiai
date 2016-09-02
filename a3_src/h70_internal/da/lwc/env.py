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
def dependency_path(dependency_id,
                    interface,
                    register         = None,
                    dirpath_lwc_root = None):
    """
    Return the path for the specified interface type and dependency id.

    """
    if register is None:
        register = dependencies_register(
                                    dirpath_lwc_root = dirpath_lwc_root)

    if dependency_id not in register:
        raise RuntimeError(
                'Could not identify dependency: "{dep}".'.format(
                                    dep = dependency_id))

    dependency_data = register[dependency_id]
    if interface not in dependency_data['iface']:
        raise RuntimeError(
                ('Dependency: "{dep}" ' +
                 'does not support interface "{iface}".').format(
                                    iface = interface,
                                    dep   = dependency_id))

    if interface not in dependency_data['path']:
        raise RuntimeError(
                ('Dependency: "{dep}" ' +
                 'does not declare a path for interface "{iface}".').format(
                                    iface = interface,
                                    dep   = dependency_id))

    dirpath_env = da.lwc.discover.path(
                                    'current_env',
                                    dirpath_lwc_root = dirpath_lwc_root)

    return os.path.normpath(os.path.join(
                                    dirpath_env,
                                    dependency_data['dirname'],
                                    dependency_data['policy'],
                                    dependency_data['path'][interface]))


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
def python_import_path(interface = None,                # pylint: disable=R0912
                       dirpath_lwc_root = None):
    """
    Return a list of Python import paths configured for the local working copy.

    Dependency information for the current local working copy is stored in
    the dependency map file. Different directories are used to store python
    libraries for python2 and python3.

    """
    if interface is None:
        interface = _iface_for_current_python_rt()

    dirpath_env = da.lwc.discover.path(
                                'current_env',
                                dirpath_lwc_root = dirpath_lwc_root)

    register    = dependencies_register(
                                dirpath_lwc_root = dirpath_lwc_root)

    # python_path for the specified iface.
    # Replicates some of the logic in function addpackage in site.py
    python_path = []
    for (_, dependency_data) in register.items():
        if interface not in dependency_data['iface']:
            continue
        dirpath_package = os.path.normpath(
                                os.path.join(
                                    dirpath_env,
                                    dependency_data['dirname'],
                                    dependency_data['policy'],
                                    dependency_data['path'][interface]))
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

    # # Add system python as well. !WARNING! !DANGEROUS! !REMOVE WHEN POSSIBLE!
    if interface == 'lib_python3':
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

    The interface id is used to determine which library version to import, so
    we can switch between python 2.x and python 3.x if required.

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
