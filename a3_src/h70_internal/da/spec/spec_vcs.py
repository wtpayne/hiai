# -*- coding: utf-8 -*-
"""
Unit tests for the da.vcs module.

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

import tempfile
import os

import git


# -----------------------------------------------------------------------------
def create_file_and_commit(dirpath_repo, filepath):
    """
    Helper function to commit a file.

    """
    repo = git.Repo(dirpath_repo)
    with open(filepath, 'wt') as file:
        file.write(filepath)
    repo.index.add(repo.untracked_files)
    repo.index.commit('file added: ' + filepath)
    hexsha = repo.commit(repo.head.reference).hexsha
    return hexsha


# =============================================================================
class SpecifyCommitInfo:
    """
    Specify the da.vcs.commit_info() function

    """

    # -------------------------------------------------------------------------
    def it_returns_a_dict_some_commit_related_info(self):
        """
        When given the path to a repository, a dict is returned.

        """
        import da.vcs
        with tempfile.TemporaryDirectory() as dirpath_repo:

            # Create the repository.
            repo = git.Repo.init(dirpath_repo, bare = False)
            assert not repo.bare
            assert repo.head.reference.name == 'master'
            filepath_test = os.path.join(dirpath_repo, 'vcs_test')
            create_file_and_commit(dirpath_repo, filepath_test)
            assert not repo.is_dirty()
            assert not repo.untracked_files
            assert repo.head.reference.name == 'master'

            info = da.vcs.commit_info(dirpath_repo)
            assert isinstance(info, dict)
            assert sorted(info.keys()) == sorted(['ancestor_count',
                                                  'author_email',
                                                  'author_name',
                                                  'author_tz_off',
                                                  'authored_date',
                                                  'branch',
                                                  'commit_message',
                                                  'commit_msg_enc',
                                                  'commit_summary',
                                                  'committed_date',
                                                  'committer_email',
                                                  'committer_name',
                                                  'committer_tz_off',
                                                  'has_untracked',
                                                  'hexsha',
                                                  'is_dirty',
                                                  'is_modified',
                                                  'short_hexsha'])
            assert info['branch'] == 'master'


# =============================================================================
class SpecifyRollbackContext:
    """
    Specify the da.vcs.rollback_context() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The rollback_context() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.rollback_context)


# =============================================================================
class SpecifyRollback:
    """
    Specify the da.vcs.rollback() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The rollback() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.rollback)


# =============================================================================
class SpecifyGetConfigurationId:
    """
    Specify the da.vcs.get_configuration_id() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The get_configuration_id() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.get_configuration_id)


# =============================================================================
class SpecifyGetBranchName:
    """
    Specify the da.vcs.get_branch_name() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The get_branch_name() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.get_branch_name)


# =============================================================================
class SpecifyCheckout:
    """
    Specify the da.vcs.checkout() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The checkout() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.checkout)


# =============================================================================
class SpecifyResetHead:
    """
    Specify the da.vcs.reset_head() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The reset_head() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.reset_head)


# =============================================================================
class SpecifyMoveBranchToHead:
    """
    Specify the da.vcs.move_branch_to_head() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The move_branch_to_head() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.move_branch_to_head)


# =============================================================================
class SpecifyEnsureCloned:
    """
    Specify the da.vcs.ensure_cloned() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The ensure_cloned() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.ensure_cloned)


# =============================================================================
class SpecifyDeleteUntrackedFiles:
    """
    Specify the da.vcs.delete_untracked_files() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The delete_untracked_files() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.delete_untracked_files)


# =============================================================================
class SpecifySetBaseline:
    """
    Specify the da.vcs.set_baseline() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The set_baseline() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.set_baseline)


# =============================================================================
class SpecifyFilesChangedSinceBaseline:
    """
    Specify the da.vcs.files_changed_since_baseline() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The files_changed_since_baseline() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.files_changed_since_baseline)


# =============================================================================
class SpecifyFilesChangedSinceDatetime:
    """
    Specify the da.vcs.files_changed_since_datetime() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The files_changed_since_datetime() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.files_changed_since_datetime)


# =============================================================================
class SpecifyFilesChangedInLwc:
    """
    Specify the da.vcs.files_changed_in_lwc() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The files_changed_in_lwc() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.files_changed_in_lwc)


# =============================================================================
class SpecifyAutoCommit:
    """
    Specify the da.vcs.auto_commit() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The auto_commit() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.auto_commit)


# =============================================================================
class SpecifyBlame:
    """
    Specify the da.vcs.blame() function

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The blame() function is callable.

        """
        import da.vcs
        assert callable(da.vcs.blame)
