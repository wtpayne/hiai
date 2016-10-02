# -*- coding: utf-8 -*-
"""
Version control system wrapper (software abstraction layer).

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


import functools
import itertools
import os
import shutil

import git

import da.commit_message
import da.lwc.discover


# -----------------------------------------------------------------------------
def changed_files(dirpath_lwc_root):
    """
    Return a list of files that have changed versus each repository index.

    We want static analysis and unit tests
    to be as fast as possible, so we gather
    a list of files that have changed
    between repo HEAD and the LWC.

    We can combine this with a list of
    previous test failures to reduce the
    amount of time wasted testing items
    that are known to conform with our
    rules and guidelines.

    """
    repo_tab  = design_repo_tab(dirpath_lwc_root)
    file_list = []
    for (relpath_repo, repo) in repo_tab.items():

        dirpath_repo = os.path.normpath(
                            os.path.join(dirpath_lwc_root, relpath_repo))

        # Add untracked files to list.
        for relpath in repo.untracked_files:
            abspath = os.path.join(dirpath_lwc_root, relpath)
            if os.path.isfile(abspath):
                file_list.append(abspath)

        try:
            last_commit = repo.head.commit
        except ValueError:
            continue

        # Add changed files to list.
        for diff_item in last_commit.diff(None):
            if diff_item.deleted_file:
                continue

            # In case of a rename, try both possibilities...
            abspath = os.path.join(dirpath_repo, diff_item.a_path)
            if os.path.isfile(abspath):
                file_list.append(abspath)

            abspath = os.path.join(dirpath_repo, diff_item.b_path)
            if os.path.isfile(abspath):
                file_list.append(abspath)

    return file_list


# -----------------------------------------------------------------------------
def delete_untracked(dirpath_repo):
    """
    Delete untracked files in the specified repo.

    Used by da.dep.py

    """
    repo = get_repo(dirpath_repo)
    for relpath in repo.untracked_files:
        path = os.path.join(dirpath_repo, relpath)
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


# -----------------------------------------------------------------------------
@functools.lru_cache(maxsize = 8)
def get_repo(path):
    """
    Return the repo object for path.

    """
    return git.Repo(path)


# ------------------------------------------------------------------------------
def get_baseline_for_rollback(dirpath_lwc_root):
    """
    Return baseline information for the specified design repository.

    This function returns the information that is
    required by the da.vcs.wrapper.rollback_to_baseline
    function.

    """
    baseline = dict()
    repo_tab = design_repo_tab(dirpath_lwc_root)
    for relpath in repo_tab.keys():

        repo = repo_tab[relpath]

        try:
            branch = repo.head.reference.name
        except TypeError:   # Detatched HEAD.
            branch = None

        try:
            configuration_id = repo.head.commit.hexsha
        except ValueError:  # No previous commits.
            configuration_id = None

        baseline[relpath] = {
            'repo':             repo,
            'branch':           branch,
            'configuration_id': configuration_id
        }

    return baseline


# ------------------------------------------------------------------------------
def rollback_to_baseline(baseline):
    """
    Roll the specified branch back to the specified configuration.

    The local working copy is not modified, but the
    repository state is reset back to the version
    specified in the provided baseline data structure.

    """
    for relpath in baseline.keys():

        repo             = baseline[relpath]['repo']
        branch_name      = baseline[relpath]['branch']
        configuration_id = baseline[relpath]['configuration_id']

        # If we tried to take the baseline before
        # we made any commits to the repository.
        if configuration_id is None:
            continue

        repo.head.reset(commit       = configuration_id,
                        index        = False,
                        working_tree = False)

        # Resetting the HEAD of a git repository does
        # not automatically update the branch. This will
        # result in a detatched HEAD if we do not also
        # update the branch.
        #
        # Of course, if the baseline had a detatched HEAD,
        # then we don't need to do anything.
        #
        baseline_has_detatched_head = branch_name is None
        if not baseline_has_detatched_head:
            branch              = repo.refs[branch_name]
            branch.commit       = repo.head.commit
            repo.head.reference = branch


# -----------------------------------------------------------------------------
def is_modified(repo):
    """
    Return True if the specified repo has modifications.

    Used by da.vcs.auto_commit() function.

    """
    is_dirty      = repo.is_dirty()
    has_untracked = len(repo.untracked_files) > 0
    return is_dirty or has_untracked


# -----------------------------------------------------------------------------
def last_commit_message(dirpath_lwc_root):
    """
    Return True if the repo at the specified repo has modifications.

    Used by da.vcs.auto_commit() function.

    """
    repo = get_repo(dirpath_lwc_root)
    if len(repo.heads) > 0:
        return da.commit_message.parse(repo.head.commit.message)
    else:
        return {}


# -----------------------------------------------------------------------------
def commit(repo, commit_msg, try_amendment):
    """
    Commit the current LWC state to the repository.

    This is done either as a new commit or as an
    amendment to the most recent commit.

    The SHA-1 hex digest for the resulting HEAD
    revision will be returned.

    Used by da.vcs.auto_commit() function.

    """
    if try_amendment:

        # If we are trying to make an amendment to
        # a previous commit, we need to ensure that
        # the previous commit actually exists and
        # that it has exactly one parent.
        #
        try:
            head_commit = repo.head.commit
        except ValueError:
            head_commit = None
        can_make_amendment = (
            (head_commit is not None) and (len(head_commit.parents) == 1))

        # To amend the previous commit, we need to
        # reset the branch back to the parent of
        # the current head_commit before we make
        # a new commit.
        #
        if can_make_amendment:
            branch        = repo.head.reference
            branch.commit = head_commit.parents[0]

    repo.git.add(all = True)
    repo.index.commit(commit_msg)
    return repo.head.commit.hexsha


# -----------------------------------------------------------------------------
def design_repo_tab(dirpath_lwc_root):
    """
    Return a dict containing all design document repositories.

    """
    iter_dirpath_repo = itertools.chain(
        (dirpath_lwc_root,),
        da.lwc.discover.gen_product_dirs(dirpath_lwc_root),
        da.lwc.discover.gen_counterparty_dirs(dirpath_lwc_root),
        da.lwc.discover.gen_research_dirs(dirpath_lwc_root),
        da.lwc.discover.gen_demo_dirs(dirpath_lwc_root))

    repo_tab = dict()
    for dirpath_repo in iter_dirpath_repo:

        try:
            repo = git.Repo(dirpath_repo)
        except git.exc.InvalidGitRepositoryError:
            continue

        relpath_repo = os.path.relpath(dirpath_repo, start = dirpath_lwc_root)
        repo_tab[relpath_repo] = repo

    return repo_tab
