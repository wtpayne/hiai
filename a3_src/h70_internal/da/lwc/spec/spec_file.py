# -*- coding: utf-8 -*-
"""
Unit tests for the da.lwc package.

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


# =============================================================================
class SpecifyIsPythonFile:
    """
    Specify the is_python_file() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_filename_ending_py(self):
        """
        It returns True when given a filename ending with .py.

        """
        import da.lwc.file
        assert da.lwc.file.is_python_file('anything.py') is True

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_filename_not_ending_py(self):
        """
        It returns False when given a filename not ending with .py.

        """
        import da.lwc.file
        assert da.lwc.file.is_python_file('anything.notpy') is False


# =============================================================================
class SpecifyIsCppFile:
    """
    Specify the is_cpp_file() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_filename_ending_cpp(self):
        """
        It returns True when given a filename ending with .cpp.

        """
        import da.lwc.file
        assert da.lwc.file.is_cpp_file('anything.cpp') is True

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_filename_ending_hpp(self):
        """
        It returns True when given a filename ending with .cpp.

        """
        import da.lwc.file
        assert da.lwc.file.is_cpp_file('anything.hpp') is True

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_filename_not_ending_cpp_or_hpp(self):
        """
        It returns False when given a filename not ending with .py.

        """
        import da.lwc.file
        assert da.lwc.file.is_cpp_file('anything.not_cpp_or_hpp') is False


# =============================================================================
class SpecifyIsSourceFile:
    """
    Specify the is_source_file() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_filename_ending_py(self):
        """
        It returns True when given a filename ending with .py.

        """
        import da.lwc.file
        assert da.lwc.file.is_source_file('anything.py') is True

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_filename_ending_cpp(self):
        """
        It returns True when given a filename ending with .cpp.

        """
        import da.lwc.file
        assert da.lwc.file.is_source_file('anything.cpp') is True

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_filename_ending_hpp(self):
        """
        It returns True when given a filename ending with .cpp.

        """
        import da.lwc.file
        assert da.lwc.file.is_source_file('anything.hpp') is True

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_filename_not_ending_cpp_or_hpp(self):
        """
        It returns False when given a filename not ending with .cpp or .hpp.

        """
        import da.lwc.file
        assert da.lwc.file.is_source_file(
                                    'anything.not_py_or_cpp_or_hpp') is False


# =============================================================================
class SpecifyIsSpecificationFile:
    """
    Specify the is_specification_file() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_python_specification_filepath(self):
        """
        It returns True when given a filepath conforming to the convention
        for Python specification documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_specification_file(
                                    'anything/spec/spec_anything.py') is True

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_cpp_specification_filepath(self):
        """
        It returns True when given a filepath conforming to the convention
        for C++ specification documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_specification_file(
                                    'anything/spec/spec_anything.cpp') is True

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_python_design_filepath(self):
        """
        It returns False when given a filepath conforming to the convention
        for python design documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_specification_file(
                                            'anything/anything.py') is False

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_cpp_design_filepath(self):
        """
        It returns False when given a filepath conforming to the convention
        for C++ design documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_specification_file(
                                            'anything/anything.cpp') is False

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_configuration_filepath(self):
        """
        It returns False when given a filepath conforming to the convention
        for configuration documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_specification_file('.gitignore') is False


# =============================================================================
class SpecifyIsDesignFile:
    """
    Specify the is_specification_file() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_python_design_filepath(self):
        """
        It returns True when given a filepath conforming to the convention
        for Python design documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_design_file('anything/anything.py') is True

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_cpp_design_filepath(self):
        """
        It returns True when given a filepath conforming to the convention
        for C++ design documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_design_file('anything/anything.cpp') is True

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_python_specification_filepath(self):
        """
        It returns False when given a filepath conforming to the convention
        for Python specification documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_design_file(
                                    'anything/spec/spec_anything.py') is False

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_cpp_specification_filepath(self):
        """
        It returns False when given a filepath conforming to the convention
        for C++ specification documents.

        """
        import da.lwc.file
        assert da.lwc.file.is_design_file(
                                    'anything/spec/spec_anything.cpp') is False


