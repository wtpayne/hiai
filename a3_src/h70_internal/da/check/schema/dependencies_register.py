# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for the dependencies register.

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
                  Reject,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def get():
    """
    Return the data validation schema for the dependencies register.

    """
    common = da.check.schema.common
    api_iface_name = Any('include',
                         'lib_native',
                         'lib_javascript',
                         'lib_python2',
                         'lib_python3')
    api_config = Any({}, {api_iface_name:        common.LOWERCASE_PATH})
    cli_config = Any({}, {common.LOWERCASE_NAME: common.LOWERCASE_PATH})
    gui_config = Any({}, {common.LOWERCASE_NAME: common.LOWERCASE_PATH})

    return Schema({
        'title':                        common.TITLE_TEXT,

        'introduction':                 common.PARAGRAPH_TEXT,

        'register': {

            common.LOWERCASE_NAME: {
                'desc':                 Any('TBD', common.SUMMARY_TEXT),
                'notes':                Any('TBD', common.PARAGRAPH_TEXT),
                'dirname':              common.LOWERCASE_NAME,
                'policy':               common.LOWERCASE_NAME,
                'api':                  api_config,
                'cli':                  cli_config,
                'gui':                  gui_config,
                'config': {
                    'method':           Any('automatic',
                                            'manual',
                                            'n/a'),
                    'tool':             Any('bzr',
                                            'git',
                                            'hg',
                                            'svn',
                                            'darcs',
                                            'ftp',
                                            'manual',
                                            'n/a',
                                            'TBD'),
                    'url':              common.URL
                },
                'build': {
                    'method':           Any('automatic',
                                            'manual',
                                            'n/a'),
                    'tool':             Any('n/a',
                                            'python_setuptools',
                                            'python_distutils',
                                            'make',
                                            'n/a',
                                            'TBD')
                }
            }

        },
        Extra:                          Reject
    })
