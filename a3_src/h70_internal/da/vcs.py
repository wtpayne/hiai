# -*- coding: utf-8 -*-
"""
Version Control System functions.

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

import contextlib
import datetime
import functools
import logging
import os
import shutil

import git

import da.commit_message
import da.daybook
import da.lwc.discover
import da.util


# ------------------------------------------------------------------------------
def get_configuration_id(dirpath_root):
    """
    Return the current configuration id.

    This is the git SHA-1 hash code.

    """
    return _repo(dirpath_root).head.commit.hexsha


# ------------------------------------------------------------------------------
def get_branch_name(dirpath_root):
    """
    Return the name of the current branch.

    This is either the name of the current branch or None if head is detached.

    """
    try:
        return _repo(dirpath_root).head.reference.name
    except TypeError:
        return None


# ------------------------------------------------------------------------------
def checkout(dirpath_root, configuration_id):
    """
    Checkout the specified configuration id into the local working copy.

    This function changes the head of the repository
    to match the specified configuration id (git sha
    or reference) and changes the files in the local
    working copy and the staging area (git index) to
    match.

    """
    _repo(dirpath_root).head.reset(commit       = configuration_id,
                                   index        = True,
                                   working_tree = True)


# ------------------------------------------------------------------------------
@contextlib.contextmanager
def rollback_context(dirpath_root):
    """
    Record the initial repository state and rollback if an exception is raised.

    We want to be able to revert back to a known
    good state if anything goes wrong, so right
    at the start of the meta-build process we take
    a record of the source repository configuration
    id (git SHA) as well as the name of the current
    branch.

    If an exception occurs, we reset the repository
    right to its' original state prior to our auto-
    commit of any local developer changes so that
    the developer has a chance to redo or modify
    his changes before continuing.

    """
    baseline_id = da.vcs.get_configuration_id(dirpath_root)
    branch_name = da.vcs.get_branch_name(dirpath_root)
    try:
        yield
    except (Exception, KeyboardInterrupt):
        rollback(dirpath_root     = dirpath_root,
                 branch_name      = branch_name,
                 configuration_id = baseline_id)
        raise


# ------------------------------------------------------------------------------
def rollback(dirpath_root, branch_name, configuration_id):
    """
    Roll the specified branch back to the specified configuration.

    """
    reset_head(dirpath_root, configuration_id)
    if branch_name is not None:
        move_branch_to_head(dirpath_root, branch_name)


# ------------------------------------------------------------------------------
def reset_head(dirpath_root, configuration_id):
    """
    Reset the head of the repository to the specified configuration id.

    This function changes the head of the repository
    to match the specified configuration id (git sha
    or reference) but leaves the local working copy
    and the staging area (git index) alone.

    """
    _repo(dirpath_root).head.reset(commit       = configuration_id,
                                   index        = False,
                                   working_tree = False)


# ------------------------------------------------------------------------------
def move_branch_to_head(dirpath_root, branch_name):
    """
    Move/rename the specified branch to the head commit.

    This function moves the specified branch so
    that it points to the current head of the
    repository.

    """
    repo                = _repo(dirpath_root)
    branch              = repo.refs[branch_name]
    branch.commit       = repo.head.commit
    repo.head.reference = branch


# ------------------------------------------------------------------------------
def commit_info(dirpath_root = None, ref = 'HEAD'):
    """
    Get assorted commit information for the specified repo & commit reference.

    This function is used to keep a record of the
    design configuration that the currently executing
    metabuild instance belongs to.

    """
    if dirpath_root is None:
        dirpath_root = da.lwc.discover.path("root")

    try:

        repo          = _repo(dirpath_root)
        active_branch = repo.active_branch.name
        commit        = repo.commit(ref)
        hexsha        = commit.hexsha
        is_dirty      = repo.is_dirty()
        has_untracked = len(repo.untracked_files) > 0
        is_modified   = is_dirty or has_untracked

        # Heuristic to determine an appropriate branch name.
        szbranches    = repo.git.branch('--contains', hexsha)
        branch_list   = [sz.strip(' *') for sz in szbranches.split('\n')]
        if len(branch_list) == 0:
            raise RuntimeError('Expecting commit to be on a branch')
        if active_branch in branch_list:
            branch = active_branch
        elif 'master' in branch_list:
            branch = 'master'
        else:
            branch = sorted(branch_list)[0]

        # summary line is first line (but strip whitespace first!)
        commit_message = commit.message
        commit_summary = commit_message.strip().split('\n')[0]

        return {
            'hexsha':           hexsha,
            'short_hexsha':     hexsha[0:8],
            'branch':           branch,
            'is_dirty':         is_dirty,
            'has_untracked':    has_untracked,
            'is_modified':      is_modified,
            'author_name':      commit.author.name,
            'author_email':     commit.author.email,
            'committer_name':   commit.committer.name,
            'committer_email':  commit.committer.email,
            'commit_summary':   commit_summary,
            'commit_message':   commit_message,
            'commit_msg_enc':   commit.encoding,
            'authored_date':    datetime.datetime.fromtimestamp(
                                            commit.authored_date).isoformat(),
            'author_tz_off':    commit.author_tz_offset,
            'committed_date':   datetime.datetime.fromtimestamp(
                                            commit.committed_date).isoformat(),
            'committer_tz_off': commit.committer_tz_offset,
            'ancestor_count':   commit.count('')
        }

    except (ValueError, git.exc.InvalidGitRepositoryError):

        return {
            'hexsha':           None,
            'short_hexsha':     None,
            'branch':           None,
            'author_name':      None,
            'author_email':     None,
            'committer_name':   None,
            'committer_email':  None,
            'commit_summary':   None,
            'commit_message':   None,
            'commit_msg_enc':   None,
            'authored_date':    None,
            'author_tz_off':    None,
            'committed_date':   None,
            'committer_tz_off': None,
            'ancestor_count':   None
        }


# ------------------------------------------------------------------------------
def ensure_cloned(dirpath_local, url_remote, ref):
    """
    Force local repository to a state cloned from the remote.

    """
    # Ensure the local repo exists.
    da.util.ensure_dir_exists(dirpath_local)
    try:
        local = _repo(dirpath_local)
    except git.exc.InvalidGitRepositoryError:
        git.Repo.clone_from(url_remote, dirpath_local)
        local = git.Repo(dirpath_local)
    assert not local.bare
    if not local.working_tree_dir == dirpath_local:
        raise RuntimeError(
                'Misconfigured LWC. Should be {planned}. Is: {acutual}'.format(
                                            planned = dirpath_local,
                                            acutual = local.working_tree_dir))

    # Ensure that the remote is configured.
    origin = local.remotes['origin']
    config_writer = origin.config_writer
    config_writer.set('fetchhurl', url_remote)
    config_writer.set('pushurl',   url_remote)
    config_writer.set('url',       url_remote)
    config_writer.release()
    assert local.remotes['origin'].url == url_remote

    # Checkout specified version (detatched head)
    local.remotes.origin.fetch()
    local.head.reference = ref
    local.head.reset(index = True, working_tree = True)

    assert local.head.is_detached
    assert not local.is_dirty()

    # assert len(local.untracked_files) == 0
    if len(local.untracked_files) > 0:
        for untracked_filepath in local.untracked_files:
            logging.error('Untracked file found: %s', untracked_filepath)
        raise RuntimeError(
                'Untracked files found in working copy: {path}'.format(
                                                        path = dirpath_local))


# -----------------------------------------------------------------------------
def delete_untracked_files(dirpath_repo):
    """
    Delete untracked files in the specified repo.

    """
    repo = _repo(dirpath_repo)
    for relpath in repo.untracked_files:
        path = os.path.join(dirpath_repo, relpath)
        if os.path.isfile(path):
            os.unlink(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


# -----------------------------------------------------------------------------
def set_baseline(baseline, dirpath_root):
    """
    Mark the current configuration with the specified baseline id.

    """
    repo = _repo(dirpath_root)
    if baseline not in repo.heads:
        branch = repo.create_head(baseline)
    else:
        branch = repo.heads[baseline]
    branch.set_commit(repo.head.commit)


# -----------------------------------------------------------------------------
def files_changed_since_baseline(baseline, dirpath_root):
    """
    Return the files changed since the specified baseline id was set.

    """
    repo        = _repo(dirpath_root)
    past_commit = repo.refs[baseline].commit
    file_list   = []
    for diff_item in past_commit.diff(None):
        if diff_item.deleted_file:
            continue
        file_list.append(os.path.join(dirpath_root, diff_item.b_path))


# -----------------------------------------------------------------------------
def files_changed_since_datetime(timestamp, dirpath_root):
    """
    Return a list of files that have changed since the specified timestamp.

    """
    repo     = _repo(dirpath_root)
    baseline = None
    for commit in repo.head.commit.iter_parents():
        ts_epoch    = commit.committed_date
        ts_datetime = datetime.datetime.utcfromtimestamp(ts_epoch)
        if ts_datetime <= timestamp:
            baseline = commit
            break

    if baseline is None:
        return []

    file_list = []
    for diff_item in baseline.diff(None):
        if diff_item.deleted_file:
            continue
        file_list.append(os.path.join(dirpath_root, diff_item.b_path))
    return file_list


# -----------------------------------------------------------------------------
def files_changed_in_lwc(dirpath_root):
    """
    Return a list of files that have changed versus the repository index.

    This

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
    repo      = _repo(dirpath_root)
    file_list = []
    # Add untracked files to list.
    for relpath in repo.untracked_files:
        os.path.join(dirpath_root, relpath)
    # Add changed files to list.
    for diff_item in repo.head.commit.diff(None):
        if diff_item.deleted_file:
            continue
        if diff_item.renamed:
            continue
        # new_file      - boolean
        # renamed       - boolean
        # deleted_file  - boolean
        # a_path        - old path
        # b_path        - new path
        # rename_from   - TODO: Determine field meaning & if it should be used
        # rename_to     - TODO: Determine field meaning & if it should be used
        file_list.append(os.path.join(dirpath_root, diff_item.b_path))
    return file_list


