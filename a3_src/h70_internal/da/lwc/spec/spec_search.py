# -*- coding: utf-8 -*-
"""
Unit tests for the da.lwc.search module.

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


import os
import re

import pytest

import da.lwc.search
import da.util


# -----------------------------------------------------------------------------
@pytest.fixture()
def dirpath_testdata():
    """
    Set up the test evironment.

    """
    return os.path.join(os.path.dirname(__file__), 'data')


# =============================================================================
class SpecifyFindAncestorDirContaining:
    """
    Specify the find_ancestor_dir_containing() function.

    """

    # -------------------------------------------------------------------------
    def it_finds_an_ancestor_dir(self,
                                 dirpath_testdata):
        """
        Smoke test for find_ancestor_dir_containing function.

        """

        dirpath_start    = os.path.join(dirpath_testdata,
                                        'simple_directory_tree',
                                        'branch_01',
                                        'leaf_01')
        dirpath_expected = os.path.join(dirpath_testdata,
                                        'simple_directory_tree')
        dirpath_actual   = da.lwc.search.find_ancestor_dir_containing(
                                                                dirpath_start,
                                                                'marker_file')
        assert dirpath_expected == dirpath_actual

    # -------------------------------------------------------------------------
    def it_finds_the_starting_dir(self,
                                  dirpath_testdata):
        """
        Smoke test for find_ancestor_dir_containing function.

        """
        dirpath_start    = os.path.join(dirpath_testdata,
                                        'simple_directory_tree')
        dirpath_expected = dirpath_start
        dirpath_actual   = da.lwc.search.find_ancestor_dir_containing(
                                                                dirpath_start,
                                                                'marker_file')
        assert dirpath_expected == dirpath_actual

    # -------------------------------------------------------------------------
    def it_raises_a_runtime_error_on_failure(self):
        """
        Test find_ancestor_dir_containing raises the right Exceptions.

        """
        dirpath_start = ''
        with pytest.raises(RuntimeError):
            da.lwc.search.find_ancestor_dir_containing(dirpath_start,
                                                       'marker_file')


# =============================================================================
class Specify_WalkTowardsRootGenerator:
    """
    Specify the _walk_towards_root_generator function.

    """

    # -------------------------------------------------------------------------
    def it_generates_reducing_length_strings_with_common_prefixes(
                                                            self,
                                                            dirpath_testdata):
        """
        Test that _walk_towards_root_generator has expected behaviours.

        It should produce a sequence of strings which monotonically reduce
        in length and where each subsequent string is a prefix of the previous
        one.

        """
        walk_generator   = da.lwc.search._walk_towards_root_generator
        dirpath_start    = os.path.join(dirpath_testdata,
                                        'simple_directory_tree',
                                        'branch_01',
                                        'leaf_01')
        walk_list        = [item for item in walk_generator(dirpath_start)]
        is_nonempty_walk = len(walk_list) > 0
        assert is_nonempty_walk
        for (this_item, prev_item) in zip(walk_list[1:], walk_list[:-1]):
            common_prefix = os.path.commonprefix([this_item, prev_item])
            assert len(this_item) < len(prev_item)
            assert this_item == common_prefix


# =============================================================================
class Specify_AdaptOsWalkToDirpath:
    """
    Tet cases for the _adapt_os_walk_to_dirpath function.

    """

    # -------------------------------------------------------------------------
    def it_serialises_a_simple_tree(self):
        """
        Test _adapt_os_walk_to_dirpath handles a simple use case as expected.

        The _adapt_os_walk_to_dirpath should take output in the form
        provided by os.walk and should adapt it to produce a sequence
        of "flat" directory-paths.

        """
        os_walk_input_iter      = (('a1', ['b1', 'b2'], ['c1', 'd1']),
                                   ('a2', ['b3', 'b4'], ['c2', 'd2']),
                                   ('a3', ['b5', 'b6'], ['c3', 'd3']))
        os_walk_expected_output = ('a1/b1', 'a1/b2',
                                   'a2/b3', 'a2/b4',
                                   'a3/b5', 'a3/b6')
        os_walk_actual_output   = tuple(
                    da.lwc.search._adapt_os_walk_to_dirpath(
                                                        os_walk_input_iter))
        assert os_walk_expected_output == os_walk_actual_output

    # -------------------------------------------------------------------------
    def it_serialises_empty_tree(self):
        """
        Test _adapt_os_walk_to_dirpath handles an edge case as expected.

        Empty trees should produce no output.

        """
        os_walk_input_iter      = ()
        os_walk_expected_output = ()
        os_walk_actual_output   = tuple(
                    da.lwc.search._adapt_os_walk_to_dirpath(
                                                        os_walk_input_iter))
        assert os_walk_expected_output == os_walk_actual_output


# =============================================================================
class Specify_AdaptOsWalkToFilepath:
    """
    Tet cases for the _adapt_os_walk_to_filepath function.

    """

    # -------------------------------------------------------------------------
    def it_serialises_simple_tree(self):
        """
        Test _adapt_os_walk_to_filepath handles a simple use case as expected.

        The _adapt_os_walk_to_filepath should take output in the form
        provided by os.walk and should adapt it to produce a sequence
        of "flat" file paths.

        """
        os_walk_input_iter      = (('a1', ['b1'], ['c1', 'd1']),
                                   ('a2', ['b2'], ['c2', 'd2']),
                                   ('a3', ['b3'], ['c3', 'd3']))
        os_walk_expected_output = ('a1/c1', 'a1/d1',
                                   'a2/c2', 'a2/d2',
                                   'a3/c3', 'a3/d3')
        os_walk_actual_output   = tuple(
                    da.lwc.search._adapt_os_walk_to_filepath(
                                                        os_walk_input_iter))
        assert os_walk_expected_output == os_walk_actual_output

    # -------------------------------------------------------------------------
    def it_serialises_empty_tree(self):
        """
        Test _adapt_os_walk_to_filepath handles an edge case as expected.

        Empty trees should produce no output.

        """
        os_walk_input_iter      = ()
        os_walk_expected_output = ()
        os_walk_actual_output   = tuple(
                    da.lwc.search._adapt_os_walk_to_filepath(
                                                        os_walk_input_iter))
        assert os_walk_expected_output == os_walk_actual_output


# =============================================================================
class Specify_CompileRegexList:
    """
    Specify the _compile_regex_list function.

    """

    # -------------------------------------------------------------------------
    def it_compiles_single_character_expressions(self):
        """
        Test that the simplest of expressions are combined as expected.

        """
        regex_list_input           = ['a', 'b']
        regex_list_expected_output = re.compile('(a)|(b)')
        regex_list_actual_output   = da.lwc.search._compile_regex_list(
                                                            regex_list_input)
        assert regex_list_expected_output == regex_list_actual_output


# =============================================================================
class Specify_GetRegexIndicatorFcn:
    """
    Specify the _get_regex_indicator_fcn function.

    """

    # -------------------------------------------------------------------------
    def it_detects_single_chars(self):
        """
        Test that single characters are detected.

        """
        assert da.lwc.search._get_regex_indicator_fcn(['a', 'b'], False)('a')
        assert da.lwc.search._get_regex_indicator_fcn(['a', 'b'], False)('b')
        assert not da.lwc.search._get_regex_indicator_fcn(
                                                    ['a', 'b'], False)('c')


# =============================================================================
class Specify_GetDualRegexIndicatorFcn:
    """
    Specify the _get_dual_regex_indicator_fcn.

    """

    # -------------------------------------------------------------------------
    def it_detects_items_in_include_list_but_not_those_in_exclude_list(self):
        """
        Test that items in include list return true unless in the exclude list.

        """
        incl = ['a', 'b']
        excl = ['b', 'c']
        fcn  = da.lwc.search._get_dual_regex_indicator_fcn(incl,
                                                           excl)
        assert fcn('a')
        assert not fcn('b')
        assert not fcn('c')
        assert not fcn('d')

    # -------------------------------------------------------------------------
    def it_nothing_is_excluded_when_no_explicit_exclude_list_is_given(self):
        """
        Test that no include item is excluded when no exclude list is given.

        """
        incl = ['a', 'b']
        fcn  = da.lwc.search._get_dual_regex_indicator_fcn(incl,
                                                           excl=None)
        assert fcn('a')
        assert fcn('b')
        assert not fcn('c')
        assert not fcn('d')

    # -------------------------------------------------------------------------
    def it_defaults_to_include_all_when_no_explicit_include_list_given(self):
        """
        Test that everything is included when the include list is None.

        """
        excl = ['b', 'c']
        fcn  = da.lwc.search._get_dual_regex_indicator_fcn(incl=None,
                                                           excl=excl)
        assert fcn('a')
        assert not fcn('b')
        assert not fcn('c')
        assert fcn('d')

    # -------------------------------------------------------------------------
    def it_defaults_to_include_all_when_no_conditions_specified(self):
        """
        Test that everything is included when both arguments are None.

        """
        fcn  = da.lwc.search._get_dual_regex_indicator_fcn(incl=None,
                                                           excl=None)
        assert fcn('a')
        assert fcn('b')
        assert fcn('c')
        assert fcn('d')


# =============================================================================
class Specify_DirnameFilter:
    """
    Specify the da.lwc.search._dirname_filter function.

    """

    # -------------------------------------------------------------------------
    def it_all_items_passed_through_filter_that_is_always_true(self):
        """
        Test that an always-true filter function passes all items.

        """
        def always_true_indicator(_):
            return True

        os_walk_input_iter    = (('a1', ['b1'], ['c1', 'd1']),
                                 ('a2', ['b2'], ['c2', 'd2']),
                                 ('a3', ['b3'], ['c3', 'd3']))
        filter_fcn            = da.lwc.search._dirname_filter(
                                                        os_walk_input_iter,
                                                        always_true_indicator)
        assert tuple(filter_fcn) == os_walk_input_iter

    # -------------------------------------------------------------------------
    def it_more_than_one_item_passed_through_when_filter_passes_all(
                                                    self, dirpath_testdata):
        """
        Test that an always-true filter function passes at least one real path.

        """
        def always_true_indicator(_):
            return True

        dirpath_test_tree      = os.path.join(dirpath_testdata,
                                              'simple_directory_tree')
        filter_fcn             = da.lwc.search._dirname_filter(
                                                    os.walk(dirpath_test_tree),
                                                    always_true_indicator)
        assert len(tuple(filter_fcn)) > 1

    # -------------------------------------------------------------------------
    def it_no_subdirs_passed_through_when_filter_passes_none(self,
                                                             dirpath_testdata):
        """
        Test that an always false filter function blocks real paths.

        """
        def always_false_indicator(_):
            return False

        dirpath_test_tree      = os.path.join(dirpath_testdata,
                                              'simple_directory_tree')
        filter_fcn             = da.lwc.search._dirname_filter(
                                                    os.walk(dirpath_test_tree),
                                                    always_false_indicator)
        num_items_pass_filter  = len(tuple(filter_fcn))
        assert num_items_pass_filter == 1


# =============================================================================
class Specify_DirnameRegexFilter:
    """
    Specify the da.lwc.search._dirname_regex_filter function.

    """

    # -------------------------------------------------------------------------
    def it_detect_all_expression(self, dirpath_testdata):
        """
        Test that we get all subdirectories when we do not filter.

        """
        dirpath_test_tree  = os.path.join(dirpath_testdata,
                                          'simple_directory_tree')

        expected_output    = (
                        (os.path.join(dirpath_test_tree),
                            ['branch_02', 'branch_01'],
                            ['marker_file']),
                        (os.path.join(dirpath_test_tree, 'branch_02'),
                            [],
                            ['placeholder_file']),
                        (os.path.join(dirpath_test_tree, 'branch_01'),
                            ['leaf_01', 'leaf_02'],
                            []),
                        (os.path.join(dirpath_test_tree, 'branch_01/leaf_01'),
                            [],
                            ['placeholder_file']),
                        (os.path.join(dirpath_test_tree, 'branch_01/leaf_02'),
                            [],
                            ['placeholder_file']))

        actual_output      = tuple(da.lwc.search._dirname_regex_filter(
                                        os_walk = os.walk(dirpath_test_tree),
                                        excl    = None))

        assert expected_output == actual_output


# =============================================================================
class Specify_FilepathRegexFilter:
    """
    Specify the da.lwc.search._filepath_regex_filter function.

    """

    # -------------------------------------------------------------------------
    def it_detect_all_expression(self):
        """
        Test that all items are matched by a suitable regular expression.

        """
        iter_filepaths    = ('a', 'b', 'c', 'd')
        iter_filtered     = da.lwc.search._filepath_regex_filter(
                                            iter_filepaths = iter_filepaths,
                                            incl           = ['^.*$'],
                                            excl           = None)
        expected_output   = tuple(iter_filepaths)
        assert expected_output == tuple(iter_filtered)

    # -------------------------------------------------------------------------
    def it_detect_suffix_expression(self):
        """
        Test that we can use regular expressions to detect items with suffixes.

        """
        iter_filepaths    = ('a_0', 'b_0', 'c_1', 'd_1')
        iter_filtered     = da.lwc.search._filepath_regex_filter(
                                            iter_filepaths = iter_filepaths,
                                            incl           = ['^.*_0$'],
                                            excl           = None)
        expected_output   = ('a_0', 'b_0')
        assert expected_output == tuple(iter_filtered)


# =============================================================================
class Specify_FilepathFromOsWalkFilter:
    """
    Specify the da.lwc.search._filepath_from_os_walk_filter function.

    """

    # -------------------------------------------------------------------------
    def it_detect_all_expression(self, dirpath_testdata):
        """
        Test the use of an expression to detect everything.

        """
        dirpath_test_tree  = os.path.join(dirpath_testdata,
                                          'dir_with_prefixed_files')

        detect_all_exp     = '^.*$'

        actual_output      = tuple(da.lwc.search._filepath_from_os_walk_filter(
                                        os_walk  = os.walk(dirpath_test_tree),
                                        pathincl = [detect_all_exp],
                                        pathexcl = []))

        expected_output    = (
                            os.path.join(dirpath_test_tree, 'prefix00_file01'),
                            os.path.join(dirpath_test_tree, 'prefix00_file00'),
                            os.path.join(dirpath_test_tree, 'prefix01_file03'),
                            os.path.join(dirpath_test_tree, 'prefix01_file02'))

        assert expected_output == actual_output

    # -------------------------------------------------------------------------
    def it_detect_prefix_expression(self, dirpath_testdata):
        """
        Test the use of an expression to detect prefixes.

        """
        dirpath_test_tree  = os.path.join(dirpath_testdata,
                                          'dir_with_prefixed_files')

        detect_prefix_exp  = '^.*prefix00_.*$'

        actual_output      = tuple(da.lwc.search._filepath_from_os_walk_filter(
                                        os_walk  = os.walk(dirpath_test_tree),
                                        pathincl = [detect_prefix_exp],
                                        pathexcl = []))

        expected_output    = (
                            os.path.join(dirpath_test_tree, 'prefix00_file01'),
                            os.path.join(dirpath_test_tree, 'prefix00_file00'))

        assert expected_output == actual_output

    # -------------------------------------------------------------------------
    def it_detect_nothing_expression(self, dirpath_testdata):
        """
        Test the use of an expression that detects nothing.

        """
        dirpath_test_tree  = os.path.join(dirpath_testdata,
                                          'dir_with_prefixed_files')

        detect_nothing_exp = '^$'

        actual_output      = tuple(
            da.lwc.search._filepath_from_os_walk_filter(
                                        os_walk  = os.walk(dirpath_test_tree),
                                        pathincl = [detect_nothing_exp],
                                        pathexcl = []))

        expected_output    = tuple()

        assert expected_output == actual_output


# =============================================================================
class Specify_DirnameFilteredOsWalkGen:
    """
    Specify the da.lwc.search._dirname_filtered_os_walk_gen() function.

    """

    # -------------------------------------------------------------------------
    def it_filtering_nothing_at_all(self, dirpath_testdata):
        """
        Test the use of an expression that matches nothing to exclude.

        """
        dirpath_test_tree  = os.path.join(
                            dirpath_testdata, 'dir_with_folders_for_filtering')

        detect_nothing_exp = '^$'

        actual_output      = tuple(
            da.lwc.search._dirname_filtered_os_walk_gen(
                                            root    = dirpath_test_tree,
                                            direxcl = [detect_nothing_exp]))

        expected_output    = (
            (   os.path.join(dirpath_test_tree),
                ['dir_to_be_filtered', 'dir_not_to_be_filtered'],
                []),
            (   os.path.join(dirpath_test_tree, 'dir_to_be_filtered'),
                [],
                ['file_in_filtered_folder']),
            (   os.path.join(dirpath_test_tree, 'dir_not_to_be_filtered'),
                [],
                ['file_in_not_filtered_folder']))

        assert expected_output == actual_output

    # -------------------------------------------------------------------------
    def it_filter_something_by_full_name(self, dirpath_testdata):
        """
        Test that we may filter items using its' full name.

        """
        dirpath_test_tree = os.path.join(
                            dirpath_testdata, 'dir_with_folders_for_filtering')

        detect_something   = '^dir_to_be_filtered$'

        actual_output      = tuple(
            da.lwc.search._dirname_filtered_os_walk_gen(
                                                root    = dirpath_test_tree,
                                                direxcl = [detect_something]))

        expected_output    = (
            (   os.path.join(dirpath_test_tree),
                ['dir_not_to_be_filtered'],
                []),
            (   os.path.join(dirpath_test_tree, 'dir_not_to_be_filtered'),
                [],
                ['file_in_not_filtered_folder']))

        assert expected_output == actual_output


# =============================================================================
class SpecifyFilteredFilepathGenerator:
    """
    Specify the da.lwc.search.filtered_filepath_generator function.

    """

    # -------------------------------------------------------------------------
    def it_undefined_filters_shall_cause_all_filepaths_to_be_returned(
                                                    self, dirpath_testdata):
        """
        Test that undefined filters cause all filepaths to be returned.

        """
        dirpath_test_tree  = os.path.join(
                dirpath_testdata, 'dir_with_files_and_folders_for_filtering')

        actual_output      = tuple(
            da.lwc.search.filtered_filepath_generator(
                                        root     = dirpath_test_tree,
                                        direxcl  = None,
                                        pathincl = None,
                                        pathexcl = None))

        expected_output = (
                    os.path.join(dirpath_test_tree,
                                 'dir_to_be_filtered',
                                 'file_in_filtered_folder'),
                    os.path.join(dirpath_test_tree,
                                 'dir_not_to_be_filtered',
                                 'file_in_not_filtered_folder_with_suffix01'),
                    os.path.join(dirpath_test_tree,
                                 'dir_not_to_be_filtered',
                                 'file_in_not_filtered_folder_with_suffix02'))

        assert expected_output == actual_output

    # -------------------------------------------------------------------------
    def it_direxcl_shall_exclude_all_files_in_specified_dirs(
                                                    self, dirpath_testdata):
        """
        Test we exclude whole directories with _filtered_filepath_generator.

        """
        dirpath_test_tree  = os.path.join(
                dirpath_testdata, 'dir_with_files_and_folders_for_filtering')

        actual_output      = tuple(
            da.lwc.search.filtered_filepath_generator(
                                        root     = dirpath_test_tree,
                                        direxcl  = ['^dir_to_be_filtered$'],
                                        pathincl = None,
                                        pathexcl = None))

        expected_output = (
                    os.path.join(dirpath_test_tree,
                                 'dir_not_to_be_filtered',
                                 'file_in_not_filtered_folder_with_suffix01'),
                    os.path.join(dirpath_test_tree,
                                 'dir_not_to_be_filtered',
                                 'file_in_not_filtered_folder_with_suffix02'))

        assert expected_output == actual_output

    # -------------------------------------------------------------------------
    def it_pathexcl_shall_exclude_files_as_specified(self, dirpath_testdata):
        """
        Test we can exclude files by suffix with _filtered_filepath_generator.

        """
        dirpath_test_tree  = os.path.join(
                dirpath_testdata, 'dir_with_files_and_folders_for_filtering')

        actual_output      = tuple(
            da.lwc.search.filtered_filepath_generator(
                                        root     = dirpath_test_tree,
                                        direxcl  = ['^dir_to_be_filtered$'],
                                        pathincl = None,
                                        pathexcl = ['^.*_suffix01$']))

        expected_output = (
                    os.path.join(dirpath_test_tree,
                                 'dir_not_to_be_filtered',
                                 'file_in_not_filtered_folder_with_suffix02'),)

        assert expected_output == actual_output

    # -------------------------------------------------------------------------
    def it_pathexcl_shall_include_files_as_specified(self, dirpath_testdata):
        """
        Test we can detect suffixed files with _filtered_filepath_generator.

        """
        dirpath_test_tree  = os.path.join(
                dirpath_testdata, 'dir_with_files_and_folders_for_filtering')

        actual_output      = tuple(
            da.lwc.search.filtered_filepath_generator(
                                        root     = dirpath_test_tree,
                                        direxcl  = ['^dir_to_be_filtered$'],
                                        pathincl = ['^.*_suffix02$'],
                                        pathexcl = None))

        expected_output = (
                    os.path.join(dirpath_test_tree,
                                 'dir_not_to_be_filtered',
                                 'file_in_not_filtered_folder_with_suffix02'),)

        assert expected_output == actual_output


# =============================================================================
class SpecifyFindFiles:
    """
    Specify the da.lwc.search.find_files function.

    """

    # -------------------------------------------------------------------------
    def it_can_filter_files_based_on_their_suffix(self, dirpath_testdata):
        """
        Test that we can detect files with suffixes using find_files.

        """
        dirpath_test_tree  = os.path.join(
                dirpath_testdata, 'dir_with_files_and_folders_for_filtering')

        actual_output      = tuple(
            da.lwc.search.find_files(
                                root    = dirpath_test_tree,
                                suffix  = '_suffix02'))

        expected_output = (
                    os.path.join(dirpath_test_tree,
                                 'dir_not_to_be_filtered',
                                 'file_in_not_filtered_folder_with_suffix02'),)

        assert expected_output == actual_output


# =============================================================================
class SpecifyFilteredDirpathGenerator:
    """
    Specify the da.lwc.search.filtered_dirpath_generator() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The filtered_dirpath_generator() function is callable.

        """
        assert callable(da.lwc.search.filtered_dirpath_generator)
