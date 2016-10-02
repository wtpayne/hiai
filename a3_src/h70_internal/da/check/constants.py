# -*- coding: utf-8 -*-
"""
Constants for conformance checking functionality.

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

# There are 5 kind of message types :
#   * (C) convention, for programming standard violation
#   * (R) refactor, for bad code smell
#   * (W) warning, for python specific problems
#   * (E) error, for probable bugs in the code
#   * (F) fatal, if an error occurred which prevented pylint from doing further

# Base id of standard checkers (used in msg and report ids):
# 01: base
# 02: classes
# 03: format
# 04: import
# 05: misc
# 06: variables
# 07: exceptions
# 08: similar
# 09: design_analysis
# 10: newstyle
# 11: typecheck
# 12: logging
# 13: string_format
# 14: string_constant
# 15: stdlib
# 16: python3
# 17-50: not yet used: reserved for future internal checkers.
# 51-99: perhaps used: reserved for external checkers

BUILD_MISSING_DESIGN_FILE       = 'E7001'
BUILD_DESIGN_SYNTAX_ERROR       = 'E7002'
BUILD_SPEC_SYNTAX_ERROR         = 'E7003'

GCC_UNKNOWN_ERROR               = 'E7101'

CLANG_UNKNOWN_ERROR             = 'E7201'

DEP_NO_CONFIG                   = 'E7301'
DEP_NO_HG_URL                   = 'E7302'
DEP_NO_GIT_URL                  = 'E7303'
DEP_REGISTER_FORMAT             = 'E7304'

SCHEMA_MISSING                  = 'E7401'
SCHEMA_FAILURE_DATA_FILE        = 'E7402'
SCHEMA_FAILURE_EMBEDDED_DATA    = 'E7403'

PYTEST_NO_SPEC                  = 'E7501'
PYTEST_NO_COVERAGE              = 'E7502'
PYTEST_NO_TEST_CLASS            = 'E7503'
PYTEST_BAD_TEST_CLASS           = 'E7504'
PYTEST_TEST_NOT_PASSED          = 'E7505'

ENGDOC_SCHEMA_FAILURE           = 'E7601'

DATA_NAME_ERR_IN_DATA_ROOT      = 'E7701'
DATA_NAME_ERR_IN_COUNTERPARTY   = 'E7702'
DATA_NAME_ERR_IN_YEAR           = 'E7703'
DATA_NAME_ERR_IN_PROJECT        = 'E7704'
DATA_NAME_ERR_IN_TIMEBOX        = 'E7705'
DATA_NAME_ERR_IN_MMDD_DATE      = 'E7706'
DATA_NAME_ERR_IN_PLATFORM       = 'E7707'
DATA_NAME_ERR_IN_RECORDING      = 'E7708'

DATA_FILE_LABELFILE_MISSING     = 'E7750'
DATA_FILE_CATALOG_MISSING       = 'E7751'

DATA_FMT_JSEQ                   = 'E7801'
DATA_FMT_YAML                   = 'E7802'
DATA_FMT_ASF                    = 'E7803'

DATA_FMT_BAD_CATALOG_FORMAT     = 'E7804'
DATA_FMT_BAD_CATALOG_CONTENT    = 'E7805'

DATA_CATALOG_NO_REC_DIR         = 'E7850'
DATA_CATALOG_NO_STREAM_FILE     = 'E7851'
DATA_CATALOG_BAD_UTC_START      = 'E7852'
DATA_CATALOG_BAD_UTC_END        = 'E7853'
DATA_CATALOG_UTC_CONSISTENCY    = 'E7854'
DATA_CATALOG_BAD_SHA256         = 'E7855'
DATA_CATALOG_BAD_SIZE_BYTES     = 'E7856'

DATA_META_BAD_FMT               = 'E7901'
