# -*- coding: utf-8 -*-
"""
Module for validation of embedded data structures in python files.

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
                  Optional,
                  Reject,
                  Required,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def file_metadata_schema(idclass_tab):
    """
    Return the data validation schema for python file metadata.

    """
    hiai_copyright = Schema(
        'Copyright 2016 High Integrity Artificial Intelligence Systems')

    hashdist_copyright = Schema(
        'Copyright 2012, Dag Sverre Seljebotn and Ondrej Certik')

    apache_license_v2 = Schema(
        'Licensed under the Apache License, Version 2.0 '
        '(the License); you may not use this file except in compliance '
        'with the License. You may obtain a copy of the License at\n'
        'http://www.apache.org/licenses/LICENSE-2.0\n'
        'Unless required by applicable law or agreed to in writing, '
        'software distributed under the License is distributed on an '
        'AS IS BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, '
        'either express or implied. See the License for the specific '
        'language governing permissions and limitations under the '
        'License.')

    bsd_3_clause_license = (
        'Licensed under the BSD 3-clause license.\n'
        'Redistribution and use in source and binary forms, with or without '
        'modification, are permitted provided that the following conditions '
        'are met:\n'

        'Redistributions of source code must retain the above copyright '
        'notice, this list of conditions and the following disclaimer.\n'

        'Redistributions in binary form must reproduce the above '
        'copyright notice, this list of conditions and the following '
        'disclaimer in the documentation and/or other materials provided '
        'with the distribution.\n'

        'Neither the name of the copyright holders nor the names of '
        'other contributors may be used to endorse or promote products '
        'derived from this software without specific prior written '
        'permission.\n'

        'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS '
        'AS IS AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT '
        'LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS '
        'FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE '
        'COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, '
        'INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, '
        'BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; '
        'LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER '
        'CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT '
        'LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN '
        'ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE '
        'POSSIBILITY OF SUCH DAMAGE.')

    protection_level = idclass_tab['protection_level']
    validation_level = idclass_tab['validation_level']

    return Schema({

        Required('type'):               Any('python_module',
                                            'python_package'),

        Required('validation_level'):   validation_level,

        Required('protection'):         protection_level,

        Required('copyright'):          Any(hiai_copyright,
                                            hashdist_copyright),

        Required('license'):            Any(apache_license_v2,
                                            bsd_3_clause_license),

        Extra:                          Reject

    })


# -----------------------------------------------------------------------------
def function_metadata_schema():
    """
    Return the data validation schema for python function metadata.

    """
    return Schema({
        'type':                     Any('function',
                                        'generator',
                                        'constructor'),
        'args': {
                                    da.check.schema.common.LOWERCASE_NAME: str
        },
        Optional('yields'):         str,
        Optional('preconditions'):  [str],
        Optional('side_effects'):   [str],
    })


# -----------------------------------------------------------------------------
def class_metadata_schema():
    """
    Return the data validation schema for python class metadata.

    """
    return Schema({
        'type':         'class',
        'attributes':   { da.check.schema.common.LOWERCASE_NAME: str }
    })


# -----------------------------------------------------------------------------
def file_scope_schema(idclass_tab):
    """
    Return the validation schema for data within python module scope.

    """
    return Schema(Any(

        Required(file_metadata_schema(idclass_tab)),

        Optional(da.check.schema.common.requirement_set_schema(idclass_tab))

    ))


# -----------------------------------------------------------------------------
def class_scope_schema(idclass_tab):
    """
    Return the validation schema for data within python class scope.

    """
    return Schema(Any(

        Required(class_metadata_schema()),

        Optional(da.check.schema.common.requirement_set_schema(idclass_tab))

    ))


# -----------------------------------------------------------------------------
def function_scope_schema(idclass_tab):
    """
    Return the validation schema for data within python function scope.

    """
    return Schema(Any(

        Required(function_metadata_schema()),

        Optional(da.check.schema.common.requirement_set_schema(idclass_tab))

    ))
