# -*- coding: utf-8 -*-
"""
Report generation functions.

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


import os.path

import markdown
import mdx_gfm

import da.index
import da.util
from . import docx_builder
from . import html_builder


# Standard engineering document types.
_DOCUMENT_TYPES = [
    'com',   # mil-std-498 - Computer operation manual.
    'cpm',   # mil-std-498 - Computer programming manual.
    'dbdd',  # mil-std-498 - Database design description.
    'fsm',   # mil-std-498 - Firmware support manual.
    'idd',   # mil-std-498 - Interface design description.
    'irs',   # mil-std-498 - Interface requirements specification.
    'ocd',   # mil-std-498 -    Operational concept description.
    'pip',   # smc-s-012   - Process improvement plan.
    'sad',   # smc-s-012   - Software architecture description.
    'scom',  # mil-std-498 - Software center operator manual.
    'sdd',   # mil-std-498 - Software design description.
    'sdp',   # smc-s-012   -    Software development plan.
    'siom',  # mil-std-498 - Software input output manual.
    'sip',   # mil-std-498 - Software installation plan.
    'smbp',  # smc-s-012   - Software master build plan.
    'smp',   # smc-s-012   - Software measurement plan.
    'smr',   # smc-s-012   - Software measurement report.
    'sps',   # mil-std-498 - Software product specification.
    'srs',   # mil-std-498 - Software requirement specification.
    'ssdd',  # mil-std-498 - System/subsystem design description.
    'sss',   # mil-std-498 - System/subsystem specification.
    'std',   # mil-std-498 - Software test description.
    'stp',   # mil-std-498 - Software test plan.
    'str',   # mil-std-498 - Software test report.
    'strp',  # mil-std-498 - Software transition plan.
    'sum',   # mil-std-498 - Software user manual.
    'svd']   # mil-std-498 - Software version description.


# -----------------------------------------------------------------------------
def metabuild(_):
    """
    Generate metabuild reports.

    These reports compare and contrast multiple builds.

    """
    pass


# -----------------------------------------------------------------------------
def build(cfg, build_data):
    """
    Generate reports and documentation for a subsidiary build.

    """
    dirpath_log = cfg['paths']['dirpath_branch_log']
    da.util.ensure_dir_exists(dirpath_log)

    if build_data is not None:
        da.index.write(build_data, dirpath_log)

    _create_engineering_documents(cfg)
    return True


# -----------------------------------------------------------------------------
def _create_engineering_documents(cfg):
    """
    Create and save all engineering documents.

    """
    # TODO: Consider if we want to filter what gets generated?
    #       Why isn't this being driven by the main loop?
    #       How do we do incremental documentation builds?
    for (relpath, doc_type, data) in _gen_doc_data(cfg):
        (filepath_docx, filepath_html) = _get_document_paths(
                                                        cfg, relpath, doc_type)
        section_list = _get_sorted_sections(data)
        docx_builder.build(data, section_list, filepath_docx)
        html_builder.build(data, section_list, filepath_html)


# -----------------------------------------------------------------------------
def _get_sorted_sections(data):
    """
    Return a sorted list of the sections in the provided document data.

    """
    return sorted(_gen_sections(data), key = _section_sortkey)


# -----------------------------------------------------------------------------
def _section_sortkey(section):
    """
    Return the sort-key for a document section.

    """
    try:
        parts_list = section['num'].split('.')
        return list('%06d' % int(part) for part in parts_list)
    except ValueError:
        return list(section['num'])


# -----------------------------------------------------------------------------
def _gen_sections(data):
    """
    Yield each section in the provided document data.

    """
    for (path, item) in da.util.walkobj(data,
                                        gen_nonleaf = True,
                                        gen_path    = True,
                                        gen_obj     = True):
        if '_metadata' in path:
            continue

        # All valid sections will have a _num field.
        try:
            section_num = item['_num']
        except TypeError:
            continue

        # Not sure if this is relevant any more ...
        # What do we do with _req anyway???
        if '_txt' in item:
            section_type   = '_txt'
        elif '_req' in item:
            section_type   = '_req'
        else:
            raise RuntimeError('Could not determine section type.')

        # Empty paragraphs.
        # (Remove here or in individual rendereds?)
        is_empty = (    not item[section_type]
                     or item[section_type] == 'TBD\n'
                     or item[section_type] == 'NONE\n')
        if is_empty:
            paragraph_list = []
        else:
            paragraph_list = [item[section_type]]

        # Convert github-flavour-markdown paragraphs to html,
        gfm_extn  = mdx_gfm.GithubFlavoredMarkdownExtension()
        mkdn      = markdown.Markdown(extensions = [gfm_extn])
        html_list = [mkdn.convert(para) for para in paragraph_list]

        yield {
            'level':  section_num.count('.')  + 1,
            'title':  path[-1].replace('_', ' ').capitalize(),
            'num':    section_num,
            'type':   section_type,
            'para':   paragraph_list,
            'html':   html_list}


# -----------------------------------------------------------------------------
def _get_document_paths(cfg, relpath, doc_type):
    """
    Return filepaths for the engineering documents we are about to create.

    """
    dirpath_doc   = os.path.join(
                        cfg['paths']['dirpath_branch_log'], relpath, doc_type)
    doc_id        = _get_document_id(cfg, relpath, doc_type)
    filename_docx = '{doc_id}.docx'.format(doc_id = doc_id)
    filename_html = '{doc_id}.html'.format(doc_id = doc_id)
    filepath_docx = os.path.join(dirpath_doc, filename_docx)
    filepath_html = os.path.join(dirpath_doc, filename_html)
    return (filepath_docx, filepath_html)


# -----------------------------------------------------------------------------
def _gen_doc_data(cfg):
    """
    Yield document data for each project and document type.

    """
    for doc_type in _DOCUMENT_TYPES:
        for (relpath, data) in _gen_doc_data_for_type(cfg, doc_type):
            data['_metadata'].update(_get_metadata(cfg, relpath, doc_type))
            yield (relpath, doc_type, data)


# -----------------------------------------------------------------------------
def _get_metadata(cfg, relpath, doc_type):
    """
    Return document metadata for the specified document type.

    """
    return {
        'document_id':        _get_document_id(cfg, relpath, doc_type),
        'compilation_date':   cfg['timestamp']['date'],
        'timebox_id':         cfg['timestamp']['timebox_id'],
        'configuration_id':   cfg['defined_baseline']['short_hexsha']}


# -----------------------------------------------------------------------------
def _get_document_id(_, relpath, doc_type):
    """
    Return the document id for the specified document type.

    """
    # TODO: Decide if it is valid to have a situation when relpath is not a
    #       relpath to a project ... i.e. we have a document that is not
    #       associated with a counterparty and project !?!?
    (counterparty_id, _, project_id) \
                        = _parse_project_path(relpath_project = relpath)
    counterparty_number = counterparty_id.split('_')[0]
    project_number      = project_id.split('_')[0]
    document_id         = '{pfix}_{cpty}_{proj}_{doc_type}'.format(
                                 pfix     = 'da',
                                 cpty     = counterparty_number,
                                 proj     = project_number,
                                 doc_type = doc_type)
    return document_id


# -----------------------------------------------------------------------------
def _parse_project_path(relpath_project):
    """
    Return the counterparty id, year and project id from a project path.

    """
    (relpath_year, project_id) = os.path.split(relpath_project)
    (relpath_cpty, project_yr) = os.path.split(relpath_year)
    counterparty_id            = os.path.basename(relpath_cpty)

    return (counterparty_id, project_yr, project_id)


# -----------------------------------------------------------------------------
def _gen_doc_data_for_type(cfg, doc_type):
    """
    Yield document data for each project and the specified document type.

    """
    dirpath_lwc_root     = cfg['paths']['dirpath_lwc_root']
    dirpath_isolated_src = cfg['paths']['dirpath_isolated_src']
    default_data         = _load_default_doc_data(
                                        cfg, doc_type, dirpath_isolated_src)
    if default_data:
        for (relpath, custom_data) in _gen_custom_doc_data(
                                        cfg, doc_type, dirpath_lwc_root):

            data = da.util.merge_dicts(default_data, custom_data)
            yield (relpath, data)


# -----------------------------------------------------------------------------
def _load_default_doc_data(_, doc_type, dirpath_lwc_root):
    """
    Return default data for the specified document type.

    """
    rootpath_doc = da.lwc.discover.path(
                                    'doc', dirpath_lwc_root = dirpath_lwc_root)
    dirpath_doc  = os.path.join(rootpath_doc, 'default', doc_type)
    data         = {}
    if os.path.isdir(dirpath_doc):
        for filepath in da.lwc.search.find_files(root     = dirpath_doc,
                                                 prefix   = doc_type,
                                                 suffix   = 'docdata.yaml'):
            data = da.util.merge_dicts(data, da.util.load(filepath))
    return data


# -----------------------------------------------------------------------------
def _gen_custom_doc_data(_, doc_type, dirpath_lwc_root):
    """
    Yield custom data for each project and the specified document type.

    """
    for dirpath in da.lwc.discover.gen_project_dirs(dirpath_lwc_root):

        data    = {}
        relpath = os.path.relpath(dirpath, dirpath_lwc_root)
        for filepath in da.lwc.search.find_files(root     = dirpath,
                                                 prefix   = doc_type,
                                                 suffix   = 'docdata.yaml'):
            data = da.util.merge_dicts(data, da.util.load(filepath))
        yield (relpath, data)
