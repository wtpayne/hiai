# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for build configuration data.

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


from good import (Extra,
                  Maybe,
                  Optional,
                  Reject,
                  Required,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def get(idclass_tab):
    """
    Return the build configuration schema.

    """
    common         = da.check.schema.common
    environment_id = idclass_tab['environment']

    build_scope = Schema({
        Optional('defined_baselines'):  [common.GIT_COMMIT_ISH],
        Optional('environment'):        [environment_id],
        Optional('restriction'):        common.BUILD_RESTRICTION,
        Extra:                          Reject
    })

    build_options = Schema({
        Optional('clean_tmp_dir'):                            bool,
        Optional('auto_commit'):                              bool,
        Optional('loglevel_overall'):                         common.LOG_LEVEL,
        Optional('loglevel_file'):                            common.LOG_LEVEL,
        Optional('loglevel_console'):                         common.LOG_LEVEL,
        Optional('enable_build_profiling'):                   bool,
        Optional('enable_build_debugger'):                    bool,
        Optional('enable_cms_registration'):                  bool,
        Optional('enable_cms_delete_old_builds'):             bool,
        Optional('cms_expiration_days'):                      int,
        Optional('check_changed_files_only'):                 bool,
        Optional('errors_abort_immediately'):                 bool,
        Optional('dep_build_exclusion'):                      Maybe(str),
        Optional('dep_build_limitation'):                     Maybe(str),
        Optional('optimisation_module'):                      Maybe(str),
        Extra:                                                Reject
    })

    build_steps = Schema({
        Optional('enable_dep_fetch_src'):                     bool,
        Optional('enable_dep_build'):                         bool,
        Optional('enable_main_build'):                        bool,
        Optional('enable_test_python_unittest'):              bool,
        Optional('enable_static_data_validation'):            bool,
        Optional('enable_static_indexing'):                   bool,
        Optional('enable_static_test_python_complexity'):     bool,
        Optional('enable_static_test_python_codestyle'):      bool,
        Optional('enable_static_test_python_docstyle'):       bool,
        Optional('enable_static_test_python_pylint'):         bool,
        Optional('enable_static_test_python_typecheck'):      bool,
        Optional('enable_compile_gcc'):                       bool,
        Optional('enable_compile_clang'):                     bool,
        Optional('enable_generate_design_docs'):              bool,
        Optional('enable_report_generation'):                 bool,
        Optional('enable_bulk_data_checks'):                  bool,
        Extra:                                                Reject
    })

    return Schema({
        Required('title'):      common.TITLE_TEXT,
        Optional('scope'):      build_scope,
        Optional('options'):    build_options,
        Optional('steps'):      build_steps,
        Extra:                  Reject
    })
