# -*- coding: utf-8 -*-
"""
Utility functions.

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

from . import misc

from . import importutils

__all__ = ()


# Pylint rule C0103 (invalid-name) disabled by design decision.
# the module members assigned below are functions, not constants,
# so compliant (all-caps) names would be misleading.
coroutine          = misc.coroutine                     # pylint: disable=C0103
string_types       = misc.string_types                  # pylint: disable=C0103
is_string          = misc.is_string                     # pylint: disable=C0103
index_builder_coro = misc.index_builder_coro            # pylint: disable=C0103
build_index        = misc.build_index                   # pylint: disable=C0103
walkobj            = misc.walkobj                       # pylint: disable=C0103
flatten_ragged     = misc.flatten_ragged                # pylint: disable=C0103
decompose_map      = misc.decompose_map                 # pylint: disable=C0103
write_jseq         = misc.write_jseq                    # pylint: disable=C0103
load               = misc.load                          # pylint: disable=C0103
save               = misc.save                          # pylint: disable=C0103
ensure_dir_exists  = misc.ensure_dir_exists             # pylint: disable=C0103
ensure_file_exists = misc.ensure_file_exists            # pylint: disable=C0103
merge_dicts        = misc.merge_dicts                   # pylint: disable=C0103
iter_yaml_docs     = misc.iter_yaml_docs                # pylint: disable=C0103
iter_files         = misc.iter_files                    # pylint: disable=C0103
iter_dirs          = misc.iter_dirs                     # pylint: disable=C0103
sha256             = misc.sha256                        # pylint: disable=C0103
sys_path_context   = misc.sys_path_context              # pylint: disable=C0103
sys_argv_context   = misc.sys_argv_context              # pylint: disable=C0103
import_fcn         = importutils.import_fcn             # pylint: disable=C0103
import_module_file = importutils.import_module_file     # pylint: disable=C0103
import_from_dir    = importutils.import_from_dir        # pylint: disable=C0103
