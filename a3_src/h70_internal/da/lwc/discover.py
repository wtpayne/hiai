# -*- coding: utf-8 -*-
"""
Local working copy path aliasing.

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

import da.lwc.search
import da.memo


LWC_DIR_EXCLUDE_EXPR_LIST = [r'^\..*$',
                             r'^\.git$',
                             r'^\.cache$',
                             r'^\.vagrant',
                             r'^__pycache__']

LWC_EXT_INCLUDE_EXPR_LIST = [r'^.*\.bash$',
                             r'^.*\.css$',
                             r'^.*\.template.html$',
                             r'^.*\.template.docx$',
                             r'^.*\.py$',
                             r'^.*\.md$',
                             r'^.*\.json$',
                             r'^.*\.yaml$']

LWC_PROJECT_DIR_EXPR      = r'^.*p[0-9]{4}_[a-z0-9_]{2,64}$'

LWC_COUNTERPARTY_DIR_EXPR = r'^.*c[0-9]{3}_[a-z0-9_]{2,64}$'

LWC_RESEARCHER_DIR_EXPR   = r'^.*t[0-9]{3}_[a-z0-9_]{2,64}$'

_LWC_TAB = {
    'env':        ('a0_env',                                ),
    'cfg':        ('a1_cfg',                                ),
    'dat':        ('a2_dat',                                ),
    'src':        ('a3_src',                                ),
    'tmp':        ('a4_tmp',                                ),
    'cms':        ('a5_cms',                                ),
    'resource':   ('a3_src', 'h10_resource'                 ),
    'daybook':    ('a3_src', 'h10_resource', 'daybook'      ),
    'registry':   ('a3_src', 'h10_resource', 'registry'     ),
    'capability': ('a3_src', 'h20_capability'               ),
    'product':    ('a3_src', 'h30_product'                  ),
    'project':    ('a3_src', 'h40_project'                  ),
    'research':   ('a3_src', 'h50_research'                 ),
    'demo':       ('a3_src', 'h60_demo'                     ),
    'internal':   ('a3_src', 'h70_internal'                 ),
    'bldcfg':     ('a3_src', 'h70_internal', 'da', 'bldcfg' ),
    'doc':        ('a3_src', 'h80_doc'                      )
}


# -----------------------------------------------------------------------------
def gen_product_dirs(dirpath_lwc_root = None):
    """
    Generate all product dirs in the local working copy.

    """
    return da.lwc.search.filtered_dirpath_generator(
                        root     = path(key              = 'product',
                                        dirpath_lwc_root = dirpath_lwc_root),
                        direxcl  = da.lwc.discover.LWC_DIR_EXCLUDE_EXPR_LIST,
                        pathincl = None,
                        pathexcl = None)


# -----------------------------------------------------------------------------
def gen_counterparty_dirs(dirpath_lwc_root = None):
    """
    Generate all project counterparty dirs in the local working copy.

    """
    return da.lwc.search.filtered_dirpath_generator(
                        root     = path(key              = 'project',
                                        dirpath_lwc_root = dirpath_lwc_root),
                        direxcl  = da.lwc.discover.LWC_DIR_EXCLUDE_EXPR_LIST,
                        pathincl = [da.lwc.discover.LWC_COUNTERPARTY_DIR_EXPR],
                        pathexcl = None)


# -----------------------------------------------------------------------------
def gen_project_dirs(dirpath_lwc_root = None):
    """
    Generate all project dirs in the local working copy.

    """
    return da.lwc.search.filtered_dirpath_generator(
                        root     = path(key              = 'project',
                                        dirpath_lwc_root = dirpath_lwc_root),
                        direxcl  = da.lwc.discover.LWC_DIR_EXCLUDE_EXPR_LIST,
                        pathincl = [da.lwc.discover.LWC_PROJECT_DIR_EXPR],
                        pathexcl = None)


# -----------------------------------------------------------------------------
def gen_research_dirs(dirpath_lwc_root = None):
    """
    Generate all research (per team member) dirs in the local working copy.

    """
    return da.lwc.search.filtered_dirpath_generator(
                        root     = path(key              = 'research',
                                        dirpath_lwc_root = dirpath_lwc_root),
                        direxcl  = da.lwc.discover.LWC_DIR_EXCLUDE_EXPR_LIST,
                        pathincl = [da.lwc.discover.LWC_RESEARCHER_DIR_EXPR],
                        pathexcl = None)


# -----------------------------------------------------------------------------
def gen_demo_dirs(dirpath_lwc_root = None):
    """
    Generate all demo dirs in the local working copy.

    """
    return da.lwc.search.filtered_dirpath_generator(
                        root     = path(key              = 'demo',
                                        dirpath_lwc_root = dirpath_lwc_root),
                        direxcl  = da.lwc.discover.LWC_DIR_EXCLUDE_EXPR_LIST,
                        pathincl = None,
                        pathexcl = None)


# -----------------------------------------------------------------------------
def gen_src_files(dirpath_lwc_root = None):
    """
    Generate all source files in the local working copy.

    """
    if dirpath_lwc_root is None:
        dirpath_lwc_root = _lwc_root(__file__)
    return da.lwc.search.filtered_filepath_generator(
                root     = path(key              = 'src',
                                dirpath_lwc_root = dirpath_lwc_root),
                direxcl  = da.lwc.discover.LWC_DIR_EXCLUDE_EXPR_LIST,
                pathincl = da.lwc.discover.LWC_EXT_INCLUDE_EXPR_LIST)


# -----------------------------------------------------------------------------
@da.memo.var
def path(key, dirpath_lwc_root = None):
    """
    Return the directory path corresponding to the specified key.

    """
    # Get lwc_root if it is not defined
    if dirpath_lwc_root is None:
        dirpath_lwc_root = _lwc_root(__file__)

    # LWC root
    if key == 'root':
        return dirpath_lwc_root

    # Handle 'heavyweight' folders that can't get copied to tmp
    if (key == 'env') or (key == 'cfg') or (key == 'dat'):
        dirname_tmp = _LWC_TAB['tmp'][0]
        is_tmp_lwc  = dirname_tmp in dirpath_lwc_root
        if is_tmp_lwc:
            dirpath_outer_lwc_root = _lwc_root(dirpath_lwc_root)
        else:
            dirpath_outer_lwc_root = dirpath_lwc_root
        return os.path.join(dirpath_outer_lwc_root, *_LWC_TAB[key])

    # Env dir for the current runtime environment?
    if key == 'current_env':
        import da.machine as _machine
        dirpath_env = path(key = 'env', dirpath_lwc_root = dirpath_lwc_root)
        env_id      = _machine.env_id()
        return os.path.join(dirpath_env, env_id)

    # Config directory for the current user & machine?
    if key == 'current_cfg':
        import da.team as _team
        import da.machine as _machine
        dirpath_cfg = path(key = 'cfg', dirpath_lwc_root = dirpath_lwc_root)
        member_id   = _team.member_id(dirpath_lwc_root = dirpath_lwc_root)
        machine_id  = _machine.machine_id(dirpath_lwc_root = dirpath_lwc_root)
        return os.path.join(dirpath_cfg, member_id, machine_id)

    # Key is an entry in the static table above?
    if key in _LWC_TAB:
        return os.path.join(dirpath_lwc_root, *_LWC_TAB[key])

    raise RuntimeError(
            'Could not identify path for key: {key}'.format(
                                                        key = key))


# -----------------------------------------------------------------------------
@da.memo.var
def _lwc_root(filepath_self):
    """
    Return the directory path to the root of the local working copy.

    """
    marker_file_name   = 'da'
    dirpath_self       = os.path.dirname(filepath_self)
    dirpath_lwc_root   = da.lwc.search.find_ancestor_dir_containing(
                            dirpath_self, marker_file_name, allow_dir = False)
    dirpath_normalised = os.path.normpath(dirpath_lwc_root)
    dirpath_real       = os.path.realpath(dirpath_normalised)
    return dirpath_real
