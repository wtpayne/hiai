# -*- coding: utf-8 -*-
"""
Unit tests for the da.cli module.

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


import click

import pytest




# =============================================================================
class SpecifyFuzzyAliasGroup:
    """
    Specify the da.cli.fuzzy_alias_group() function.

    """

    def it_is_callable(self):
        """
        The fuzzy_alias_group() function is callable.

        """
        import da.cli
        assert callable(da.cli.fuzzy_alias_group)


# =============================================================================
class SpecifyExitWithCodeShow:
    """
    Specify the da.cli.ExitWithCode.show() method.

    """

    def it_is_callable(self):
        """
        The show() method is callable.

        """
        import da.cli
        assert callable(da.cli.ExitWithCode.show)


# =============================================================================
class SpecifyExplicitInfoNameCommandMakeContext:
    """
    Specify the da.cli.ExplicitInfoNameCommand.make_context() method.

    """

    def it_is_callable(self):
        """
        The make_context() method is callable.

        """
        import da.cli
        assert callable(da.cli.ExplicitInfoNameCommand.make_context)


# =============================================================================
class SpecifyFuzzyCommandAliasGroupGetCommand:
    """
    Specify the da.cli.FuzzyCommandAliasGroup.get_command() method.

    """

    def it_is_callable(self):
        """
        The get_command() method is callable.

        """
        import da.cli
        assert callable(da.cli.FuzzyCommandAliasGroup.get_command)


# =============================================================================
class SpecifyExitApplication:
    """
    Specify the da.cli.exit_application() function.

    """

    # -------------------------------------------------------------------------
    def it_raises_an_clickexception(self):
        """
        Placeholder test case.

        """
        import da.cli
        test_exit_code    = 42
        test_exit_message = 'Test exit message'
        with pytest.raises(click.ClickException) as exc:
            da.cli.exit_application(exit_code = test_exit_code,
                                    message   = test_exit_message)
            assert exc.exit_code == test_exit_code
            assert exc.message   == test_exit_message


# =============================================================================
class SpecifyMain:
    """
    Specify the da.cli.main() function.

    """

    def it_is_callable(self):
        """
        The main() function is callable.

        """
        import da.cli
        assert callable(da.cli.main)


# =============================================================================
class SpecifyBuild:
    """
    Specify the da.cli.build() function.

    """

    def it_is_callable(self):
        """
        The build() function is callable.

        """
        import da.cli
        assert callable(da.cli.build)


# =============================================================================
class SpecifyRun:
    """
    Specify the da.cli.run() function.

    """

    def it_is_callable(self):
        """
        The run() function is callable.

        """
        import da.cli
        assert callable(da.cli.run)


# =============================================================================
class SpecifyRepl:
    """
    Specify the da.cli.repl() function.

    """

    def it_is_callable(self):
        """
        The repl() function is callable.

        """
        import da.cli
        assert callable(da.cli.repl)


# =============================================================================
class SpecifySim:
    """
    Specify the da.cli.sim() function.

    """

    def it_is_callable(self):
        """
        The sim() function is callable.

        """
        import da.cli
        assert callable(da.cli.sim)


# =============================================================================
class SpecifyVtx:
    """
    Specify the da.cli.vtx() function.

    """

    def it_is_callable(self):
        """
        The vtx() function is callable.

        """
        import da.cli
        assert callable(da.cli.vtx)


# =============================================================================
class Specify_GenPluginSubgroups:
    """
    Specify the da.cli._gen_plugin_subgroups() function.

    """

    def it_is_callable(self):
        """
        The _gen_plugin_subgroups() function is callable.

        """
        import da.cli
        assert callable(da.cli._gen_plugin_subgroups)


# =============================================================================
class Specify_LoadCliPluginGroup:
    """
    Specify the da.cli._load_cli_plugin_group() function.

    """

    def it_is_callable(self):
        """
        The _load_cli_plugin_group() function is callable.

        """
        import da.cli
        assert callable(da.cli._load_cli_plugin_group)
