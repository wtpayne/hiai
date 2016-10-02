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

import da.check.constants
import da.check.schema.build_config
import da.check.schema.bulk_data_catalog
import da.check.schema.bulk_data_label
import da.check.schema.codeword_register
import da.check.schema.common
import da.check.schema.coordinate_systems_register
import da.check.schema.dataflow
import da.check.schema.daybook_schema         # (daybook is already a module)
import da.check.schema.dependencies_register
import da.check.schema.design_document_repository_register
import da.check.schema.engdoc
import da.check.schema.glossary
import da.check.schema.hilcfg
import da.check.schema.idclass_register
import da.check.schema.lifecycle_product_register
import da.check.schema.lifecycle_product_class_register
import da.check.schema.machine_register
import da.check.schema.milcfg
import da.check.schema.mnemonic_register
import da.check.schema.process_register
import da.check.schema.process_class_register
import da.check.schema.python_embedded
import da.check.schema.requirements_spec
import da.check.schema.silcfg
import da.check.schema.team_register
import da.lwc.file
import da.util


# -----------------------------------------------------------------------------
def _validate_data_file(build_unit, schema_map, build_monitor):
    """
    Send errors to the build_monitor if sent files are not schema-compliant.

    Return False if no validation schema exists for the supplied file type.

    """
    # Select which schema to use.
    filepath = build_unit['filepath']
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
        build_monitor.report_nonconformity(
            tool    = 'da.check.schema',
            msg_id  = da.check.constants.SCHEMA_FAILURE_DATA_FILE,
            msg     = str(validation_failure),
            path    = filepath)
    return True


# -----------------------------------------------------------------------------
def _validate_embedded_data(build_unit, schema_map, build_monitor):
    """
    Send errors to the build_monitor if sent files are not schema-compliant.

    """
    file          = build_unit['file']
    relpath       = build_unit['relpath']
    filepath      = build_unit['filepath']
    filename      = os.path.basename(relpath)
    (_, name_ext) = os.path.splitext(filename)

    if name_ext == '.py':

        # TODO:
        module_name = da.python_source.get_module_name(filepath)
        for (item, context) in da.python_source.iter_embedded_data(
                                            module_name = module_name,
                                            root        = build_unit['ast'],
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
                build_monitor.report_nonconformity(
                    tool    = 'da.check.schema',
                    msg_id  = da.check.constants.SCHEMA_FAILURE_EMBEDDED_DATA,
                    msg     = str(validation_failure),
                    path    = filepath)

        return True

    else:  # No validation schema found for this file
        return False


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(build_monitor, dirpath_lwc_root = None):
    """
    Send errors to the build_monitor if sent files are not schema-compliant.

    After instantiation, for each (file, relpath, filepath) triple that is
    sent to this coroutine, any data structures held in the corresponding
    file are validated against the appropriate schema. Any errors found are
    sent to the build_monitor coroutine.

    """
    common      = da.check.schema.common
    idclass_tab = common.idclass_schema(dirpath_lwc_root)

    # Schema for data files
    sch = da.check.schema
    datfile_schema = {

        '.build.yaml':
            sch.build_config.get(idclass_tab),

        '.dataflow.yaml':
            da.check.schema.dataflow.get(),

        '.daybook.yaml':
            sch.daybook_schema.get(idclass_tab),

        '.glossary.yaml':
            sch.glossary.get(),

        '.hilcfg.yaml':
            sch.hilcfg.get(),

        '.milcfg.yaml':
            sch.milcfg.get(),

        '.rspec.yaml':
            sch.requirements_spec.get(idclass_tab),

        '.silcfg.yaml':
            sch.silcfg.get(),

        'codeword.register.yaml':
            sch.codeword_register.get(idclass_tab),

        'coordinate_systems.register.yaml':
            sch.coordinate_systems_register.get(idclass_tab),

        'dependencies.register.json':
            sch.dependencies_register.get(),

        'design_document_repository.register.yaml':
            sch.design_document_repository_register.get(),

        'idclass.register.yaml':
            sch.idclass_register.get(),

        'lifecycle_product.register.yaml':
            sch.lifecycle_product_register.get(idclass_tab),

        'lifecycle_product_class.register.yaml':
            sch.lifecycle_product_class_register.get(idclass_tab),

        'machine.register.yaml':
            sch.machine_register.get(idclass_tab),

        'mnemonic.register.yaml':
            sch.mnemonic_register.get(),

        'process.register.yaml':
            sch.process_register.get(idclass_tab),

        'process_class.register.yaml':
            sch.process_class_register.get(idclass_tab),

        'team.register.yaml':
            sch.team_register.get(idclass_tab),
    }

    # Schema for data embedded in python files
    python_embedded = da.check.schema.python_embedded
    embed_schema    = {
        'python_file':      python_embedded.file_scope_schema(idclass_tab),
        'python_function':  python_embedded.function_scope_schema(idclass_tab),
        'python_class':     python_embedded.class_scope_schema(idclass_tab)
    }

    while True:

        build_unit = (yield)
        filepath   = build_unit['filepath']

        if da.lwc.file.is_test_data(filepath):
            continue

        if da.lwc.file.is_tool_config(filepath):
            continue

        # No checking for CSS.
        if filepath.endswith('.css'):
            continue

        # No checking for bash scripts.
        if filepath.endswith('.bash'):
            continue

        # No checking for HTML templates.
        if filepath.endswith('.template.html'):
            continue

        if da.check.schema.engdoc.validate(filepath, build_monitor):
            continue

        if _validate_data_file(build_unit, datfile_schema, build_monitor):
            continue

        if _validate_embedded_data(
                            build_unit, embed_schema, build_monitor):
            continue

        build_monitor.report_nonconformity(
            tool    = 'da.check.schema',
            msg_id  = da.check.constants.SCHEMA_MISSING,
            msg     = 'No data validation method or schema for: {file}'.format(
                                                            file = filepath),
            path    = filepath)
