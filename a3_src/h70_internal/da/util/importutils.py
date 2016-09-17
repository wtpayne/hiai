# -*- coding: utf-8 -*-
"""
Module import utility functions.

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


import importlib
import os
import sys


# -----------------------------------------------------------------------------
def import_fcn(module_dot_fcn):
    """
    Import the specified function.

    """
    (module_name, function_name) = module_dot_fcn.rsplit(".", 1)
    module   = importlib.import_module(module_name)
    function = getattr(module, function_name)
    return function


# -----------------------------------------------------------------------------
def import_module_file(filepath):
    """
    Import the specified module.

    """
    # The first implementation of this function
    # used the importlib.machinery.SourceFileLoader
    # function, but this approach unfortunately
    # caused issues for us once we started to use
    # sys.modules to unload and reload modules to
    # dynamically shift the LWC to the controlled
    # area for build operations.
    #
    # Modules loaded with this function didn't
    # appear to be represented with the right type
    # in sys.modules - or at least couldn't be
    # reloaded without throwing an exception.
    #
    # To work around this issue, we have had to
    # replace the call to importlib.import_module
    # with the higher level __import__ function.
    # This appears to do all the book-keeping that
    # we require.
    #
    (dirpath, filename) = os.path.split(filepath)
    (module_name, _)    = os.path.splitext(filename)
    return import_from_dir(dirpath, module_name)


# -----------------------------------------------------------------------------
def import_from_dir(dirpath, module_name):
    """
    Import a module from a specified_directory.

    """
    if dirpath in sys.path:
        module = importlib.__import__(module_name)
    else:
        sys.path.insert(0, dirpath)
        try:
            module = importlib.__import__(module_name)
        finally:
            del sys.path[0]
    return module
