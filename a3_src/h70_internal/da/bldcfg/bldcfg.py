# -*- coding: utf-8 -*-
"""
Loading build configuration files & assembling build configuration structures.

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

import datetime
import functools
import itertools
import os
import warnings

import boltons.strutils

import da.exception
import da.lwc
import da.team
import da.machine
import da.timebox
import da.vcs


DATEFMT_DATETIME_UTC = '%Y-%m-%dT%H:%M:%S.%f'


# -----------------------------------------------------------------------------
def load_cfg(cfg_key, cfg_extras, dirpath_lwc_root):
    """
    Find or generate skeleton build configuration matching the specified name.

    This function tries to find a build configuration
    file matching CFG_NAME.

    If an exact match cannot be found, it also attempts
    fuzzy string matching to account for the possibility
    of mistyped or partially completed inputs.

    The configuration that this function returns is
    incomplete; skeletal. We wait until after the
    LWC is automatically committed to the VCS before
    adding VCS-commit-hash derived information to the
    build configuration structure.

    """
    # Is cfg_key an exact match with a build configuration file?
    (cfg_name, cfg_data, misses) = _exact_match_or_none(
                                        cfg_name         = cfg_key,
                                        dirpath_lwc_root = dirpath_lwc_root)

    if cfg_data is None:

        # Does cfg_key act like a build restriction?
        (cfg_name, cfg_data) = _build_restriction_or_none(
                                        restriction_list = [cfg_key],
                                        dirpath_lwc_root = dirpath_lwc_root)

        if cfg_data is None:

            # Does cfg_key (fuzzily) match a build
            # configuration file?
            # (One of the ones that it didn't exactly
            # match earlier).
            (cfg_name, cfg_data) = _fuzzy_match_or_none(query      = cfg_key,
                                                        candidates = misses)

            if cfg_data is None:

                # cfg_key doesn't seem to match anything. Give up.
                raise da.exception.AbortWithoutStackTrace(
                    'Could not find build configuration: {cfg_key}'.format(
                                                        cfg_key = cfg_key))

    return _assemble_cfg(
                 cfg_name         = cfg_name,
                 cfg_data         = cfg_data,
                 cfg_extras       = cfg_extras,
                 dirpath_lwc_root = dirpath_lwc_root)


# -----------------------------------------------------------------------------
def is_in_restricted_build(relpath, restriction_list):
    """
    Return true if the relpath matches the specified build restriction.

    """
    if (not restriction_list) or (not relpath):
        return False

    # We could use a glob based build restriction
    # - or even a regex?
    (dirpath_rel, filename) = os.path.split(relpath)
    (rootname, _)           = os.path.splitext(filename)
    relpath_parts           = dirpath_rel.split(os.sep)
    relpath_parts.extend([rootname, filename])

    # We could use set intersection????
    for restriction in restriction_list:
        if restriction and (restriction in relpath_parts):
            return True
    return False


# -----------------------------------------------------------------------------
def _exact_match_or_none(cfg_name, dirpath_lwc_root):
    """
    Return cfg_name and cfg_data if cfg_name matches a config file, else None.

    """
    misses = {}
    for filepath_cfg in _gen_config_files(dirpath_lwc_root):

        filename_cfg = os.path.basename(filepath_cfg)
        # Build config filename is <id>.build.yaml
        # so os.path.splitext() is not suitable here.
        id_cfgfile = filename_cfg.split('.')[0]

        if id_cfgfile == cfg_name:
            cfg_name = id_cfgfile
            cfg_data = da.util.load(filepath_cfg)
            return (cfg_name, cfg_data, misses)

        misses[id_cfgfile] = filepath_cfg

    return (None, None, misses)  # Not a build configuration file


# -----------------------------------------------------------------------------
def _build_restriction_or_none(restriction_list, dirpath_lwc_root):
    """
    Return cfg_name and cfg_data if restriction matches something, else None.

    If the restriction list can be used to succesfully
    restrict the build to one or more design elements
    or subsystems, then dynamically create a build
    configuration that uses it and return.

    The cfg_name is created by slugging the contents
    of the restriction list so we can create directories
    from it.

    For the moment we consider only design documents
    (source files) as potential matches for a build
    restriction. In future we may wish to extend this
    to counterparty names or project names so that
    we can build all systems relevant to a particular
    counterparty, or all systems relevant to a particular
    project or contract.

    """
    for filepath_src in da.lwc.discover.gen_src_files(dirpath_lwc_root):
        relpath_src = os.path.relpath(filepath_src, dirpath_lwc_root)
        if is_in_restricted_build(relpath          = relpath_src,
                                  restriction_list = restriction_list):

            cfg_name = boltons.strutils.slugify('_'.join(restriction_list))
            cfg_data = {
                'scope': {
                    'restriction': restriction_list
                }
            }

            return (cfg_name, cfg_data)

    return (None, None)  # Not a build restriction.


# -----------------------------------------------------------------------------
def _fuzzy_match_or_none(query, candidates):
    """
    Return loaded cfg if key fuzzily matches one of the candidates, else None.

    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import fuzzywuzzy.process

    (fuzzy_match, fuzzy_score)  = fuzzywuzzy.process.extractOne(
                                                query   = query,
                                                choices = candidates.keys())
    if fuzzy_score > 70:
        cfg_name = fuzzy_match
        cfg_data = da.util.load(candidates[fuzzy_match])
        return (cfg_name, cfg_data)

    else:
        return (None, None)  # Not a fuzzy match


