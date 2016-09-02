# -*- coding: utf-8 -*-
"""
Machine (workstation & server) management functions.

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

import socket
import platform
import subprocess

import da.register


# ------------------------------------------------------------------------------
def machine_id(dirpath_lwc_root = None, hostname = None):
    """
    Return the identifier code for the current machine (workstation or server).

    """
    hostname   = gethostname() if hostname is None else hostname
    register   = da.register.load(
                            register_name    = 'machine',
                            dirpath_lwc_root = dirpath_lwc_root)

    iter_match = _generate_matching_machines(register, hostname)
    matches    = tuple(iter_match)
    num_match  = len(matches)

    if num_match == 1:
        (matching_id, _) = matches[0]
        return matching_id

    if num_match == 0:
        raise RuntimeError('No matching machines found for: {node}'.format(
                                                            node = hostname))

    if num_match >= 2:
        raise RuntimeError('More than one matching machine found')


# ------------------------------------------------------------------------------
def env_id():
    """
    Return the identifier code for the current runtime environment.

    The env_id is used to identify the machines and binaries that are
    ABI-compatible with one another. Because the way that we check for
    ABI compatibility varies between Linux, Windows and OSX, the logic
    used to determine the env_id is also operating system specific.

    If an env_id is defined, then there is an implied claim of support
    for that runtime environment. We should only add env_ids for which
    we also have the means to run regression tests. (i.e. a virtual
    test environment of some sort)

    """
    system = platform.system()
    if system == 'Linux':

        return _env_id_for_linux_systems()

    elif system == 'Windows':

        raise RuntimeError(
            'Windows is not currently supported by the "hi" tool.')

    elif system == 'Darwin':

        raise RuntimeError(
            'OSX is not currently supported by the "hi" tool.')

    else:

        raise RuntimeError(
            'The system "{system}" is not supported.')


# ------------------------------------------------------------------------------
def _env_id_for_linux_systems():
    """
    Return the identifier code for the current (Linux-based) environment.

    """
    (distro_name,
     distro_ver,
     distro_id) = platform.linux_distribution()

    # If we are running inside pyrun on Ubuntu Linux (Xenial), the
    # platform.linux_distribution function reports 'debian' as the
    # distro_name and 'stretch/sid' as the distro_ver, rather than
    # the 'Ubuntu' and '16.04' that CPython reports. If we suspect
    # that this may be happening, then we fall back on the system
    # lsb_release command to get a more reliably consistent set of
    # values for the distribution information.

    maybe_pyrun = (distro_name == 'debian' and
                   distro_ver  == 'stretch/sid')
    if maybe_pyrun:

        (distro_name,
         distro_ver,
         distro_id)  = _lsb_linux_distribution()

    is_ubuntu_xenial = (distro_name == 'Ubuntu' and
                        distro_ver  == '16.04'  and
                        distro_id   == 'xenial')

    machine   = platform.machine()
    is_x86_64 = machine == 'x86_64'

    if is_x86_64 and is_ubuntu_xenial:
        return 'e00_x86_64_linux_ubuntu_xenial'

    raise RuntimeError(
        'Linux distribution "{name} - {ver} - {id}" is not supported.'.format(
                                                            name = distro_name,
                                                            ver  = distro_ver,
                                                            id   = distro_id))


# ------------------------------------------------------------------------------
def gethostname():
    """
    Return the current hostname.

    This function is an alias for socket.gethostname.

    """
    return socket.gethostname()


# -----------------------------------------------------------------------------
def _generate_matching_machines(register, hostname):
    """
    Yield all registered machines that match the current hostname.

    """
    for (registered_machine_id, machine_data) in register.items():
        if hostname == machine_data['hostname']:
            yield (registered_machine_id, machine_data)


# ------------------------------------------------------------------------------
def _lsb_release(arg):
    """
    Return the output of the /usr/bin/lsb_release command.

    """
    filepath_bin = '/usr/bin/lsb_release'
    command      = [filepath_bin, '--{arg}'.format(arg = arg)]
    output_bytes = subprocess.check_output(command)
    output       = output_bytes.decode(encoding = 'utf-8', errors = 'strict')
    output_parts = output.split()
    output_value = output_parts[-1]
    return output_value


# ------------------------------------------------------------------------------
def _lsb_linux_distribution():
    """
    Return a tuple describing the linux distribution name, version and id.

    """
    distro_name = _lsb_release('id')
    distro_ver  = _lsb_release('release')
    distro_id   = _lsb_release('codename')
    return (distro_name,
            distro_ver,
            distro_id)