# =============================================================================
class SpecifyIsTestData:
    """
    Specify the is_test_data() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The is_test_data() function is callable.

        """
        import da.lwc.file
        assert callable(da.lwc.file.is_test_data)


# =============================================================================
class SpecifyIsTestConfig:
    """
    Specify the is_test_config() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The is_test_config() function is callable.

        """
        import da.lwc.file
        assert callable(da.lwc.file.is_test_config)


# =============================================================================
class SpecifyIsTestRelated:
    """
    Specify the is_test_related() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_true_when_given_a_valid_unit_test_path(self):
        """
        When given a valid test path, is_test_related() shall return True.

        """
        import da.lwc.file
        a_valid_unit_test = '/module/spec/spec_name.py'
        assert da.lwc.file.is_test_related(a_valid_unit_test) == True

    # -------------------------------------------------------------------------
    def it_returns_false_when_given_a_valid_module_path(self):
        """
        When given a valid module path, is_test_related() shall return False.

        """
        import da.lwc.file
        a_valid_module = '/module/name.py'
        assert da.lwc.file.is_test_related(a_valid_module) == False


# =============================================================================
class SpecifyIsToolConfig:
    """
    Specify the is_tool_config() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The is_tool_config() function is callable.

        """
        import da.lwc.file
        assert callable(da.lwc.file.is_tool_config)


# =============================================================================
class SpecifyDesignFilepathFor:
    """
    Specify the design_filepath_for() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_python_module_path_when_given_module_test_path(self):
        """
        When given the test path for a module, the module path is returned.

        When given a valid module test path, the corresponding module path
        shall be returned.

        """
        import da.lwc.file
        filepath_design_document = '/package/module.py'
        filepath_test            = '/package/spec/spec_module.py'
        assert da.lwc.file.design_filepath_for(
                                    filepath_test) == filepath_design_document

    # -------------------------------------------------------------------------
    def it_returns_python_package_path_when_given_package_test_path(self):
        """
        When given the test path for a module, the module path is returned.

        When given a valid module test path, the corresponding module path
        shall be returned.

        """
        import da.lwc.file
        filepath_design_document = '/package/__init__.py'
        filepath_test            = '/package/spec/spec_package.py'
        assert da.lwc.file.design_filepath_for(
                                    filepath_test) == filepath_design_document

    # -------------------------------------------------------------------------
    def it_returns_c_source_file_path_when_given_c_test_path(self):
        """
        When given the test path for a module, the module path is returned.

        When given a valid module test path, the corresponding module path
        shall be returned.

        """
        import da.lwc.file
        filepath_design_document = '/component/srcfile.c'
        filepath_test            = '/component/spec/spec_srcfile.c'
        assert da.lwc.file.design_filepath_for(
                                    filepath_test) == filepath_design_document


# =============================================================================
class SpecifySpecificationFilepathFor:
    """
    Specify the specification_filepath_for() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_test_path_when_given_python_module_path(self):
        """
        When given a module path, the corresponding spec path is returned.

        When given a valid module path, the get_specification_filepath_for()
        function shall return the specification path that corresponds to the
        path provided.

        """
        import da.lwc.file
        filepath_design_document = '/package/module.py'
        filepath_test            = '/package/spec/spec_module.py'
        assert da.lwc.file.specification_filepath_for(
                                    filepath_design_document) == filepath_test

    # -------------------------------------------------------------------------
    def it_returns_a_test_path_when_given_python_package_path(self):
        """
        When given a package path, the corresponding test path is returned.

        When given a valid module path, the specification_filepath_for()
        function shall return the test path that corresponds to the path
        provided.

        """
        import da.lwc.file
        filepath_design_document = '/package/__init__.py'
        filepath_test            = '/package/spec/spec_package.py'
        assert da.lwc.file.specification_filepath_for(
                                    filepath_design_document) == filepath_test

    # -------------------------------------------------------------------------
    def it_returns_a_test_path_when_given_c_source_file_path(self):
        """
        When given a C src file path, the corresponding test path is returned.

        """
        import da.lwc.file
        filepath_design_document = '/component/srcfile.c'
        filepath_test            = '/component/spec/spec_srcfile.c'
        assert da.lwc.file.specification_filepath_for(
                                    filepath_design_document) == filepath_test
