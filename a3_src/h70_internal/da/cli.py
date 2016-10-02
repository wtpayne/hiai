# -*- coding: utf-8 -*-
"""
Development Automation System Command Line Interface.

This module handles the Development Automation Command
Line Interface. It makes use of the click library
(click.pocoo.org) for input parameter parsing and
command dispatch.

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


import datetime
import importlib
import os
import warnings

import click

import da.lwc.discover


# =============================================================================
class ExitWithCode(click.ClickException):
    """
    Raise this Exception to exit the application with a specified exit code.

    """

    def __init__(self, exit_code, message=None):
        """
        Return a constructed ExitWithCode Exception object.

        """
        super(ExitWithCode, self).__init__(message)
        super(ExitWithCode, self).__setattr__('exit_code', exit_code)

    def show(self, file=None):
        """
        Display the error message to the appropriate file if it has been set.

        """
        if file is None:

            # Pylint rule W0212 (protected-access)
            # disabled at risk to enable use of
            # internal (non-public) Click library
            # functionality.
            #
            file = click._compat.get_text_stderr()      # pylint: disable=W0212

        if self.message is not None:
            click.echo(self.format_message(), file = file)


# =============================================================================
class CustomContextObject(dict):
    """
    Custom context information for the DA CLI.

    """

    pass


# -----------------------------------------------------------------------------
# Pylint rule C0103 (invalid-name) disabled by
# design decision.
#
# The pass_custom_ctx variable is a decorator
# function, not an item of constant data, so an
# all-caps name would be misleading.
#
pass_custom_ctx = click.make_pass_decorator(            # pylint: disable=C0103
                                CustomContextObject)


# =============================================================================
class FuzzyCommandAliasGroup(click.Group):
    """
    Command group that allows for fuzzy matching of command names.

    """

    def get_command(self, ctx, cmd_key):
        """
        Return the command given by fuzzily matching a supplied command alias.

        """
        # Note: Plugins need to be loaded at import
        #       time so that they will appear in the
        #       help text. It isn't sufficient to
        #       import plugins here.

        # Try an exact match.
        key_norm     = cmd_key.lower()
        command_list = self.list_commands(ctx)
        if key_norm in command_list:
            return click.Group.get_command(self, ctx, key_norm)

        # Try a prefix match.
        matches = [cmd for cmd in command_list
                   if cmd.startswith(cmd_key) or cmd_key.startswith(cmd)]
        if len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])

        # Explicitly reject ambiguous prefix matches.
        if len(matches) > 1:
            ctx.fail(
                'Too many matching commands: %s' % ', '.join(sorted(matches)))

        # Try a fuzzy match.
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import fuzzywuzzy.process
        (match, score) = fuzzywuzzy.process.extractOne(key_norm, command_list)
        if score > 80:
            return click.Group.get_command(self, ctx, match)

        # Default to the build command if nothing else matches, ensuring that
        # we pass through the build config parameter if given.
        #
        build_command           = click.Group.get_command(self, ctx, 'build')
        build_cfg_param         = build_command.params[0]
        build_cfg_param.default = cmd_key
        return build_command


# -----------------------------------------------------------------------------
def fuzzy_alias_group(name = None, cls = None, **attrs):
    """
    Create a FuzzyCommandAliasGroup and set the decorated function as callback.

    Once decorated the function turns into a click command Group.

    args:

        name:   The name of the command. This defaults
                to the function name.

        cls:    The class to instantiate. Default is
                FuzzyCommandAliasGroup.

    """
    attrs.setdefault('invoke_without_command', True)
    if cls is None:
        cls = FuzzyCommandAliasGroup

    def decorator(func):
        """
        Return Click decorator function for FuzzyCommandAliasGroup callbacks.

        """
        # Pylint rule W0212 (protected-access)
        # disabled at risk to enable use of internal
        # (non-public) Click library functionality.
        #
        cmd = click.decorators._make_command(           # pylint: disable=W0212
                                    func, name, attrs, cls)

        # Pylint rule W0201 (attribute-defined-outside-init)
        # disabled at risk to support integration
        # with Click library functionality.
        #
        cmd.__doc__ = func.__doc__                      # pylint: disable=W0201
        return cmd

    return decorator


# =============================================================================
class ExplicitInfoNameCommand(click.Command):
    """
    A Command that creates Contexts with an explicitly specified info_name.

    This class ensures that the usage message always
    displays the correct command name rather than
    using the user's input string from sys.argv.

    It is a subclass of click.Command with the
    make_context method overridden so that the
    Context class from which the usage message
    is supplied takes its info_name from
    Command.name rather than from sys.argv.

    """

    def make_context(self, info_name, args, parent, **extra):
        """
        Return the Command Context with info_name explicitly set to self.name.

        """
        return super(ExplicitInfoNameCommand, self).make_context(
                                                        info_name = self.name,
                                                        args      = args,
                                                        parent    = parent,
                                                        **extra)


# -----------------------------------------------------------------------------
def exit_application(exit_code = 0, message = None):
    """
    Halt the application with the specified exit code and message.

    """
    raise ExitWithCode(exit_code, message)


# -----------------------------------------------------------------------------
@fuzzy_alias_group(name = 'main')
@click.pass_context
def main(click_ctx):
    """
    The main entry point for Development Automation System commands.

    The Development Automation System defines and
    controls the development process and is the
    basis for engineering process compliance
    monitoring and automation.

    Wherever possible development process steps are
    carried out or reported via this tool.

    """
    if click_ctx.invoked_subcommand is None:
        click_ctx.forward(build)


# -----------------------------------------------------------------------------
@main.command(
    cls  = ExplicitInfoNameCommand,
    name = 'build',
    context_settings = {'allow_extra_args': True})
@pass_custom_ctx
@click.pass_context
@click.argument(
    'cfg_name',
    type     = click.STRING,
    required = False,
    default  = 'default',
    envvar   = 'DA_CFG_NAME')
@click.option(
    '-t', '--datetime_utc',
    help    = 'Build UTC date/time stamp.',
    default = datetime.datetime.utcnow())
def build(click_ctx, da_ctx, cfg_name, datetime_utc):
    """
    Build current LWC with CFG_NAME build config.

    CFG_NAME can be the name of a configuration
    file or the name of a design element.

    If the name of a design element is supplied,
    then configuration is generated automatically
    to restrict the build to that design element
    only.

    The notion of a build is quite general. Any
    action that can be done in a single step and
    that produces some sort of persistent output
    should be thought of as part of the build.

    The only exceptions are actions that start
    interactive sessions or other processes,
    e.g. launching interactive tools, reporting
    servers etc..

    """
    # Rename imports to prevent conflict with
    # outer da imports.
    #
    import sys
    import traceback
    import da.metabuild as _metabuild
    import da.constants as _constants
    import da.exception as _exception
    import da.lwc.run   as _run

    # Some of the build configuration can only be
    # defined at runtime.
    cfg_extras = {
        'build_context': {
            'pid':              da_ctx['pid'],
            'outer_cmd':        da_ctx['outer_cmd'],
            'cmd_args':         da_ctx['args'],
            'unmatched_args':   click_ctx.args
        },
        'paths': {
            'dirpath_lwc_root': da_ctx['dirpath_lwc_root'],
            'dirpath_cwd':      da_ctx['dirpath_cwd']
        },
        'timestamp': {
            'datetime_utc':     datetime_utc
        },
        'options': {}
    }

    exit_code = _constants.META_BUILD_ABORTED
    try:

        exit_code = _metabuild.main(
                                cfg_key          = cfg_name,
                                cfg_extras       = cfg_extras,
                                dirpath_lwc_root = da_ctx['dirpath_lwc_root'])

        # The build either returns _metabuild.COMPLETED or throws an exception.
        assert exit_code == _constants.META_BUILD_COMPLETED

    except _exception.AbortSilently:
        pass

    except _exception.AbortWithoutStackTrace as abort:

        # We often want to abort the build in circumstances which do not
        # warrant the display of a stack trace.
        #
        click.secho(
            '\n{title}\n\n{message}\n'.format(title   = 'Nonconformity:',
                                              message = abort.message),
            fg = 'red')

        if os.path.isfile(abort.filepath):
            filepath    = abort.filepath
            line_number = abort.line_number if abort.line_number else 1
            if line_number == -1:
                with open(filepath) as file:
                    line_number = sum(1 for line in file)
            _run.subl(dirpath_lwc_root = da_ctx['dirpath_lwc_root'],
                      filepath         = filepath,
                      line_number      = line_number)

    # Pylint rule W0703 (broad-except) disabled.
    # All Exception objects are caught because
    # keeping an explicit list of exception
    # classes is not practical given the evolving
    # and low-maturity nature of much of the
    # software that will be doing the throwing.
    #
    except Exception as err:                            # pylint: disable=W0703

        # I find the stack trace that the Python
        # interpreter prints to be a bit dense
        # and hard to read, so instead of letting
        # the exception propagate back up the
        # interpreter, we intercept it here and
        # print the stack trace in a manner of
        # our choosing.
        #
        click.secho(
            '\n{hr}\n{title}\n{uscore}\n\n{exc}\n\n{trace}\n{hr}\n'.format(
                                    hr     = '-' * 80,
                                    title  = 'ERROR IN BUILD PROCESS',
                                    uscore = '----------------------',
                                    exc    = repr(err),
                                    trace  = traceback.format_exc(limit=10)),
            fg = 'red')

        # Since we have already intercepted the
        # exception, we can take the opportunity
        # to add hooks for whatever development
        # environment we happen to be using at
        # the momeent (e.g. Eclipse or Sublime).
        #
        # In the first instance, we simply open
        # the editor at the location where the
        # exception was thrown, but in future we
        # may do something more sophisticated7
        # here.
        #
        # TODO: Review and extend IDE integration.
        #
        tb_last_stack_frame = traceback.extract_tb(sys.exc_info()[2])[-1]
        _run.subl(dirpath_lwc_root = da_ctx['dirpath_lwc_root'],
                  filepath         = tb_last_stack_frame[0],
                  line_number      = tb_last_stack_frame[1])

    finally:
        exit_application(exit_code)


# -----------------------------------------------------------------------------
@main.command(
    cls  = ExplicitInfoNameCommand,
    name = 'run')
@click.argument(
    'appname',
    type     = click.Choice(['bash', 'subl']),
    required = True)
@pass_custom_ctx
def run(da_ctx, appname):
    """
    Run app configured for the current LWC.

    """
    import da.lwc.run as _run
    if appname == 'bash':
        return _run.bash(dirpath_lwc_root = da_ctx['dirpath_lwc_root'])

    if appname == 'subl':
        return _run.subl(dirpath_lwc_root = da_ctx['dirpath_lwc_root'])


# -----------------------------------------------------------------------------
@main.command(
    cls  = ExplicitInfoNameCommand,
    name = 'repl')
@click.argument(
    'type',
    type     = click.Choice(['ptpy', 'ipy', 'bpy', 'cpy']),
    required = False,
    default  = 'ptpy',
    envvar   = 'DA_REPL_TYPE')
def repl(type):
    """
    Read Eval Print Loop for the current LWC.

    TYPE can be one of: ptpy, ipy, bpy, cpy.

    ptpy is the ptpython enhanced curses repl.

    ipy  is the ptpython repl in ipython mode.

    bpy  is the bpython enhanced curses repl.

    cpy is the vanilla cpython repl.

    """
    if type == 'ptpy':
        import ptpython.repl
        ptpython.repl.embed(globals(), locals())

    if type == 'ipy':
        import ptpython.ipython
        ptpython.ipython.embed()

    elif type == 'bpy':
        import bpython
        bpython.embed()

    elif type == 'cpy':
        import code
        code.interact()


# -----------------------------------------------------------------------------
@main.group()
def sim():
    """
    Run a simulation.

    This group of commands

    """
    pass


# -----------------------------------------------------------------------------
@sim.command(
    cls  = ExplicitInfoNameCommand,
    name = 'vtx')
@click.argument(
    'logic',
    required = True,
    type     = click.STRING)
@click.argument(
    'cfg',
    required = True,
    type     = click.File(mode = 'rt'))
@click.argument(
    'inputs',
    required = True,
    type     = click.File(mode = 'rt'))
@click.argument(
    'outputs',
    required = True,
    type     = click.File(mode   = 'wt', atomic = True))
def vtx(logic, cfg, inputs, outputs):
    """
    Simulate a single application vertex.

    This script is used to simulate a single algorithm module on its own
    using a pre-recorded sequence of inputs.

    Simulating algorithm modules independently dramatically reduce the
    amount of computation required to tune the paramters of modules in
    the latter stages of the processing pipeline.

    """
    import json
    import yaml
    import runtime.mil

    vertex = runtime.mil.Vertex(cfg         = yaml.safe_load(cfg),
                                module_name = logic)

    for (iline, line) in enumerate(inputs):
        print(iline)
        vertex.inputs = json.loads(line)
        vertex.iter()
        outputs.write(json.dumps(vertex.outputs))


# -----------------------------------------------------------------------------
# Load CLI plugins from each counterparty directory.
#
# ---
# i00041_control_access_to_counterparty_specific_confidential_documents:
#   - "Access to counterparty specific confidential
#      documents SHALL be controlled."
#   - notes: "We want to provide assurance to our
#            counterparties that access controls
#            will be instituted and enforced to
#            protect their confidential information
#            and intellectual property."
#   - type: mandate
#   - state: draft
#
# i00042_organise_documents_for_reuse:
#   - "Documents SHALL be organised to facilitate
#      reuse across projects."
#   - notes: "We want to promote reuse of design
#            documents by adopting a product line
#            engineering approach. This means that
#            many products and projects are aggregated
#            together into a single monolithic
#            configuration."
#   - type: mandate
#   - state: draft
#
# i00043_store_counterparty_confidential_documents_in_secure_subrepos:
#   - "Counterparty specific confidential documents SHALL be stored in
#      access-controlled subrepositories."
#   - notes: "We want to coversion documents with
#            counterparty specific confidentiality
#            alongside product line documents that
#            are open-access across the organisation.
#            To achieve this, we store the confidential
#            documents in an access controlled
#            subrepository that is (optionally)
#            embedded within the encompassing
#            product line organisational structure."
#   - type: mandate
#   - state: draft
#   - ref:
#       - i00041_control_access_to_counterparty_specific_confidential_documents
#       - i00042_organise_documents_for_reuse
#
# i00044_discoverable_processes_and_procedures:
#   - "Processes and procedures SHALL be discoverable."
#   - notes: "We want new members of staff to be
#            able to look up and discover the right
#            processes, procedures and tools for
#            their current task."
#   - type: mandate
#   - state: draft
#
# i00045_single_command_line_entry_point:
#   - "The DA command line tool SHALL permit access to all manually triggered
#      procedures."
#   - notes: "The online help for the DA command
#            line tool is the mechanism whereby
#            team members can discover processes
#            and procedures."
#   - type: mandate
#   - state: draft
#   - ref:
#       - i00044_discoverable_processes_and_procedures
#
# i00046_counterparty_specific_command_line_plugins:
#   - "The DA command line tool SHALL include a
#      plugin mechanism for functions that are
#      confidential to a specific counterparty."
#   - notes: "We want to expose counterparty-specific
#            functionality through the da command-line
#            tool, yet be able to secure access to
#            that functionality to authorised users
#            only. To achieve this goal, the DA
#            command line tool SHALL implement a
#            plugin mechanism to pick up CLI
#            extensions from whatever counterparty
#            specific subrepos that are present."
#   - type: mandate
#   - state: draft
#   - ref:
#       - i00044_discoverable_processes_and_procedures
#       - i00041_control_access_to_counterparty_specific_confidential_documents
#       - i00042_organise_documents_for_reuse
# ...
def _gen_plugin_subgroups(rootpath, relpath = None):
    """
    Yield all CLI plugin command (sub) groups in the given directory.

    ---
    type: generator

    args:
        rootpath:
            The directory path to the import root.

        relpath:
            The relative path to the directory where
            a cli_plugin.py module may be found. This
            is used to generate the first part of the
            name under which the cli plugin module
            will be imported.

    yields:
        All click.core.Group objects that are found
        in the plugin module's namespace.

    ...

    """
    if relpath is None:
        relpath = ''

    filepath_plugin = os.path.join(rootpath, relpath, 'cli_plugin.py')

    if not os.path.isfile(filepath_plugin):
        return

    filename         = os.path.basename(filepath_plugin)
    (module_name, _) = os.path.splitext(filename)
    path_parts       = relpath.split(os.sep)
    fullname         = '.'.join(path_parts + [module_name])
    loader           = importlib.machinery.SourceFileLoader(fullname,
                                                            filepath_plugin)
    module           = loader.load_module()

    for value in module.__dict__.values():
        if isinstance(value, click.core.Group):
            subgroup = value
            yield subgroup


# -----------------------------------------------------------------------------
def _load_cli_plugin_group(parent, group_name, group_help, dirpath_root):
    """
    Load all CLI plugins in the specified directory.

    This function will iterate over all subdirectories
    in dirpath_root, loading all cli_plugin.py modules
    that are encountered.

    ---
    type: function

    args:
        parent:
            Click command group within which the plugins will live.

        group_name:
            The name used to invoke this group in the CLI.

        group_help:
            Help text for plugins.

        dirpath_root:
            Directory path containing the plugins.

    returns:
        None

    ...

    """
    def no_op():
        """
        No-op callback function for generated CLI groups.

        """
        pass

    group = click.group(name = group_name,
                        help = group_help)(no_op)
    parent.add_command(group)                           # pylint: disable=E1101

    filepath_plugin = os.path.join(dirpath_root, 'cli_plugin.py')
    if os.path.isfile(filepath_plugin):
        for subgroup in _gen_plugin_subgroups(dirpath_root):
            group.add_command(subgroup)                 # pylint: disable=E1101

    for dirname in os.listdir(dirpath_root):
        for subgroup in _gen_plugin_subgroups(dirpath_root, dirname):
            group.add_command(subgroup)                 # pylint: disable=E1101


_load_cli_plugin_group(
    parent       = main,
    group_name   = 'res',
    group_help   = 'Run a research utility or test.',
    dirpath_root = da.lwc.discover.path('research'))

_load_cli_plugin_group(
    parent       = main,
    group_name   = 'prj',
    group_help   = 'Run a project specific utility or test.',
    dirpath_root = da.lwc.discover.path('project'))

_load_cli_plugin_group(
    parent       = main,
    group_name   = 'demo',
    group_help   = 'Run a demo.',
    dirpath_root = da.lwc.discover.path('demo'))
