# -*- coding: utf-8 -*-
"""
Module containing functions related to files in the LWC.

This includes filename transforms such as design-file to test-file
lookup and vice-versa, as well as any other filename transforms as
might be necessary.

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


SPEC_FILE_PREFIX   = 'spec_'
SPEC_DIR_NAME      = 'spec'
TEST_DATA_DIR_NAME = 'data'


# -----------------------------------------------------------------------------
def is_python_file(filepath):
    """
    Return True if filepath is a document written in the Python language.

    """
    return filepath.endswith('.py')


# -----------------------------------------------------------------------------
def is_cpp_file(filepath):
    """
    Return True if filepath is a document written in the C++ language.

    """
    return filepath.endswith('.cpp') or filepath.endswith('.hpp')


# -----------------------------------------------------------------------------
def is_source_file(filepath):
    """
    Return True if filepath iswritten in a recognised programming language.

    """
    return is_python_file(filepath) or is_cpp_file(filepath)


# -----------------------------------------------------------------------------
def is_specification_file(filepath):
    """
    Return True if filepath is for a specification file.

    Specification files contain the requirements
    specifications and unit tests that together
    document the behaviour of design elements
    contained within a corresponding design
    document.

    """
    (dirpath, filename) = os.path.split(filepath)
    (_, dirname)        = os.path.split(dirpath)
    return (     is_source_file(filepath)
             and (dirname == SPEC_DIR_NAME)
             and filename.startswith(SPEC_FILE_PREFIX))


# -----------------------------------------------------------------------------
def is_design_file(filepath):
    """
    Return True if filepath is a design document.

    Source files are either design documents or
    specification documents.

    """
    return is_source_file(filepath) and not is_specification_file(filepath)


# -----------------------------------------------------------------------------
def is_test_data(filepath):
    """
    Return true if filepath lies within a test data directory.

    """
    testdata_pattern = (   os.sep + SPEC_DIR_NAME
                         + os.sep + TEST_DATA_DIR_NAME
                         + os.sep)
    return testdata_pattern in filepath


# -----------------------------------------------------------------------------
def is_test_config(filepath):
    """
    Return true if filepath is for a test configuration file.

    """
    (dirpath, filename) = os.path.split(filepath)
    (_, dirname)        = os.path.split(dirpath)
    return (     (dirname == SPEC_DIR_NAME)
             and (filename == 'conftest.py'))


# -----------------------------------------------------------------------------
def is_test_related(filepath):
    """
    Return true if filepath is a test or test related file. False otherwise.

    """
    return (    is_specification_file(filepath)
             or is_test_data(filepath)
             or is_test_config(filepath))


# -----------------------------------------------------------------------------
def is_tool_config(filepath):
    """
    Return true if filepath is a tool configuration file.

    """
    (_, filename) = os.path.split(filepath)
    return filename in ('.coveragerc',
                        '.gitignore',
                        'specification.pylintrc',
                        'design.pylintrc')


# -----------------------------------------------------------------------------
def is_experimental(filepath):
    """
    Return true if filepath is an experimental design document.

    """
    return True if 'h50_research' in filepath else False


# -----------------------------------------------------------------------------
def design_filepath_for(filepath_spec):
    """
    Return the design doc filepath corresponding to the specification provided.

    """
    (dirpath_spec,   filename_spec)  = os.path.split(filepath_spec)
    (rootname_spec,  fileext_spec)   = os.path.splitext(filename_spec)
    (dirpath_module, dirname_spec)   = os.path.split(dirpath_spec)
    (_,              dirname_module) = os.path.split(dirpath_module)

    assert dirname_spec == SPEC_DIR_NAME
    assert filename_spec.startswith(SPEC_FILE_PREFIX)

    # Tests for packages are named after the package
    # name, not the module name.
    #
    design_name = rootname_spec.replace(SPEC_FILE_PREFIX, '')
    if design_name == dirname_module:
        filename_module = '__init__.py'
    else:
        filename_module = '{name}{ext}'.format(name = design_name,
                                               ext  = fileext_spec)

    filepath_module = os.path.join(dirpath_module, filename_module)
    return filepath_module


# -----------------------------------------------------------------------------
def specification_filepath_for(filepath_design):
    """
    Return the filepath of the specification for the specified design document.

    """
    (dirpath_design, filename_design) = os.path.split(filepath_design)
    (rootname_design, fileext_design) = os.path.splitext(filename_design)
    dirpath_spec                      = os.path.join(
                                                dirpath_design, SPEC_DIR_NAME)

    # Tests for packages are named after the package
    # name, not the module name.
    #
    if (fileext_design == '.py') and (rootname_design == '__init__'):
        name = os.path.basename(dirpath_design)
    else:
        name = rootname_design

    filename_spec = '{prefix}{name}{ext}'.format(prefix = SPEC_FILE_PREFIX,
                                                 name   = name,
                                                 ext    = fileext_design)
    filepath_spec = os.path.join(dirpath_spec, filename_spec)
    return filepath_spec