# -----------------------------------------------------------------------------
def _gen_config_files(dirpath_lwc_root):
    """
    Generate all build config filepaths under the specified directory.

    """
    _pathto          = functools.partial(da.lwc.discover.path,
                                         dirpath_lwc_root = dirpath_lwc_root)
    _gen_cfgfiles_in = functools.partial(da.lwc.search.find_files,
                                         suffix           = '.build.yaml')
    return itertools.chain(_gen_cfgfiles_in(_pathto('bldcfg')),
                           _gen_cfgfiles_in(_pathto('internal')))


# -----------------------------------------------------------------------------
def _assemble_cfg(cfg_name, cfg_data, cfg_extras, dirpath_lwc_root):
    """
    Create configuration structure.

    """
    # We always load the default configuration file.
    # If another custom confiugration file is specified,
    # we load that one too, and allow it to selectively
    # override whatever default values it wishes to.
    # If any custom configuration is provided by the
    # command line, this takes priority over both of
    # the above.
    #
    dirpath_internal     = da.lwc.discover.path(
                                        key              = 'internal',
                                        dirpath_lwc_root = dirpath_lwc_root)
    dirpath_cfg          = os.path.join(dirpath_internal, 'da', 'bldcfg')
    filepath_default_cfg = os.path.join(dirpath_cfg, 'default.build.yaml')

    cfg = da.util.load(filepath_default_cfg)        # default config file.

    if not cfg_name == 'default':
        cfg = da.util.merge_dicts(cfg, cfg_data)    # custom config file.

    cfg = da.util.merge_dicts(cfg, cfg_extras)      # command line config.

    cfg['cfg_name'] = cfg_name

    cfg = da.util.merge_dicts(cfg,
                            {'paths': {'dirpath_lwc_root': dirpath_lwc_root}})

    cfg = da.util.merge_dicts(cfg, _create_timestamps(cfg))

    cfg = da.util.merge_dicts(cfg, _create_build_context_record(cfg))

    cfg = da.util.merge_dicts(cfg, _create_paths_record(cfg))

    return cfg


