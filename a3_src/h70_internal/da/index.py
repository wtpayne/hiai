# -*- coding: utf-8 -*-
"""
Identifier traceability indexing functions.

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

import itertools
import os
import re

import yaml

import da.idclass
import da.python_source
import da.util
import da.util.marked_yaml


# -----------------------------------------------------------------------------
def iter_embed_data(file, relpath):
    """
    Return an iterator yielding embedded data structures in the specified file.

    """
    if relpath.endswith('.yaml'):
        for item in yaml.load_all(file, Loader = da.util.marked_yaml.Loader):
            yield (item, None)

    elif relpath.endswith('.py'):
        return


# -----------------------------------------------------------------------------
def write(indices, dirpath_idxfiles):
    """
    Persist supplied index data to disk.

    Build a mapping from an identifier string to
    the locations (file/row/col) where that
    identifier string occurs.

    data[idclass][idstr][filepath] -> (iline, icol)

    """
    (line_index, references_index, objects_index) = indices

    # Check for duplicate identifier numbers or descriptions.
    for idclass, classdata in line_index.items():
        set_nums  = set()
        set_descs = set()
        for idstr in sorted(classdata.keys()):
            (idnum, description) = idstr.split('_', maxsplit = 1)
            if idnum in set_nums:
                raise RuntimeError(
                    'Duplicate identifier num: "{idnum}" in "{idstr}"'.format(
                                                        idnum = idnum,
                                                        idstr = idstr))
            if description in set_descs:
                raise RuntimeError(
                    'Duplicate description: "{desc}" in "{idstr}"'.format(
                                                        desc  = description,
                                                        idstr = idstr))

            set_nums.add(idnum)
            set_descs.add(description)

    # Persist all indices to disk.
    da.util.ensure_dir_exists(dirpath_idxfiles)
    for idclass, classdata in line_index.items():
        filename  = '{idclass}.line_index.jseq'.format(idclass = idclass)
        da.util.write_jseq(os.path.join(dirpath_idxfiles, filename),
                           itertools.starmap(lambda k, v: {k: v},
                                             sorted(classdata.items())))

    if references_index is not None:
        for idclass, classdata in references_index.items():
            filename = '{idclass}.references_index.jseq'.format(
                                                            idclass = idclass)
            da.util.write_jseq(os.path.join(dirpath_idxfiles, filename),
                               itertools.starmap(lambda k, v: {k: v},
                                                 sorted(classdata.items())))
    if objects_index is not None:
        for idclass, classdata in objects_index.items():
            filename = '{idclass}.objects_index.jseq'.format(
                                                            idclass = idclass)
            da.util.write_jseq(os.path.join(dirpath_idxfiles, filename),
                               itertools.starmap(lambda k, v: {k: v},
                                                 sorted(classdata.items())))

    return True


# -----------------------------------------------------------------------------
# TODO: Refactor to reduce number of branches.
#       (Rule disabled to facilitate tightening of the threshold)
@da.util.coroutine
def index_coro(dirpath_lwc_root, indices = None):       # pylint: disable=R0912
    """
    Yield mappings corresponding to the sent sequence of multi-key tuples.

    """
    if indices is not None:
        (line_index, references_index, objects_index) = indices
    else:
        line_index       = None
        references_index = None
        objects_index    = None

    line_idx_builder       = da.util.index_builder_coro(line_index)
    references_idx_builder = da.util.index_builder_coro(references_index)
    objects_idx_builder    = da.util.index_builder_coro(objects_index)
    matcher                = _id_matcher_coro(dirpath_lwc_root)

    while True:

        indices    = (line_index, references_index, objects_index)
        build_unit = (yield indices)
        file       = build_unit['file']
        relpath    = build_unit['relpath']

        # The first pass over the file is for
        # relatively unsophisticated indexing
        # - not accounting for any formatting
        # of the file other than the presence
        # of newline delimiters.
        #
        file.seek(0)
        for iline, binary_line in enumerate(file):
            text_line = binary_line.decode('utf-8')
            for (match_class, idstr,
                 line_offset, col_offset) in matcher.send(text_line):
                line_num   = 1 + iline + line_offset
                col_num    = 1 + col_offset
                pos        = (line_num, col_num)
                line_index = line_idx_builder.send((match_class,
                                                     idstr,
                                                     relpath,
                                                     pos))

        # The second pass over the file takes
        # account of the file format - We try
        # to parse the file to identify the
        # context within which each identifier
        # is placed.
        #
        file.seek(0, os.SEEK_SET)

        # YAML files are grist to the mill --
        # any part of a YAML data structure
        # is potentially of interest to us.
        #
        if relpath.endswith('yaml'):
            for data in yaml.load_all(file,
                                      Loader = da.util.marked_yaml.Loader):

                (maybe_ref_idx, maybe_obj_idx) = _index_yaml(
                                                        references_idx_builder,
                                                        objects_idx_builder,
                                                        matcher,
                                                        relpath,
                                                        data)
                if maybe_ref_idx is not None:
                    references_index = maybe_ref_idx
                if maybe_obj_idx is not None:
                    objects_index    = maybe_obj_idx

        # We are only really interested in YAML or
        # JSON structures that are embedded in
        # comments or docstrings within the Python
        # source document.
        #
        # ---
        # i00022_store_requirements_in_python_source_documents:
        #   - "The system SHALL extract and process requirement clauses stored
        #     as comments in Python source documents."
        #   - notes: "We want to encourage the use of requirements to document
        #            both top-down and bottom-up aspects of the design process.
        #            Allowing requirement clauses to be stored as comments in
        #            source files makes it much easier for developers to create
        #            bottom-up requirements. Additionally, by placing the
        #            requirements next to the site of the implementation makes
        #            it leess likely that requirements will be forgotten or
        #            ignored."
        #   - type: mandate
        #   - state: draft
        # ...
        if relpath.endswith('py'):
            pass
        # for data in da.python_source.iter_embedded_data(file, relpath):
        #     (maybe_ref_idx, maybe_obj_idx) = _index_yaml(
        #                                             references_idx_builder,
        #                                             objects_idx_builder,
        #                                             matcher,
        #                                             relpath,
        #                                             data)
        #     if maybe_ref_idx is not None:
        #         references_index = maybe_ref_idx
        #     if maybe_obj_idx is not None:
        #         objects_index    = maybe_obj_idx


# -----------------------------------------------------------------------------
def _index_yaml(
        references_idx_builder, objects_idx_builder, matcher, relpath, data):
    """
    Return indices built using the specified nested line-marked mapping object.

    """
    references_index = None
    objects_index    = None

    for (path, obj) in da.util.walkobj(data, gen_leaf    = False,
                                             gen_nonleaf = True,
                                             gen_path    = True,
                                             gen_obj     = True):

        if not hasattr(obj, 'start_mark'):
            continue

        obj_line   = 1 + obj.start_mark.line
        obj_column = 1 + obj.start_mark.column
        if da.util.is_string(obj):
            for (match_class, idstr, line_offset, col_offset) in matcher.send(
                                                                        obj):

                line_num         = obj_line   + line_offset
                col_num          = obj_column + col_offset
                pos              = (line_num, col_num)
                references_index = references_idx_builder.send((match_class,
                                                                  idstr,
                                                                  relpath,
                                                                  str(pos),
                                                                  path))

        name = path[-1]
        if da.util.is_string(name):
            for (match_class, idstr, line_offset, col_offset) in matcher.send(
                                                                        name):

                line_num      = 1 + obj_line   + line_offset
                col_num       = 1 + obj_column + col_offset
                pos           = (line_num, col_num)
                objects_index = objects_idx_builder.send(
                    (match_class, idstr, relpath, str(pos), str(path), obj))

    return (references_index, objects_index)


# -----------------------------------------------------------------------------
@da.util.coroutine
def _id_matcher_coro(dirpath_lwc_root):
    """
    Yield identifier strings that have been found in the sent blocks of text.

    For each text block sent to this coroutine, it
    yields a list of identifier strings.

    """
    exception_list = ['x86_64',
                      'd3_array',
                      'd3_brush',
                      'd3_drag',
                      'd3_dsv',
                      'd3_force',
                      'd3_hcg',
                      'd3_hexbin',
                      'd3_hierarchy',
                      'd3_hsv',
                      'd3_interpolate',
                      'd3_path',
                      'd3_sankey',
                      'd3_scale',
                      'd3_selection',
                      'd3_tile',
                      'd3_time',
                      'd3_timer',
                      'd3_transition',
                      'd3_zoom']
    regextab       = da.idclass.regex_table(dirpath_lwc_root)
    regex_generic  = re.compile(
                        r"\b[a-zA-Z]{1,2}[0-9]{1,12}_[a-zA-Z0-9_]{2,200}")
    matchlist      = []

    while True:

        text      = (yield matchlist)
        matchlist = []

        for match in regex_generic.finditer(text):

            idstr  = match.group(0)
            istart = match.start()
            if istart == 0:
                line_offset = 0
                col_offset  = 0
            else:
                prev_lines  = text[:istart].splitlines()
                line_offset = len(prev_lines) - 1
                col_offset  = len(prev_lines[-1])

            # We can (will) make this a lot faster in future ... but
            # for now it serves well enough.
            is_exact = False
            for idclass, idregex in regextab.items():
                if idregex.match(idstr):
                    is_exact = True
                    matchlist.append((idclass, idstr, line_offset, col_offset))
                    break

            # If we find something that is plausibly
            # an identifier, but does not exactly
            # match any of our identifier classes,
            # then we have probably got a malformed
            # identifier of some sort (likely due
            # to a typo), so we raise an exception
            # to let the developer fix it, (or else
            # add it to the whitelist)
            #
            if (not is_exact) and (idstr not in exception_list):
                raise RuntimeError(
                        'Possibly malformed id: %s', idstr)
