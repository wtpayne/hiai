# -*- coding: utf-8 -*-
"""
Package containing data validation schema for various engineering documents.

---
type:
    python_package

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


from good import (Any,
                  Extra,
                  Invalid,
                  Optional,
                  Reject,
                  Required,
                  Schema)

import da.check.constants
import da.util


# -----------------------------------------------------------------------------
def metadata():
    """
    Return the engineering document metadata schema.

    """
    return Schema({
        Required('_metadata'): {
            Required('document_type'):           str,
            Required('document_type_acronym'):   str,
            Optional('system_of_interest_name'): str,
            Optional('document_id'):             str,
            Optional('compilation_date'):        str,
            Optional('timebox_id'):              str,
            Optional('configuration_id'):        str,
            Optional('lifecycle_stage'):         str,
            Optional('protective_marking'):      str,
            Optional('contact_person'):          str,
            Optional('contact_email'):           str,
            Extra:                               Reject
        }
    })


# -----------------------------------------------------------------------------
def section_content():
    """
    Return the engineering document section content schema.

    """
    return Schema({
        Required('_num'):   str,
        Required('_req'):   str,
        Required('_txt'):   Any(str, None),
        Extra:              Reject
    })


# -----------------------------------------------------------------------------
def _gen_section_content(section, path = ''):
    """
    Yield content data for each section/subsection in an engineering document.

    """
    # Work out which keys are for content and which ones are subsections.
    content_keys    = set()
    subsection_keys = set()
    for key in section.keys():
        is_content = key.startswith('_')
        if is_content:
            content_keys.add(key)
        else:
            subsection_keys.add(key)

    # Collate and yield the content at this level.
    content = dict((key, section[key]) for key in content_keys)
    if content:
        yield (path, content)

    # Recurse down into subsections and yield any content there also.
    for key in subsection_keys:
        if not path:
            pathstr = key
        else:
            pathstr = path + '.' + key
        for tup in _gen_section_content(section[key], pathstr):
            yield tup


# -----------------------------------------------------------------------------
def validate(filepath, build_monitor):
    """
    Send errors to the build_monitor if sent files are not schema-compliant.

    Return False if no validation schema exists for the supplied file type.

    """
    # Engineering document content-data is held in *.docdata.yaml files.
    if not filepath.endswith('.docdata.yaml'):
        return False

    data = da.util.load(filepath)

    # Validate metadata.
    if '_metadata' in data:
        schema = metadata()
        try:
            schema(data)
        except Invalid as validation_failure:
            build_monitor.report_nonconformity(
                tool    = 'da.check.schema',
                msg_id  = da.check.constants.ENGDOC_SCHEMA_FAILURE,
                msg     = str(validation_failure),
                path    = filepath)
        return True

    # Validate content
    schema = section_content()
    for (path, content) in _gen_section_content(data):

        try:
            schema(content)
        except Invalid as validation_failure:
            msg = 'Error in: {path}\n{error}'.format(
                                            path  = path,
                                            error = str(validation_failure))
            build_monitor.report_nonconformity(
                tool    = 'da.check.schema',
                msg_id  = da.check.constants.ENGDOC_SCHEMA_FAILURE,
                msg     = msg,
                path    = filepath)
    return True
