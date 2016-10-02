# -*- coding: utf-8 -*-
"""
Unit tests for the da.commit_message module.

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


import textwrap


# =============================================================================
class SpecifyCompose:
    """
    Specify the da.commit_message.compose() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The compose() function is callable.

        """
        import da.commit_message
        assert callable(da.commit_message.compose)


# =============================================================================
class SpecifyParse:
    """
    Specify the da.commit_message.parse() function.

    """

    # -------------------------------------------------------------------------
    def it_parses_well_formed_commit_messages(self):
        """
        The parse() function parses a well formed commit message.

        """
        import da.commit_message
        example_message = textwrap.dedent("""
        c000|p0000|j0000000|Development Automation Bootstrap

        ---
        work_summary:    Development Automation Bootstrap

        work_notes:      We have a basic skeleton build-system in place and
                         available. Some of the basic infrastructure behind
                         traceability (indexing) is in place. We can generate
                         commit messages automatically from our diary entries,
                         and can automatically squash similar commits
                         together. Previous git history has been erased to
                         remove large numbers of spurious commits and to
                         ensure that the history may be processed in a fairly
                         uniform manner.

        job_id:          j0000000_bootstrap_development_automation_system

        job_description: We need to bootstrap a simple build system - at least
                         to the point where we can enforce and ensure that
                         commit messages have sufficient information to infer
                         trace relationships - minimising the quantity of the
                         system which is not subject to traceability.

        counterparty_id: c000_orion
        project_id:      p0000_da
        mandate:
          - i00007_mandate
          - i00008_development_automation

        ...
        """)
        commit_message_data = da.commit_message.parse(example_message)

        assert commit_message_data['work_summary'] == \
                    'Development Automation Bootstrap'

        assert commit_message_data['work_notes'] ==                           \
                    'We have a basic skeleton build-system in place and '     \
                    'available. Some of the basic infrastructure behind '     \
                    'traceability (indexing) is in place. We can generate '   \
                    'commit messages automatically from our diary entries, '  \
                    'and can automatically squash similar commits '           \
                    'together. Previous git history has been erased to '      \
                    'remove large numbers of spurious commits and to '        \
                    'ensure that the history may be processed in a fairly '   \
                    'uniform manner.'

        assert commit_message_data['job_id'] == \
                    'j0000000_bootstrap_development_automation_system'

        assert commit_message_data['job_description'] ==                      \
                    'We need to bootstrap a simple build system - at least '  \
                    'to the point where we can enforce and ensure that '      \
                    'commit messages have sufficient information to infer '   \
                    'trace relationships - minimising the quantity of the '   \
                    'system which is not subject to traceability.'

        assert commit_message_data['counterparty_id'] == 'c000_orion'

        assert commit_message_data['project_id'] == 'p0000_da'

        assert commit_message_data['mandate'] == [
                    'i00007_mandate', 'i00008_development_automation']

    # -------------------------------------------------------------------------
    def it_fails_gracefully_with_a_malformed_commit_message(self):
        """
        It fails gracefully when given malformed commit message.

        """
        import da.commit_message
        example_message = textwrap.dedent('This is a malformed commit message')
        commit_message_data = da.commit_message.parse(example_message)

        assert commit_message_data['work_summary']    is None
        assert commit_message_data['work_notes']      is None
        assert commit_message_data['job_id']          is None
        assert commit_message_data['job_description'] is None
        assert commit_message_data['counterparty_id'] is None
        assert commit_message_data['project_id']      is None
        assert commit_message_data['mandate']         == []
