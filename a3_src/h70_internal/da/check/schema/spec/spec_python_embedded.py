# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.schema.python_embedded module.

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


import pytest


# -----------------------------------------------------------------------------
@pytest.fixture()
def valid_file_metadata():
    """
    Return valid python file metadata.

    """
    return {
        'type':                 'python_module',
        'validation_level':     'v00_minimum',
        'protection':           'k00_public',
        'copyright':
            "Copyright 2016 High Integrity Artificial Intelligence Systems",
        'license': (
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
    }


# -----------------------------------------------------------------------------
@pytest.fixture()
def valid_class_metadata():
    """
    Return valid python class metadata.

    """
    return {
        'type':                 'class',
        'attributes': {
            'attribute_a':      'A comment about attribute_a',
            'attribute_b':      'A comment about attribute_b'
        }
    }


# -----------------------------------------------------------------------------
@pytest.fixture()
def valid_function_metadata():
    """
    Return valid python function metadata.

    """
    return {
        'type':                 'function',
        'args': {
            'argument_a':       'A comment about argument_a',
            'argument_b':       'A comment about argument_b'
        }
    }


# -----------------------------------------------------------------------------
@pytest.fixture()
def valid_requirement_set(load):
    """
    Return valid requirement set data.

    """
    return load("""
    ---
    i00041_control_access_to_counterparty_specific_confidential_documents:
      - "Access to counterparty specific confidential documents SHALL be
         controlled."
      - notes: "We want to provide assurance to our counterparties that access
               controls will be instituted and enforced to protect their
               confidential information and intellectual property."
      - type: mandate
      - state: draft

    i00042_organise_documents_for_reuse:
      - "Documents SHALL be organised to facilitate reuse across projects."
      - notes: "We want to promote reuse of design documents by adopting a
               product line engineering approach. This means that many
               products and projects are aggregated together into a single
               monolithic configuration."
      - type: mandate
      - state: draft
    ...""")


# =============================================================================
class SpecifyFileMetadataSchema:
    """
    Specify da.check.schema.python_embedded.file_metadata_schema() function.

    """

    # -------------------------------------------------------------------------
    def it_accepts_valid_file_metadata(self,
                                       idclass_tab,
                                       valid_file_metadata):
        """
        When given valid Python file metadata it validates without throwing.

        """
        import da.check.schema.python_embedded
        schema = da.check.schema.python_embedded.file_metadata_schema(
                                                                idclass_tab)
        assert schema(valid_file_metadata) == valid_file_metadata


# =============================================================================
class SpecifyFileScopeSchema:
    """
    Specify the da.check.schema.python_embedded.file_scope_schema() function.

    """

    # -------------------------------------------------------------------------
    def it_accepts_valid_file_metadata(self,
                                       idclass_tab,
                                       valid_file_metadata):
        """
        When given valid Python file metadata it validates without throwing.

        """
        import da.check.schema.python_embedded
        schema = da.check.schema.python_embedded.file_scope_schema(idclass_tab)
        assert schema(valid_file_metadata) == valid_file_metadata

    # -------------------------------------------------------------------------
    def it_accepts_a_valid_requirement_set(self,
                                           idclass_tab,
                                           valid_requirement_set):
        """
        The python_embedded.file_scope_schema validates a requirement set.

        """
        import da.check.schema.python_embedded
        schema = da.check.schema.python_embedded.file_scope_schema(idclass_tab)
        assert schema(valid_requirement_set) == valid_requirement_set


# =============================================================================
class SpecifyClassScopeSchema:
    """
    Specify the da.check.schema.python_embedded.class_scope_schema() function.

    """

    # -------------------------------------------------------------------------
    def it_accepts_valid_class_metadata(self,
                                        idclass_tab,
                                        valid_class_metadata):
        """
        The python_embedded.class_scope_schema validates class metadata.

        """
        import da.check.schema.python_embedded
        schema = da.check.schema.python_embedded.class_scope_schema(
                                                                idclass_tab)
        assert schema(valid_class_metadata) == valid_class_metadata


    # -------------------------------------------------------------------------
    def it_accepts_a_valid_requirement_set(self,
                                           idclass_tab,
                                           valid_requirement_set):
        """
        The python_embedded.class_scope_schema validates a requirement set.

        """
        import da.check.schema.python_embedded
        schema = da.check.schema.python_embedded.class_scope_schema(
                                                                idclass_tab)
        assert schema(valid_requirement_set) == valid_requirement_set


# =============================================================================
class SpecifyFunctionScopeSchema:
    """
    Specify da.check.schema.python_embedded.function_scope_schema() function.

    """

    # -------------------------------------------------------------------------
    def it_accepts_valid_function_metadata(self,
                                           idclass_tab,
                                           valid_function_metadata):
        """
        The python_embedded.function_scope_schema validates a requirement set.

        """
        import da.check.schema.python_embedded
        schema = da.check.schema.python_embedded.function_scope_schema(
                                                                idclass_tab)
        assert schema(valid_function_metadata) == valid_function_metadata


    # -------------------------------------------------------------------------
    def it_accepts_a_valid_requirement_set(self,
                                           idclass_tab,
                                           valid_requirement_set):
        """
        The python_embedded.function_scope_schema validates a requirement set.

        """
        import da.check.schema.python_embedded
        schema = da.check.schema.python_embedded.function_scope_schema(
                                                                idclass_tab)
        assert schema(valid_requirement_set) == valid_requirement_set


# =============================================================================
class SpecifyFunctionMetadataSchema:
    """
    Specify da.check.schema.python_embedded.function_metadata_schema().

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The function_metadata_schema() function is callable.

        """
        import da.daybook
        assert callable(
                    da.check.schema.python_embedded.function_metadata_schema)


# =============================================================================
class SpecifyClassMetadataSchema:
    """
    Specify da.check.schema.python_embedded.class_metadata_schema().

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The class_metadata_schema() function is callable.

        """
        import da.daybook
        assert callable(da.check.schema.python_embedded.class_metadata_schema)
