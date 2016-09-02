# -*- coding: utf-8 -*-
"""
File search utilities.

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
import re


# -----------------------------------------------------------------------------
def find_files(root,
               prefix  = None,
               suffix  = None,
               dirname = None,
               direxcl = None):
    """
    Find files.

    """
    if direxcl is None:
        direxcl = [r'^\..*$']
    pathincl_regex = r'^.*'
    if dirname is not None:
        pathincl_regex += dirname + os.sep
    if prefix is not None:
        prefix = prefix.replace('.', r'\.')
        pathincl_regex += prefix + r'.*'
    if suffix is not None:
        suffix = suffix.replace('.', r'\.')
        pathincl_regex += suffix
    pathincl_regex += r'$'
    pathincl = [pathincl_regex]

    return filtered_filepath_generator(
        root     = root,
        direxcl  = direxcl,
        pathincl = pathincl,
        pathexcl = None)


# -----------------------------------------------------------------------------
def filtered_dirpath_generator(root,
                               direxcl  = None,
                               pathincl = None,
                               pathexcl = None):
    """
    Return generator of dirpaths from root, filtered using regex lists.

    """
    return _dirpath_from_os_walk_filter(
            os_walk  = _dirname_filtered_os_walk_gen(root, direxcl = direxcl),
            pathincl = pathincl,
            pathexcl = pathexcl)


# -----------------------------------------------------------------------------
def filtered_filepath_generator(root,
                                direxcl  = None,
                                pathincl = None,
                                pathexcl = None):
    """
    Return generator of filepaths from root, filtered using regex lists.

    """
    return _filepath_from_os_walk_filter(
            os_walk  = _dirname_filtered_os_walk_gen(root, direxcl = direxcl),
            pathincl = pathincl,
            pathexcl = pathexcl)


# -----------------------------------------------------------------------------
def _dirpath_from_os_walk_filter(os_walk,
                                 pathincl = None,
                                 pathexcl = None):
    """
    Return filter of dirpaths, adapted to take an iterable of os.walk tuples.

    """
    return _filepath_regex_filter(
        _adapt_os_walk_to_dirpath(os_walk), pathincl, pathexcl)


# -----------------------------------------------------------------------------
def _filepath_from_os_walk_filter(os_walk,
                                  pathincl = None,
                                  pathexcl = None):
    """
    Return filter of filepaths, adapted to take an iterable of os.walk tuples.

    """
    return _filepath_regex_filter(
        _adapt_os_walk_to_filepath(os_walk), pathincl, pathexcl)


# -----------------------------------------------------------------------------
def _adapt_os_walk_to_dirpath(os_walk):
    """
    Return adapter converting os.walk tuple iterable into dirpath iterable.

    Intended to process the output of os_walk and dirname_filter functions.

    """
    for (current_path, dir_list, _) in os_walk:
        for dir_name in dir_list:
            yield os.path.join(current_path, dir_name)


# -----------------------------------------------------------------------------
def _adapt_os_walk_to_filepath(os_walk):
    """
    Return adapter converting os.walk tuple iterable into filepath iterable.

    Intended to process the output of os_walk and dirname_filter functions.

    """
    for (current_path, _, file_list) in os_walk:
        for file_name in file_list:
            yield os.path.join(current_path, file_name)


# -----------------------------------------------------------------------------
def _dirname_filtered_os_walk_gen(root,
                                  direxcl     = None,
                                  onerror     = None,
                                  followlinks = False):
    """
    Return generator of os.walk tuples, filtered using regex lists.

    """
    return _dirname_regex_filter(
        os_walk = os.walk(root,
                          topdown     = True,
                          onerror     = onerror,
                          followlinks = followlinks),
        excl    = direxcl)


# -----------------------------------------------------------------------------
def _dirname_regex_filter(os_walk,
                          excl = None):
    """
    Filter tuples generated by os.walk. Recursion limited by directory name.

    The supplied indicator function is used to decide if a directory subtree
    should be recursed into or not.

    """
    dirname_indicator_func = _get_dual_regex_indicator_fcn(excl = excl)
    return _dirname_filter(os_walk, dirname_indicator_func)


# -----------------------------------------------------------------------------
def _dirname_filter(os_walk, dirname_indicator_func):
    """
    Filter tuples generated by os.walk. Recursion limited by directory name.

    The supplied indicator function is used to decide if a directory subtree
    should be recursed into or not.

    """
    for (current_path, subdir_list, file_list) in os_walk:
        if not subdir_list:
            subdir_list[:] = []
        else:
            subdir_list[:] = (
                path for path in subdir_list if dirname_indicator_func(path))
        yield (current_path, subdir_list, file_list)


# -----------------------------------------------------------------------------
def _filepath_regex_filter(iter_filepaths,
                           incl = None,
                           excl = None):
    """
    Filter for filepaths, filtering specified using regex lists.

    """
    filepath_indicator_func = _get_dual_regex_indicator_fcn(incl, excl)
    return (path for path in iter_filepaths if filepath_indicator_func(path))


# -----------------------------------------------------------------------------
def _get_dual_regex_indicator_fcn(incl=None, excl=None):
    """
    Indicator function for strings based on a pair of compiled regexes.

        - Returns True if incl matches and excl does not.
        - If incl is not specified or None, it always matches (always include).
        - If excl is not specified or None, it never matches (never exclude).

    """
    is_incl = _get_regex_indicator_fcn(incl, default = True)
    is_excl = _get_regex_indicator_fcn(excl, default = False)
    return lambda item: is_incl(item) and not is_excl(item)


# -----------------------------------------------------------------------------
def _get_regex_indicator_fcn(regex_list=None, default=False):
    """
    Return an indicator function defined by the specified regular expression.

    """
    if regex_list:
        regex = _compile_regex_list(regex_list)
        return lambda item: (regex.match(item) is not None)
    else:
        return lambda item: (default)


# -----------------------------------------------------------------------------
def _compile_regex_list(regex_list):
    """
    Compile a list of regex strings into a regular expression object.

    """
    combined = "(" + ")|(".join(regex_list) + ")"
    compiled = re.compile(combined)
    return compiled


# -----------------------------------------------------------------------------
def find_ancestor_dir_containing(dir_path, marker_name, allow_dir=True):
    """
    Search for an ancestor directory of dir_path that contains a marker.

    This function identifies the closest (deepest) ancestor directory of
    dir_path that contains a file or directory named as specified by the
    marker_name parameter.

    It works by visiting each ancestor directory in dir_path in turn,
    starting at dir_path and proceeding up towards the root of the file-
    system hierarchy. At each step, it checks to see if a file or directory
    with the specified name exists. If it finds this marker, it returns
    the containing directory. If not, it continues towards the root. If,
    after reaching the root, no marker has yet been found, a SearchError
    exception is raised.

    This function was created to help identify the root of the local
    working copy, given a path within it. It should also be possible to
    use this function to help identify the root of various other filesystem
    hierarchies, given the emplacement of suitable marker files or
    directories.

    """
    for dir_path in _walk_towards_root_generator(os.path.realpath(dir_path)):
        path_marker = os.path.join(dir_path, marker_name)
        is_file     = os.path.isfile(path_marker)
        if allow_dir:
            is_dir    = os.path.isdir(path_marker)
            is_marker = is_file or is_dir
        else:
            is_marker = is_file

        if is_marker:
            return dir_path
    raise RuntimeError("Could not find marker {name}".format(
                                                        name = marker_name))


# -----------------------------------------------------------------------------
def _walk_towards_root_generator(dir_path):
    """
    Iterate over ancestor directories from dir_path up to the filesystem root.

    This function generates a sequence of directory paths starting with
    dir_path and progressively returning the parent directory of each
    until the filesystem root directory is reached.

    """
    prev_path = None
    while dir_path != prev_path:
        yield dir_path
        prev_path = dir_path
        dir_path  = os.path.dirname(dir_path)
