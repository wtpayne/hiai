# -*- coding: utf-8 -*-
"""
Unit tests for the python_source module.

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


import ast
import io
import textwrap


# -----------------------------------------------------------------------------
def get_list_of_tokens_from_text(text_content):
    """
    Return a list of tokens parsed from the provided text.

    """
    import da.python_source
    bytes_content = io.BytesIO(textwrap.dedent(text_content).encode())
    token_list    = list()
    for token in da.python_source._gen_comment_and_docstr_toks(bytes_content):
        token_list.append(token.txt)
    return token_list


# =============================================================================
class SpecifyGenTopLevelClassNames:
    """
    Specify the da.python_source.gen_top_level_class_names() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The gen_top_level_class_names() function is callable.

        """
        import da.python_source
        assert callable(da.python_source.gen_top_level_class_names)


# =============================================================================
class SpecifyGenTopLevelFunctionNames:
    """
    Specify the da.python_source.gen_top_level_function_names() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The gen_top_level_function_names() function is callable.

        """
        import da.python_source
        assert callable(da.python_source.gen_top_level_function_names)


# =============================================================================
class SpecifyGenTopLevelMethodNames:
    """
    Specify the da.python_source.gen_top_level_method_names() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The gen_top_level_method_names() function is callable.

        """
        import da.python_source
        assert callable(da.python_source.gen_top_level_method_names)


# =============================================================================
class Specify_GenCommentAndDocstrToks:
    """
    Specify the _gen_comment_and_docstr_toks() function.

    """

    # -------------------------------------------------------------------------
    def it_can_extract_a_single_line_comment(self):
        """
        A single line comment is extracted from the input stream.

        ---
        i00047_extract_comments_from_python_files:
          - "The system SHALL extract comment text from files conforming to
            the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      # One comment
                      def a_function:
                          pass
                      '''
        assert get_list_of_tokens_from_text(test_vector) == [' One comment']

    # -------------------------------------------------------------------------
    def it_can_extract_a_function_docstring(self):
        """
        A function docstring is extracted from the input stream.

        ---
        i00048_extract_function_docstrings_from_python_files:
          - "The system SHALL extract function level docstring text from
            files conforming to the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      def a_function:
                          """
                          One function level docstring
                          """
                          pass
                      '''
        assert get_list_of_tokens_from_text(
                            test_vector) == ['One function level docstring']

    # -------------------------------------------------------------------------
    def it_can_extract_a_class_docstrings(self):
        """
        A class docstring is extracted from the input stream.

        ---
        i00049_extract_class_docstrings_from_python_files:
          - "The system SHALL extract class level docstring text from
            files conforming to the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      class a_class:
                          """
                          One class level docstring
                          """
                          pass
                      '''
        assert get_list_of_tokens_from_text(
                                test_vector) == ['One class level docstring']

    # -------------------------------------------------------------------------
    def it_can_extract_a_module_docstring(self):
        """
        A module docstring is extracted from the input stream.

        ---
        i00050_extract_module_docstrings_from_python_files:
          - "The system SHALL extract module level docstring text from
            files conforming to the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      """
                      One module level docstring
                      """
                      def a_function:
                          pass
                      '''
        assert get_list_of_tokens_from_text(
                                test_vector) == ['One module level docstring']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_followed_by_a_single_line_comment(self):
        """
        A function docstring followed by a single line comment is extracted.

        """
        test_vector = '''
                      def a_function:
                          """
                          One function level docstring
                          """
                          # And one comment
                          pass
                      '''
        assert get_list_of_tokens_from_text(
                            test_vector) == ['One function level docstring',
                                             ' And one comment']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_followed_by_a_multiline_comment(self):
        """
        A function docstring followed by a multi line comment is extracted.

        """
        test_vector = '''
                      def a_function:
                          """
                          One function level docstring
                          """
                          # And one comment
                          # Over multiple lines
                          pass
                      '''
        assert get_list_of_tokens_from_text(
                            test_vector) == ['One function level docstring',
                                             ' And one comment',
                                             ' Over multiple lines']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_between_comments(self):
        """
        A function docstring between two single line comments is extracted.

        """
        test_vector = '''
                      # A Comment
                      def a_function:
                          """
                          A Docstring
                          on multiple lines
                          """
                          # And another comment after.
                          pass
                      '''
        assert get_list_of_tokens_from_text(
                            test_vector) == [' A Comment',
                                             'A Docstring\non multiple lines',
                                             ' And another comment after.']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_but_ignore_a_string_literal(self):
        """
        A function docstring is extracted but a string literal is ignored.

        """
        test_vector = '''
                      def a_function:
                          """
                          One docstring
                          """
                          x = """And one string literal"""
                          pass
                      '''
        assert get_list_of_tokens_from_text(test_vector) == ['One docstring']


    # -------------------------------------------------------------------------
    def it_can_extract_a_multiline_comment_containing_yaml(self):
        """
        A multiline comment containing some yaml is extracted.

        """
        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      '''
        assert get_list_of_tokens_from_text(test_vector) == [' ---',
                                                             ' key: value',
                                                             ' ...']


