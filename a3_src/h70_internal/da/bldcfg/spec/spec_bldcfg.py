# -*- coding: utf-8 -*-
"""
Unit tests for the da.bldcfg package.

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

import da.lwc.discover


# -----------------------------------------------------------------------------
@pytest.fixture()
def dirpath_lwc_root():
    """
    Test fixture with the path to the root of the local working copy.

    """
    return da.lwc.discover.path(key = 'root')


# =============================================================================
class SpecifyLoadCfg:
    """
    Specify the da.bldcfg.load_cfg() function.

    """

    # -------------------------------------------------------------------------
    def it_finds_configuration_when_cfg_key_matches_exactly(
                                                    self, dirpath_lwc_root):
        """
        ---
        i00000_load_configuration_based_on_an_exact_match:
          - "When provided with a cfg_key that is equal to the root of the
            filename of a build configuration file that exists in the local
            working copy, then the load_cfg function SHALL return a valid
            configuration derived from the content of that file."
          - notes: "The root of the filename is the filename without extension
                   or delimiter. For a file named foo.txt, foo is the root and
                   .txt is the extension."
          - type: mandate
          - state: draft
        ...
        """
        import da.bldcfg
        default_config = da.bldcfg.load_cfg(
                                        cfg_key          = 'default',
                                        cfg_extras       = {},
                                        dirpath_lwc_root = dirpath_lwc_root)
        assert isinstance(default_config, dict)
        assert 'cfg_name' in default_config
        assert default_config['cfg_name'] == 'default'
        assert len(default_config) == 8  # At least some data returned.

    # -------------------------------------------------------------------------
    def it_finds_configuration_when_cfg_key_matches_approximately(
                                                    self, dirpath_lwc_root):
        """
        ---
        i00000_load_configuration_based_on_an_approximate_match:
          - "When provided with a cfg_key that is approximately equal to the
            root of the filename of a build configuration file that exists in
            the local working copy, then the load_cfg function SHALL return a
            valid configuration derived from the content of that file."
          - notes: "Approximately matching can be implementation defined. It is
                   assumed that the python fuzzywuzzy string matching library
                   or a near equivalent will be used."
          - type:  mandate
          - state: draft
        ...
        """
        import da.bldcfg
        default_config = da.bldcfg.load_cfg(
                                        cfg_key          = 'deffault',
                                        cfg_extras       = {},
                                        dirpath_lwc_root = dirpath_lwc_root)
        assert isinstance(default_config, dict)
        assert 'cfg_name' in default_config
        assert default_config['cfg_name'] == 'default'
        assert len(default_config) == 8  # At least some data returned.

    # -------------------------------------------------------------------------
    def it_creates_configuration_when_cfg_key_can_act_as_a_restriction(
                                                    self, dirpath_lwc_root):
        """
        ---
        i00000_generate_configuration_based_on_a_build_restriction:
          - "When provided with a cfg_key that does not exactly match any
            existing build configuration file in the local working copy and
            that does match one or more design elements in the local working
            copy then the load_cfg function SHALL generate configuration
            that is suitable for building those elements and those elements
            alone."
          - notes: "Approximately matching can be implementation defined."
          - type:  mandate
          - state: draft
        ...
        """
        import da.bldcfg
        default_config = da.bldcfg.load_cfg(
                                        cfg_key          = 'bldcfg',
                                        cfg_extras       = {},
                                        dirpath_lwc_root = dirpath_lwc_root)
        assert isinstance(default_config, dict)
        assert 'cfg_name' in default_config
        assert default_config['cfg_name'] == 'bldcfg'
        assert len(default_config) == 8  # At least some data returned.


# =============================================================================
class SpecifyIsInRestrictedBuild:

    # -------------------------------------------------------------------------
    def it_returns_true_when_the_restriction_matches_the_filename_root(self):
        """
        ---
        i00000_accept_design_documents_matching_a_filename_restriction:
          - "When the restriction string is equal to the root of the filename
            then the is_in_restricted_build function SHALL return boolean
            True."
          - notes: "The root of the filename is the filename without extension
                   or delimiter. For a file named foo.txt, foo is the root and
                   .txt is the extension."
          - type: mandate
          - state: draft
        ...
        """
        import da.bldcfg
        relpath      = '/dirname1/dirname2/dirname3/filename.ext'
        restriction  = ['filename']
        return_value = da.bldcfg.is_in_restricted_build(relpath, restriction)
        assert return_value is True

    # -------------------------------------------------------------------------
    def it_returns_true_when_restriction_matches_a_directory_name(self):
        """
        ---
        i00000_accept_design_documents_matching_a_directory_name_restriction:
          - "When the restriction string is equal to the name of one of
            the directories in the relpath then the is_in_restricted_build
            function SHALL return boolean True."
          - type: mandate
          - state: draft
        ...
        """
        import da.bldcfg
        relpath      = '/dirname1/dirname2/dirname3/filename.ext'
        restriction  = ['dirname2']
        return_value = da.bldcfg.is_in_restricted_build(relpath, restriction)
        assert return_value is True

    # -------------------------------------------------------------------------
    def it_returns_false_when_restriction_does_not_match_relpath(self):
        """
        ---
        i00000_reject_design_documents_not_matching_the_build_restriction:
          - "When the restriction string is not equal to the root of the
            filename in the relpath string and the restriction string is
            not equal to the name of any one of the directories in the
            relpath string then the is_in_restricted_build function SHALL
            return boolean False."
          - type: mandate
          - state: draft
        ...
        """
        import da.bldcfg
        relpath      = '/dirname1/dirname2/dirname3/filename.ext'
        restriction  = ['dirname4']
        return_value = da.bldcfg.is_in_restricted_build(relpath, restriction)
        assert return_value is False

    # -------------------------------------------------------------------------
    def it_returns_false_when_restriction_is_the_empty_string(self):
        """
        ---
        i00000_a_zero_length_restriction_string_rejects_all_relpaths:
          - "When the restriction string is a zero length string then the
            is_in_restricted_build function SHALL return boolean False."
          - type: mandate
          - state: draft
        ...
        """
        import da.bldcfg
        relpath      = '/dirname1/dirname2/dirname3/filename.ext'
        restriction  = ['']
        return_value = da.bldcfg.is_in_restricted_build(relpath, restriction)
        assert return_value is False

    # -------------------------------------------------------------------------
    def it_returns_false_when_relpath_is_the_empty_string(self):
        """
        ---
        i00000_a_zero_length_relpath_string_is_always_rejected:
          - "When the relpath string is a zero length string then the
            is_in_restricted_build function SHALL return boolean False."
          - type: mandate
          - state: draft
        ...
        """
        import da.bldcfg
        relpath      = ''
        restriction  = ['dirname2']
        return_value = da.bldcfg.is_in_restricted_build(relpath, restriction)
        assert return_value is False


# =============================================================================
class Specify_ExactMatchOrNone:

    # -------------------------------------------------------------------------
    def it_finds_configuration_data_when_cfg_name_matches_exactly(
                                                    self, dirpath_lwc_root):
        import da.bldcfg.bldcfg
        (cfg_name, cfg_data, misses) = da.bldcfg.bldcfg._exact_match_or_none(
                            cfg_name         = 'default',
                            dirpath_lwc_root = dirpath_lwc_root)

        assert cfg_name == 'default'
        assert cfg_data is not None
        assert misses is not None

    # -------------------------------------------------------------------------
    def it_returns_none_when_cfg_name_does_not_exist(self, dirpath_lwc_root):
        import da.bldcfg.bldcfg
        (cfg_name, cfg_data, misses) = da.bldcfg.bldcfg._exact_match_or_none(
                            cfg_name         = 'not_existing_configuration',
                            dirpath_lwc_root = dirpath_lwc_root)

        assert cfg_name is None
        assert cfg_data is None
        assert misses is not None


# =============================================================================
class Specify_BuildRestrictionOrNone:

    # -------------------------------------------------------------------------
    def it_is_a_function(self):
        import da.bldcfg.bldcfg
        assert callable(da.bldcfg.bldcfg._build_restriction_or_none)


# =============================================================================
class Specify_FuzzyMatchOrNone:

    # -------------------------------------------------------------------------
    def it_returns_config_for_an_exact_match(self, monkeypatch):
        import da.bldcfg.bldcfg
        monkeypatch.setattr(da.util, 'load', lambda _: {'cfg': 'from mock'})
        query        = 'build_cfg_id'
        candidates   = {'build_cfg_id': 'dirname/build_cfg_id.build.yaml'}
        (cfg_name, cfg_data) = da.bldcfg.bldcfg._fuzzy_match_or_none(
                                                    query      = query,
                                                    candidates = candidates)
        assert cfg_name is not None
        assert cfg_data is not None

    # -------------------------------------------------------------------------
    def it_returns_config_for_a_near_match(self, monkeypatch):
        import da.bldcfg.bldcfg
        monkeypatch.setattr(da.util, 'load', lambda _: {'cfg': 'from mock'})
        query        = 'uild_cfg_'
        candidates   = {'build_cfg_id': 'dirname/build_cfg_id.build.yaml'}
        (cfg_name, cfg_data) = da.bldcfg.bldcfg._fuzzy_match_or_none(
                                                    query      = query,
                                                    candidates = candidates)
        assert cfg_name is not None
        assert cfg_data is not None

    # -------------------------------------------------------------------------
    def it_returns_none_for_a_non_match(self, monkeypatch):
        import da.bldcfg.bldcfg
        monkeypatch.setattr(da.util, 'load', lambda _: {'cfg': 'from mock'})
        query        = 'Nothing like any candidate'
        candidates   = {'build_cfg_id': 'dirname/build_cfg_id.build.yaml'}
        (cfg_name, cfg_data) = da.bldcfg.bldcfg._fuzzy_match_or_none(
                                                    query      = query,
                                                    candidates = candidates)
        assert cfg_name is None
        assert cfg_data is None


# =============================================================================
class Specify_GenConfigFiles:

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.bldcfg.bldcfg
        assert callable(da.bldcfg.bldcfg._gen_config_files)


# =============================================================================
class Specify_AssembleCfg:

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.bldcfg.bldcfg
        assert callable(da.bldcfg.bldcfg._assemble_cfg)


# =============================================================================
class Specify_CreateBuildContextRecord:

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.bldcfg.bldcfg
        assert callable(da.bldcfg.bldcfg._create_build_context_record)


# =============================================================================
class Specify_CreateTimestamps:

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.bldcfg.bldcfg
        assert callable(da.bldcfg.bldcfg._create_timestamps)


# =============================================================================
class Specify_CreatePathsRecord:

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        import da.bldcfg.bldcfg
        assert callable(da.bldcfg.bldcfg._create_paths_record)
