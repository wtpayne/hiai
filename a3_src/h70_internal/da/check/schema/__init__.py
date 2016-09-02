# -*- coding: utf-8 -*-
"""
Package for validation of documents and data structures against specifications.

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


import copy
import os.path

import _ast
from good import (All,
                  Any,
                  Coerce,
                  Extra,
                  Invalid,
                  Match,
                  Maybe,
                  MultipleInvalid,
                  Optional,
                  Range,
                  Reject,
                  Required,
                  Schema)

import da.check.schema.build_config
import da.check.schema.codeword_register
import da.check.schema.common
import da.check.schema.daybook_schema         # (daybook is already a module)
import da.check.schema.dependencies_register
import da.check.schema.engdoc
import da.check.schema.glossary
import da.check.schema.hilcfg
import da.check.schema.idclass_register
import da.check.schema.machine_register
import da.check.schema.milcfg
import da.check.schema.mnemonic_register
import da.check.schema.python_embedded
import da.check.schema.requirements_spec
import da.check.schema.silcfg
import da.check.schema.team_register
import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
def _validate_data_file(build_element, schema_map, error_handler):
    """
    Send errors to the error_handler if sent files are not schema-compliant.

    Return False if no validation schema exists for the supplied file type.

    """
    # Select which schema to use.
    filepath = build_element['filepath']
    schema = [schema_map[key] for key in schema_map if filepath.endswith(key)]
    if len(schema) == 0:
        return False
    else:
        assert len(schema) == 1
        schema = schema[0]

    # Validate the data file content using the selected schema.
    data = da.util.load(filepath)
    try:
        schema(data)
    except (Invalid, MultipleInvalid) as validation_failure:
        error_handler.send({
            'tool':   'da.check.schema',
            'msg_id': 'V100',
            'msg':    str(validation_failure),
            'file':   filepath,
            'line':   1,
            'col':    0
        })
    return True


# -----------------------------------------------------------------------------
def _validate_embedded_data(build_element, schema_map, error_handler):
    """
    Send errors to the error_handler if sent files are not schema-compliant.

    """
    file          = build_element['file']
    relpath       = build_element['relpath']
    filepath      = build_element['filepath']
    filename      = os.path.basename(relpath)
    (_, name_ext) = os.path.splitext(filename)

    if name_ext == '.py':

        # TODO:
        module_name = da.python_source.get_module_name(filepath)
        for (item, context) in da.python_source.iter_embedded_data(
                                            module_name = module_name,
                                            root        = build_element['ast'],
                                            file        = file):
            try:

                if isinstance(context.node, _ast.Module):
                    schema_map['python_file'](item)

                elif isinstance(context.node, _ast.FunctionDef):
                    schema_map['python_function'](item)

                elif isinstance(context.node, _ast.ClassDef):
                    schema_map['python_class'](item)

                else:
                    raise RuntimeError(
                                'No schema for {node} in {file}: '.format(
                                                    node = str(context.node),
                                                    file = relpath))

            except Invalid as validation_failure:
                error_handler.send({
                    'tool':   'da.check.schema',
                    'msg_id': 'V200',
                    'msg':    str(validation_failure),
                    'file':   filepath,
                    'line':   1,
                    'col':    0
                })
        return True

    else:  # No validation schema found for this file
        return False


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(error_handler, dirpath_lwc_root = None):
    """
    Send errors to the error_handler if sent files are not schema-compliant.

    After instantiation, for each (file, relpath, filepath) triple that is
    sent to this coroutine, any data structures held in the corresponding
    file are validated against the appropriate schema. Any errors found are
    sent to the error_handler coroutine.

    """
    common      = da.check.schema.common
    idclass_tab = common.idclass_schema(dirpath_lwc_root)

    # Schema for data files
    sch = da.check.schema
    datfile_schema = {
        '.build.yaml':                  sch.build_config.get(idclass_tab),
        '.daybook.yaml':                sch.daybook_schema.get(idclass_tab),
        '.glossary.yaml':               sch.glossary.get(),
        '.hilcfg.yaml':                 sch.hilcfg.get(),
        '.milcfg.yaml':                 sch.milcfg.get(),
        '.rspec.yaml':                  sch.requirements_spec.get(idclass_tab),
        '.silcfg.yaml':                 sch.silcfg.get(),
        'codeword.register.yaml':       sch.codeword_register.get(idclass_tab),
        'dependencies.register.json':   sch.dependencies_register.get(),
        'idclass.register.yaml':        sch.idclass_register.get(),
        'machine.register.yaml':        sch.machine_register.get(idclass_tab),
        'mnemonic.register.yaml':       sch.mnemonic_register.get(),
        'team.register.yaml':           sch.team_register.get(idclass_tab),
    }

    # Schema for data embedded in python files
    python_embedded = da.check.schema.python_embedded
    embed_schema    = {
        'python_file':      python_embedded.file_scope_schema(idclass_tab),
        'python_function':  python_embedded.function_scope_schema(idclass_tab),
        'python_class':     python_embedded.class_scope_schema(idclass_tab)
    }

    while True:

        build_element = (yield)
        filepath      = build_element['filepath']

        if da.lwc.file.is_test_data(filepath):
            continue

        if da.lwc.file.is_tool_config(filepath):
            continue

        if da.check.schema.engdoc.validate(filepath, error_handler):
            continue

        if _validate_data_file(build_element, datfile_schema, error_handler):
            continue

        if _validate_embedded_data(
                            build_element, embed_schema, error_handler):
            continue

        raise da.exception.AbortWithoutStackTrace(
            message     = 'No data validation method for: {file}'.format(
                                            file = build_element['relpath']),
            filepath    = filepath,
            line_number = 1)