# =============================================================================
class Specify_MergeCommentBlocks:
    """
    Specify the _merge_comment_blocks() function.

    """

    # -------------------------------------------------------------------------
    def it_does_marvellous_things(self):
        """
        Test basic use cases for the _merge_comment_blocks function.

        """
        import da.python_source
        _gen_tok = da.python_source._gen_comment_and_docstr_toks
        _merge   = da.python_source._merge_comment_blocks

        def _testitem(raw):
            return _merge(_gen_tok(_to_file(raw)))

        def _to_file(raw):
            return io.BytesIO(textwrap.dedent(raw).encode())

        def _fixture(raw):
            return [blk.txt for blk in _testitem(raw)]

        test_vector = '''
                      # Comment 1.
                      # Comment 2.
                      '''
        assert _fixture(test_vector) == [' Comment 1.\n Comment 2.']

        test_vector = '''
                      # Comment 1.
                      this_is_a_gap = 1
                      # Comment 2.
                      '''
        assert _fixture(test_vector) == [' Comment 1.',
                                         ' Comment 2.']

        test_vector = '''
                      # Comment 1.
                      # Comment 2.
                      this_is_a_gap = 1
                      # Comment 3.
                      '''
        assert _fixture(test_vector) == [' Comment 1.\n Comment 2.',
                                         ' Comment 3.']

        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      '''
        assert _fixture(test_vector) == [' ---\n key: value\n ...']


# =============================================================================
class Specify_GenEmbeddedData:
    """
    Specify the _gen_embedded_data() function.

    """

    # -------------------------------------------------------------------------
    def it_does_marvellous_things(self):
        """
        Test basic use cases for the _gen_embedded_data_in_file function.

        """
        import da.python_source
        _gen_data   = da.python_source._gen_embedded_data_in_file

        def _testitem(raw):
            return _gen_data(_to_file(raw))

        def _to_file(raw):
            return io.BytesIO(textwrap.dedent(raw).encode())

        def _fixture(raw):
            return [yaml.dat for yaml in _testitem(raw)]

        test_vector = '''
                      # ---
                      # a_key: "A Value"
                      # ...
                      '''
        assert _fixture(test_vector) == [{'a_key': 'A Value'}]


# =============================================================================
class Specify_IterWindowedPairs:
    """
    Specify the _iter_windowed_pairs() function.

    """

    # -------------------------------------------------------------------------
    def it_does_marvellous_things(self):
        """
        Test basic use cases for the _iter_windowed_pairs function.

        """
        import da.python_source

        def _fixture(test_vector):
            return list(da.python_source._iter_windowed_pairs(test_vector))

        test_vector = []
        assert _fixture(test_vector) == [(None, None)]

        test_vector = ['A']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', None)]

        test_vector = ['A', 'B']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', 'B'),
                                         ('B', None)]

        test_vector = ['A', 'B', 'C']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', 'B'),
                                         ('B', 'C'),
                                         ('C', None)]

        test_vector = ['A', 'B', 'C', 'D']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', 'B'),
                                         ('B', 'C'),
                                         ('C', 'D'),
                                         ('D', None)]


# =============================================================================
class SpecifyIterEmbeddedData:
    """
    Specify the iter_embedded_data() function.

    """

    # -------------------------------------------------------------------------
    def it_does_marvellous_things(self):
        """
        Test basic use cases for the iter_embedded_data function.

        """
        import da.python_source

        def _fixture(test_vector):
            encoded_input = io.BytesIO(textwrap.dedent(test_vector).encode())
            root          = ast.parse(encoded_input.read())
            iter_out      = da.python_source.iter_embedded_data(
                                                    'mod', root, encoded_input)
            return [(embed.dat, embed.meta.path) for embed in iter_out]

        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      '''
        assert _fixture(test_vector) == [
                        ({'key':  'value'},  'mod')]

        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      def test_func():
                          pass
                      '''
        assert _fixture(test_vector) == [
                        ({'key': 'value'}, 'mod.test_func')]

        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      def test_func():
                          """
                          ---
                          key2: value2
                          ...
                          """
                          pass
                      '''
        assert _fixture(test_vector) == [
                        ({'key':  'value'},  'mod.test_func'),
                        ({'key2': 'value2'}, 'mod.test_func')]

        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      def test_func():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          pass
                      '''
        assert _fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_func'),
                        ({'key3': 'value3'}, 'mod.test_func')]

        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      def test_func():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          def inner_func():
                              """
                              ---
                              key4: value4
                              ...
                              """
                              pass
                      '''
        assert _fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_func'),
                        ({'key3': 'value3'}, 'mod.test_func'),
                        ({'key4': 'value4'}, 'mod.test_func.inner_func')]

        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      def test_func():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          # ---
                          # key4: value4
                          # ...
                          def inner_func():
                              """
                              ---
                              key5: value5
                              ...
                              """
                              pass
                      '''
        assert _fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_func'),
                        ({'key3': 'value3'}, 'mod.test_func'),
                        ({'key4': 'value4'}, 'mod.test_func.inner_func'),
                        ({'key5': 'value5'}, 'mod.test_func.inner_func')]

        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      class test_class():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          # ---
                          # key4: value4
                          # ...
                          def test_method():
                              """
                              ---
                              key5: value5
                              ...
                              """
                          pass
                      '''
        assert _fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_class'),
                        ({'key3': 'value3'}, 'mod.test_class'),
                        ({'key4': 'value4'}, 'mod.test_class.test_method'),
                        ({'key5': 'value5'}, 'mod.test_class.test_method')]

        test_vector = '''
                      def test_func():
                          # ---
                          # key1:
                          #     key2:
                          #         key3: value
                          # ...
                          pass
                      '''
        assert _fixture(test_vector) == [
                    ({'key1': {'key2': {'key3': 'value'}}}, 'mod.test_func')]

        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      '''
        assert _fixture(test_vector) == [
                        ({'key': 'value'}, 'mod')]


# =============================================================================
class SpecifyGenFunctions:
    """
    Specify the da.python_source.gen_functions() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The gen_functions() function is callable.

        """
        import da.python_source
        assert callable(da.python_source.gen_functions)


# =============================================================================
class Specify_IndentLevel:
    """
    Specify the da.python_source._indent_level() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _indent_level() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._indent_level)


# =============================================================================
class SpecifyGenAstPathsDepthFirst:
    """
    Specify the da.python_source.gen_ast_paths_depth_first() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The gen_ast_paths_depth_first() function is callable.

        """
        import da.python_source
        assert callable(da.python_source.gen_ast_paths_depth_first)


# =============================================================================
class SpecifyGetModuleName:
    """
    Specify the da.python_source.get_module_name() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The get_module_name() function is callable.

        """
        import da.python_source
        assert callable(da.python_source.get_module_name)


# =============================================================================
class Specify_HasName:
    """
    Specify the da.python_source._has_name() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _has_name() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._has_name)


# =============================================================================
class Specify_HasBody:
    """
    Specify the da.python_source._has_body() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _has_body() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._has_body)


# =============================================================================
class Specify_IterChildrenWithBodies:
    """
    Specify the da.python_source._iter_children_with_bodies() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _iter_children_with_bodies() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._iter_children_with_bodies)


# =============================================================================
class Specify_LastLineIn:
    """
    Specify the da.python_source._last_line_in() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _last_line_in() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._last_line_in)


# =============================================================================
class Specify_GenEmbeddedDataInFile:
    """
    Specify the da.python_source._gen_embedded_data_in_file() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _gen_embedded_data_in_file() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._gen_embedded_data_in_file)