# -----------------------------------------------------------------------------
def _create_build_context_record(cfg):
    """
    Create  the host environment record part of the configuration structure.

    """
    dirpath_lwc_root = cfg['paths']['dirpath_lwc_root']
    hostname         = da.machine.gethostname()
    machine_id       = da.machine.machine_id(dirpath_lwc_root)
    env_id           = da.machine.env_id()
    team_member_id   = da.team.member_id(dirpath_lwc_root)

    return {
        'build_context': {
            'hostname':       hostname,
            'machine_id':     machine_id,
            'env_id':         env_id,
            'team_member_id': team_member_id,
        }
    }


# -----------------------------------------------------------------------------
def _create_timestamps(cfg):
    """
    Create the timestamps part of the configuration structure.

    """
    # Record the time & date of the meta-build in various forms.
    if 'timestamp' in cfg and 'datetime_utc' in cfg['timestamp']:
        datetime_utc = cfg['timestamp']['datetime_utc']
    else:
        datetime_utc = datetime.datetime.utcnow()

    date             = '{year:04d}{month:02d}{day:02d}'.format(
                                        year   = datetime_utc.year,
                                        month  = datetime_utc.month,
                                        day    = datetime_utc.day)

    day_of_month     = '{day:02d}'.format(
                                        day    = datetime_utc.day)

    timestamp_isofmt = datetime_utc.isoformat()

    timestamp_utc    = '{utc_hh:02d}{utc_mm:02d}{utc_ss:02d}'.format(
                                        utc_hh = datetime_utc.hour,
                                        utc_mm = datetime_utc.minute,
                                        utc_ss = datetime_utc.second)

    short_time_utc   = '{utc_hh:02d}{utc_mm:02d}'.format(
                                        utc_hh = datetime_utc.hour,
                                        utc_mm = datetime_utc.minute)

    timebox_id       = da.timebox.ident(datetime_utc)

    (iso_year,
     iso_week,
     iso_day)        = datetime_utc.isocalendar()

    iso_year_id      = '{iso_year:04d}'.format(iso_year = iso_year)

    iso_day_id       = '{iso_week:02d}{iso_day:01d}'.format(
                                        iso_week = iso_week,
                                        iso_day  = iso_day)

    return {
        'timestamp': {
            'date':             date,
            'timestamp_isofmt': timestamp_isofmt,
            'timestamp_utc':    timestamp_utc,
            'iso_year':         iso_year,
            'iso_week':         iso_week,
            'iso_day':          iso_day,
            'iso_year_id':      iso_year_id,
            'iso_day_id':       iso_day_id,
            'day_of_month':     day_of_month,
            'short_time_utc':   short_time_utc,
            'timebox_id':       timebox_id
        }
    }


# -----------------------------------------------------------------------------
def _create_paths_record(cfg):
    """
    Create the filesystem paths part of the configuration structure.

    """
    dirpath_lwc_root = cfg['paths']['dirpath_lwc_root']
    rootpath_tmp     = da.lwc.discover.path(
                                        key              = "tmp",
                                        dirpath_lwc_root = dirpath_lwc_root)
    rootpath_cms     = da.lwc.discover.path(
                                        key              = "cms",
                                        dirpath_lwc_root = dirpath_lwc_root)

    cfg_name         = cfg['cfg_name']
    dirpath_meta_tmp = os.path.join(rootpath_tmp, cfg_name)
    dirpath_meta_log = os.path.join(dirpath_meta_tmp, 'log')
    dirpath_meta_cms = os.path.join(rootpath_cms,
                                    cfg['timestamp']['iso_year_id'],
                                    cfg['timestamp']['timebox_id'],
                                    cfg_name)
    return {
        'paths': {
            'dirpath_lwc_root':     dirpath_lwc_root,
            'rootpath_tmp':         rootpath_tmp,
            'rootpath_cms':         rootpath_cms,
            'dirpath_meta_tmp':     dirpath_meta_tmp,
            'dirpath_meta_log':     dirpath_meta_log,
            'dirpath_meta_cms':     dirpath_meta_cms
        }
    }
