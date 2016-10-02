# -*- coding: utf-8 -*-
"""
Unit tests for the da.vcs.git_adapter module.

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


import git
import pytest


# =============================================================================
class SpecifyChangedFiles:
    """
    Specify the da.vcs.git_adapter.changed_files() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The changed_files() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.changed_files)


# =============================================================================
class SpecifyDeleteUntracked:
    """
    Specify the da.vcs.git_adapter.delete_untracked() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The delete_untracked() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.delete_untracked)


# =============================================================================
class SpecifyGetRepo:
    """
    Specify the da.vcs.git_adapter.get_repo() function

    """

    # -------------------------------------------------------------------------
    def it_returns_a_git_repo_object(self, dirpath_lwc_root):
        """
        The get_repo() function returns a git.Repo object.

        """
        import da.vcs.git_adapter
        repo = da.vcs.git_adapter.get_repo(dirpath_lwc_root)
        assert isinstance(repo, git.Repo)


# =============================================================================
class SpecifyGetBaselineForRollback:
    """
    Specify the da.vcs.git_adapter.get_baseline_for_rollback() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The get_baseline_for_rollback() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.get_baseline_for_rollback)


# =============================================================================
class SpecifyRollbackToBaseline:
    """
    Specify the da.vcs.git_adapter.rollback_to_baseline() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The rollback_to_baseline() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.rollback_to_baseline)


# =============================================================================
class SpecifyIsModified:
    """
    Specify the da.vcs.git_adapter.is_modified() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The is_modified() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.is_modified)


# =============================================================================
class SpecifyLastCommitMessage:
    """
    Specify the da.vcs.git_adapter.last_commit_message() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The last_commit_message() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.last_commit_message)


# =============================================================================
class SpecifyCommit:
    """
    Specify the da.vcs.git_adapter.commit() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The commit() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.commit)


# =============================================================================
class SpecifyDesignRepoTab:
    """
    Specify the da.vcs.git_adapter.design_repo_tab() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The design_repo_tab() function is callable.

        """
        import da.vcs.git_adapter
        assert callable(da.vcs.git_adapter.design_repo_tab)


# -----------------------------------------------------------------------------
@pytest.fixture(scope = 'module')
def dirpath_lwc_root():
    """
    Return the directory path to the root of the local working copy.

    """
    import da.lwc.discover
    return da.lwc.discover.path('root')
