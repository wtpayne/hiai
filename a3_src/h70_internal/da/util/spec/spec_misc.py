# -*- coding: utf-8 -*-
"""
Unit tests for the da.util.misc module.

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
class SpecifyDecomposeMap:
    """
    Specify the decompose_map() function.

    """

    # -------------------------------------------------------------------------
    def it_decomposes_a_single_element_map(self):
        """
        When given a single element map, a single element list is returned.

        """
        import da.util.misc
        single_element_map  = {'a': 1}
        single_element_list = [{'a': 1}]
        assert list(da.util.misc.decompose_map(
                                    single_element_map)) == single_element_list

    # -------------------------------------------------------------------------
    def it_decomposes_a_multi_element_map(self):
        """
        When given a multi element map, a multi element list is returned.

        """
        import da.util.misc
        multi_element_map  = {'a': 1, 'b': 2}
        multi_element_list = [{'a': 1}, {'b': 2}]
        assert list(da.util.misc.decompose_map(
                                    multi_element_map)) == multi_element_list


# =============================================================================
class SpecifyCoroutine:
    """
    Specify the da.util.misc.coroutine() function.

    """

    def it_is_callable(self):
        """
        The coroutine() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.coroutine)


# =============================================================================
class SpecifyStringTypes:
    """
    Specify the da.util.misc.string_types() function.

    """

    def it_is_callable(self):
        """
        The string_types() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.string_types)


# =============================================================================
class SpecifyIsString:
    """
    Specify the da.util.misc.is_string() function.

    """

    def it_is_callable(self):
        """
        The is_string() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.is_string)


# =============================================================================
class SpecifyIndexBuilderCoro:
    """
    Specify the da.util.misc.index_builder_coro() function.

    """

    def it_is_callable(self):
        """
        The index_builder_coro() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.index_builder_coro)


# =============================================================================
class SpecifyBuildIndex:
    """
    Specify the da.util.misc.build_index() function.

    """

    def it_is_callable(self):
        """
        The build_index() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.build_index)


# =============================================================================
class SpecifyWalkobj:
    """
    Specify the da.util.misc.walkobj() function.

    """

    def it_is_callable(self):
        """
        The walkobj() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.walkobj)


# =============================================================================
class SpecifyFlattenRagged:
    """
    Specify the da.util.misc.flatten_ragged() function.

    """

    def it_is_callable(self):
        """
        The flatten_ragged() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.flatten_ragged)


# =============================================================================
class SpecifyWriteJseq:
    """
    Specify the da.util.misc.write_jseq() function.

    """

    def it_is_callable(self):
        """
        The write_jseq() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.write_jseq)


# =============================================================================
class SpecifyLoad:
    """
    Specify the da.util.misc.load() function.

    """

    def it_is_callable(self):
        """
        The load() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.load)


# =============================================================================
class SpecifySave:
    """
    Specify the da.util.misc.save() function.

    """

    def it_is_callable(self):
        """
        The save() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.save)


# =============================================================================
class SpecifyEnsureDirExists:
    """
    Specify the da.util.misc.ensure_dir_exists() function.

    """

    def it_is_callable(self):
        """
        The ensure_dir_exists() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.ensure_dir_exists)


# =============================================================================
class SpecifyEnsureFileExists:
    """
    Specify the da.util.misc.ensure_file_exists() function.

    """

    def it_is_callable(self):
        """
        The ensure_file_exists() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.ensure_file_exists)


# =============================================================================
class SpecifyMergeDicts:
    """
    Specify the da.util.misc.merge_dicts() function.

    """

    def it_is_callable(self):
        """
        The merge_dicts() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.merge_dicts)


# =============================================================================
class SpecifyIterYamlDocs:
    """
    Specify the da.util.misc.iter_yaml_docs() function.

    """

    def it_is_callable(self):
        """
        The iter_yaml_docs() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.iter_yaml_docs)


# =============================================================================
class SpecifyIterDirs:
    """
    Specify the da.util.misc.iter_dirs() function.

    """

    def it_is_callable(self):
        """
        The iter_dirs() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.iter_dirs)


# =============================================================================
class SpecifyIterFiles:
    """
    Specify the da.util.misc.iter_files() function.

    """

    def it_is_callable(self):
        """
        The iter_files() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.iter_files)


# =============================================================================
class SpecifySha256:
    """
    Specify the da.util.misc.sha256() function.

    """

    def it_is_callable(self):
        """
        The sha256() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.sha256)


# =============================================================================
class SpecifySysPathContext:
    """
    Specify the da.util.misc.sys_path_context() function.

    """

    def it_is_callable(self):
        """
        The sys_path_context() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.sys_path_context)


# =============================================================================
class SpecifySysArgvContext:
    """
    Specify the da.util.misc.sys_argv_context() function.

    """

    def it_is_callable(self):
        """
        The sys_argv_context() function is callable

        """
        import da.util.misc
        assert callable(da.util.misc.sys_argv_context)
