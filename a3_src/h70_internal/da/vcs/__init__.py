# -*- coding: utf-8 -*-
"""
Version Control System functions.

The da.vcs.git_adapter module acts as an abstraction
layer around the VCS tool so that we can replace
git with mercurial at some point in the future. It
should contain little or no application specific
logic.

By contrast, this module (__init__,py) sits on top
of da.vcs.git_adapter and uses it to provide some more
bespoke tailored functions for the application.

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
import logging
import os

import git

import da.commit_message
import da.daybook
import da.lwc.discover
import da.util

from . import git_adapter as vcs_adapter


# ------------------------------------------------------------------------------
@contextlib.contextmanager
def rollback_context(dirpath_root):
    """
    Record the initial repository state & roll back if an exception is raised.

    This function is used by da.metabuild to safely roll
    the repository back to a known good configuration
    in the event of an error in the build process or if
    a nonconformity in a design document is discovered.

    When this context manager is initialised (right
    at the start of the meta-build process), we
    take a record of the design document repository
    configuration id (git SHA) as well as the name
    of the current branch.

    If an exception is thrown during the metabuild
    process, we then reset the repository back to
    its' original (baseline) state prior to any
    automatic commits that the metabuild process
    may have triggered.

    This gives the team member developer a chance
    to redo or modify his changes before continuing.

    """
    baseline = vcs_adapter.get_baseline_for_rollback(dirpath_root)
    try:
        (yield)
    except (Exception, KeyboardInterrupt):
        vcs_adapter.rollback_to_baseline(baseline)
        raise


# -----------------------------------------------------------------------------
def auto_commit(cfg, dirpath_lwc_root):
    """
    Automatically commit changed files to the VCS.

    We want to eliminate the risk of deploying
    systems where the design is not known and
    cannot be reproduced.

    To achieve this, we ensure that each and every
    build is made from a known and managed design
    configuration in the configuration management
    system.

    To ease the administrative burden of this, we
    automatically commit changes to the local
    working copy. A strict whitelist based
    .gitignore file is used to keep unwanted files
    out of the repository.

    """
    if not cfg['options']['auto_commit']:
        return

    repo_tab = vcs_adapter.design_repo_tab(dirpath_lwc_root)

    if not any(vcs_adapter.is_modified(repo) for repo in repo_tab.values()):
        return

    (commit_msg, try_amendment) = _compose_commit_msg(cfg, dirpath_lwc_root)

    # Commit changes to subsidiary/nested repositories first.
    #
    # TODO: We do the commit even if that particular
    #       repository has not changed. Consider
    #       the consequences in regular/amendment
    #       cases.
    #
    #       Is this even a good idea? Please think
    #       about this.
    #
    #       What happens when we want to check out
    #       an old version?
    #
    #       What happens when we have a local version
    #       not present ...
    #
    repo_register = da.register.load('design_document_repository',
                                     dirpath_lwc_root = dirpath_lwc_root)

    relpath_root_repo = '.'
    for relpath in repo_tab.keys():
        if relpath != relpath_root_repo:

            if relpath not in repo_register:
                repo_register[relpath] = {
                    'configuration':    None
                }

            configuration = vcs_adapter.commit(
                                repo_tab[relpath], commit_msg, try_amendment)
            repo_register[relpath]['configuration'] = configuration

    # Update the register.
    da.register.update('design_document_repository',
                     register_data    = repo_register,
                     dirpath_lwc_root = dirpath_lwc_root)

    # Commit changes to the main / root repository.
    return vcs_adapter.commit(
                        repo_tab[relpath_root_repo], commit_msg, try_amendment)


# ------------------------------------------------------------------------------
def _compose_commit_msg(cfg, dirpath_lwc_root):
    """
    Return the commit message and an is_amendment flag.

    This function composes an appropriate commit
    message that reflects the most recent changes
    to the design as given by the latest entry in
    the current user's daybook.

    This message is returned along with a boolean
    flag that indicates if the commit is an amendment
    to a previous commit.

    """
    # Are we working on the same task as before?
    daybook_entry = da.daybook.latest_entry(
        iso_year_id      = cfg['timestamp']['iso_year_id'],
        timebox_id       = cfg['timestamp']['timebox_id'],
        date             = cfg['timestamp']['date'],
        team_member_id   = cfg['build_context']['team_member_id'],
        dirpath_lwc_root = dirpath_lwc_root)

    prev            = vcs_adapter.last_commit_message(dirpath_lwc_root)
    is_same_summary = daybook_entry['work_summary'] == prev['work_summary']
    is_same_notes   = daybook_entry['work_notes']   == prev['work_notes']
    try_amendment   = (is_same_summary and is_same_notes)

    # Keep track of when the task started.
    prev_work_start_time = prev['work_start_time']
    if try_amendment and prev_work_start_time is not None:
        work_start_time = prev_work_start_time
    else:
        work_start_time = cfg['timestamp']['timestamp_isofmt']

    commit_msg = da.commit_message.compose(daybook_entry, work_start_time)

    return (commit_msg, try_amendment)


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

        repo          = vcs_adapter.get_repo(dirpath_root)
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
        local = vcs_adapter.get_repo(dirpath_local)
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

    # assert local.head.is_detached
    if not local.head.is_detached:
        raise RuntimeError(
            'Local head should be detatched: {path}'.format(
                                                        path = dirpath_local))

    # assert not local.is_dirty()
    if local.is_dirty():
        raise RuntimeError(
            'Local repo should not be dirty: {path}'.format(
                                                        path = dirpath_local))

    # assert len(local.untracked_files) == 0
    if len(local.untracked_files) > 0:
        for untracked_filepath in local.untracked_files:
            logging.error('Untracked file found: %s', untracked_filepath)
        raise RuntimeError(
                'Untracked files found in working copy: {path}'.format(
                                                        path = dirpath_local))


# ------------------------------------------------------------------------------
def clone_all_design_documents(dirpath_destination,
                               dirpath_lwc_root,
                               configuration):
    """
    Clone all design document repositories into the specified directory.

    """
    # Clone the root repo.
    ensure_cloned(
        dirpath_local = os.path.join(dirpath_destination),
        url_remote    = os.path.join(dirpath_lwc_root),
        ref           = configuration)

    # Get the correct version of the (sub)repo register.
    repo_register = da.register.load('design_document_repository',
                                     dirpath_lwc_root = dirpath_destination)

    relpath_root_repo = '.'
    for relpath in vcs_adapter.design_repo_tab(dirpath_lwc_root).keys():
        if relpath == relpath_root_repo:
            continue
        try:
            subrepo_cfg = repo_register[relpath]['configuration']
            ensure_cloned(
                dirpath_local = os.path.join(dirpath_destination, relpath),
                url_remote    = os.path.join(dirpath_lwc_root, relpath),
                ref           = subrepo_cfg)
            logging.info('Cloned: %s at %s', relpath, subrepo_cfg)

        except ValueError as err:
            raise RuntimeError(
                'Failed to clone {relpath}\n'.format(relpath = relpath) +
                'Cause: {cause}'.format(cause = str(err)))


changed_files    = vcs_adapter.changed_files            # pylint: disable=C0103
delete_untracked = vcs_adapter.delete_untracked         # pylint: disable=C0103
