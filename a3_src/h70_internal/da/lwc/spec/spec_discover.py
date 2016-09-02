# -*- coding: utf-8 -*-
"""
Unit tests for the da.lwc.discover module.

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

import pytest

import da.lwc.discover


# -----------------------------------------------------------------------------
@pytest.fixture
def dirpath_testdata():
    """
    Return the test data path.

    """
    return os.path.join(os.path.dirname(__file__), 'data')


# =============================================================================
class SpecifyGenSrcFiles:
    """
    Specify the da.lwc.discover.gen_src_files() function.

    """

    # -------------------------------------------------------------------------
    def it_yields_file_paths_that_exist(self):
        """
        The gen_src_files generator SHALL yield paths that exist.

        """
        dirpath_lwc_root = da.lwc.discover.path('root')
        for filepath_srcfile in da.lwc.discover.gen_src_files(dirpath_lwc_root):
            assert os.path.isfile(filepath_srcfile)


# =============================================================================
class SpecifyPath:
    """
    Specify the da.lwc.discover.path() function.

    """

    # -------------------------------------------------------------------------
    def it_can_discover_the_root_of_the_repo(self, dirpath_testdata):
        """
        It can correctly identify the root of the repository.

        """
        specified_root  = dirpath_testdata
        actual_result   = da.lwc.discover.path(
                            key = 'root', dirpath_lwc_root = specified_root)
        expected_result = specified_root
        assert expected_result == actual_result

    # -------------------------------------------------------------------------
    def it_can_discover_parts_of_the_repo(self):
        """
        It can correctly identify the root of the real directories.

        """
        dirpath_root     = da.lwc.discover.path('root')
        assert os.path.isdir(dirpath_root), \
            'Discovered path for key "root" does not exist: {path}'.format(
                                                    path = dirpath_root)

        dirpath_env      = da.lwc.discover.path('env')
        assert os.path.isdir(dirpath_env), \
            'Discovered path for key "env" does not exist: {path}'.format(
                                                    path = dirpath_env)

        dirpath_cfg      = da.lwc.discover.path('cfg')
        assert os.path.isdir(dirpath_cfg), \
            'Discovered path for key "cfg" does not exist: {path}'.format(
                                                    path = dirpath_cfg)

        dirpath_dat      = da.lwc.discover.path('dat')
        assert os.path.isdir(dirpath_dat), \
            'Discovered path for key "dat" does not exist: {path}'.format(
                                                    path = dirpath_dat)

        dirpath_src      = da.lwc.discover.path('src')
        assert os.path.isdir(dirpath_src), \
            'Discovered path for key "src" does not exist: {path}'.format(
                                                    path = dirpath_src)

        dirpath_internal = da.lwc.discover.path('internal')
        assert os.path.isdir(dirpath_internal), \
            'Discovered path for key "internal" does not exist: {path}'.format(
                                                    path = dirpath_internal)



# =============================================================================
class SpecifyGenCounterpartyDirs:
    """
    Specify the da.lwc.discover.gen_counterparty_dirs() function.

    """

    def it_is_callable(self):
        """
        The gen_counterparty_dirs() function is callable.

        """
        assert callable(da.lwc.discover.gen_counterparty_dirs)


# =============================================================================
class SpecifyGenProjectDirs:
    """
    Specify the da.lwc.discover.gen_project_dirs() function.

    """

    def it_is_callable(self):
        """
        The gen_project_dirs() function is callable.

        """
        assert callable(da.lwc.discover.gen_project_dirs)