# -----------------------------------------------------------------------------
def auto_commit(cfg, dirpath_lwc_root):
    """
    Automatically commit changed files to the VCS.

    We want to be able to reproduce and diagnose
    errors when they occur, which means keeping
    careful records so that each and every build
    is made from a known design configuration.

    To ease the administrative burden of this, we
    automatically commit changes to the local
    working copy; using periodic audits together
    with a strict whitelist based .gitignore file
    to keep unwanted files out of the repository.

    """
    if not cfg['options']['auto_commit']:
        return

    # Have we made any changes?
    repo          = _repo(dirpath_lwc_root)
    is_dirty      = repo.is_dirty()
    has_untracked = len(repo.untracked_files) > 0
    is_modified   = is_dirty or has_untracked
    if not is_modified:
        return

    # What are we currently working on?
    daybook_entry = da.daybook.latest_entry(
                iso_year_id      = cfg['timestamp']['iso_year_id'],
                timebox_id       = cfg['timestamp']['timebox_id'],
                date             = cfg['timestamp']['date'],
                team_member_id   = cfg['build_context']['team_member_id'],
                dirpath_lwc_root = dirpath_lwc_root)
    work_summary  = daybook_entry['work_summary']
    work_notes    = daybook_entry['work_notes']

    # TODO: Make sure our changes fall within the
    #       mandate of our current job.

    # What were we working on in the last commit?
    prev = {}
    if len(repo.heads) > 0:
        prev = da.commit_message.parse(repo.head.commit.message)
    prev_work_start_time = prev['work_start_time']

    # Are we working on the same thing as before?
    is_same_work = (     work_summary == prev['work_summary']
                     and work_notes   == prev['work_notes'])

    # If we are working on the same thing as before,
    # fixup the content of the previous commit with
    # our new changes.
    #
    branch      = repo.head.reference
    head_commit = repo.head.commit
    if is_same_work and (len(head_commit.parents) == 1):
        branch.commit = head_commit.parents[0]
    repo.git.add(all = True)

    # Keep track of when the work started.
    if is_same_work and prev_work_start_time is not None:
        work_start_time = prev_work_start_time
    else:
        work_start_time = cfg['timestamp']['timestamp_isofmt']

    commit_msg = da.commit_message.compose(daybook_entry, work_start_time)

    # Commit changes to the repository.
    repo.index.commit(commit_msg)


# -----------------------------------------------------------------------------
def blame(filepath, dirpath_lwc_root):
    """
    Return the blame information for the specified file.

    """
    repo = _repo(dirpath_lwc_root)
    return repo.blame('HEAD', filepath)


# -----------------------------------------------------------------------------
@functools.lru_cache(maxsize = 1)
def _repo(path):
    """
    Return the repo object for path.

    """
    return git.Repo(path)
