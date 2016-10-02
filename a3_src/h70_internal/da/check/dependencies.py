# -*- coding: utf-8 -*-
"""
Dependencies register functions.

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


import difflib
import io
import json
import os
import os.path

import git

import da.check.constants
import da.register
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(dirpath_lwc_root, build_monitor):
    """
    Check the dependencies register for nonconformities.

    """
    while True:

        build_unit = (yield)
        if not build_unit['filepath'].endswith('dependencies.register.json'):
            continue

        reg = _load_register(dirpath_lwc_root)
        _check_register_format(reg, build_monitor)
        _compare_with_filesystem(reg, build_monitor, dirpath_lwc_root)


# -----------------------------------------------------------------------------
def _load_register(dirpath_lwc_root):
    """
    Return collated and loaded dependencies register file information.

    """
    dirpath  = da.lwc.discover.path(key = 'registry',
                                    dirpath_lwc_root = dirpath_lwc_root)
    filepath = os.path.join(dirpath, 'dependencies.register.json')

    with open(filepath, 'r') as file:
        json_text = file.read()

    data = json.loads(json_text)

    return {
        'filepath':    filepath,
        'text':        json_text,
        'data':        data
    }


# -----------------------------------------------------------------------------
def _compare_with_filesystem(reg, build_monitor, dirpath_lwc_root):
    """
    Compare the content of the dependencies register with the filesystem.

    Is the dependencies register consistent with the content of the
    depencencies directories (a0_env) on the filesystem.

    """
    rootpath_env     = da.lwc.discover.path(
                                        key              = 'env',
                                        dirpath_lwc_root = dirpath_lwc_root)
    rootpath_env_src = os.path.join(rootpath_env, 'src')

    regdata          = da.lwc.env.dependencies_register(
                                       dirpath_lwc_root = dirpath_lwc_root)

    dirpath_curr_env = da.lwc.discover.path(
                                        key              = 'current_env',
                                        dirpath_lwc_root = dirpath_lwc_root)

    # Missing configuration.
    set_src = {it.name for it in os.scandir(rootpath_env_src) if it.is_dir()}
    set_bin = {it.name for it in os.scandir(dirpath_curr_env) if it.is_dir()}
    set_cfg = {it['dirname'] for it in regdata.values()}
    on_disc = (set_src | set_bin)
    no_cfg  = on_disc - set_cfg
    for name in sorted(no_cfg):
        message = 'No dependency configuration for {name}'.format(name = name)
        build_monitor.report_nonconformity(
                                tool   = 'da.check.dependencies',
                                msg_id = da.check.constants.DEP_NO_CONFIG,
                                msg    = message,
                                path   = reg['filepath'])

    # Repositories used.
    for (key, value) in regdata.items():
        relpath_src = os.path.join(value['dirname'], value['policy'])
        dirpath_src = os.path.join(rootpath_env_src, relpath_src)

        # Mercurial?
        dirpath_hg  = os.path.join(dirpath_src, '.hg')
        if os.path.isdir(dirpath_hg):
            if value['config']['url'] == 'TBD':
                message = 'No mercurial url for {key}'.format(key = key)
                build_monitor.report_nonconformity(
                                    tool   = 'da.check.dependencies',
                                    msg_id = da.check.constants.DEP_NO_HG_URL,
                                    msg    = message,
                                    path   = reg['filepath'])
            # hg paths

        # Git?
        dirpath_git = os.path.join(dirpath_src, '.git')
        if os.path.isdir(dirpath_git):
            repo = git.Repo(dirpath_src)
            if len(repo.remotes) == 0:
                continue
            url = repo.remotes.origin.url
            if url != value['config']['url']:
                message = 'Bad git url for {key}'.format(key = key)
                build_monitor.report_nonconformity(
                                    tool   = 'da.check.dependencies',
                                    msg_id = da.check.constants.DEP_NO_GIT_URL,
                                    msg    = message,
                                    path   = reg['filepath'])

    # regdata    =
    # for key, dep in regdata.items():
    #     dirname_dep = dep['dirname']
    #     dirname_pol = dep['policy']
    #     dirpath_src = os.path.join(dirpath_env_src, dirname_dep, dirname_pol)

    #     if not os.path.isdir(dirpath_src):
    #         raise RuntimeError('PATH NOT FOUOND: {path}'.format(
    #                                                     path = dirpath_src))

    # dirpath_env_bin = os.path.join(dirpath_env,
    #                                'e00_x86_64_linux_ubuntu_xenial')


# -----------------------------------------------------------------------------
def _check_register_format(reg, build_monitor):
    """
    Check the register format.

    We do this by generating a perfectly formatted version and
    then comparing it to the version on disc.

    Any discrepancy will be reported as a design nonconformity.

    """
    register_text  = reg['text']
    reference_text = _format_register(reg['data'])
    if reference_text != register_text:

        reference_lines = reference_text.splitlines()
        register_lines  = register_text.splitlines()
        iline = 0
        for iline, lines in enumerate(zip(reference_lines, register_lines)):
            (ref_line, reg_line) = lines
            if ref_line != reg_line:
                break

        diff_text = '\n'.join((line for line in difflib.context_diff(
                                                        reference_lines,
                                                        register_lines,
                                                        'reference_format',
                                                        'current_register')))
        msg = 'Dependencies register format error '\
              'on line {line}:\n{diff}'.format(line = iline,
                                               diff = diff_text)

        build_monitor.report_nonconformity(
                            tool    = 'da.check.dependencies',
                            msg_id  = da.check.constants.DEP_REGISTER_FORMAT,
                            msg     = msg,
                            path    = reg['filepath'])


# -----------------------------------------------------------------------------
def _format_register(register_data):
    """
    Return a formatted register document.

    """
    json_doc = VerticallyAlignedJSON()
    json_doc >>= None
    json_doc = _add_register_header(json_doc, register_data)
    json_doc >>= 'register'
    for (name, entry) in sorted(register_data['register'].items()):
        json_doc += None
        json_doc >>= name
        json_doc = _add_register_entry(json_doc, entry)
        json_doc <<= name
    json_doc <<= 'register'
    json_doc <<= None
    return str(json_doc)


# -----------------------------------------------------------------------------
def _add_register_header(json_doc, register_data):
    """
    Add the dependencies register header information to the supplied JSON doc.

    """
    json_doc += None
    json_doc += ('title',           register_data['title'])
    json_doc += None
    json_doc += ('introduction',    register_data['introduction'])
    json_doc += None
    return json_doc


# -----------------------------------------------------------------------------
def _add_register_entry(json_doc, entry):
    """
    Add a single dependencies registry entry to the supplied JSON doc.

    """
    json_doc += ('desc',    entry['desc'])
    json_doc += ('notes',   entry['notes'])
    json_doc += ('dirname', entry['dirname'])
    json_doc += ('policy',  entry['policy'])
    json_doc = _add_api_section(    json_doc, entry)
    json_doc = _add_cli_section(    json_doc, entry)
    json_doc = _add_gui_section(    json_doc, entry)
    json_doc = _add_config_section( json_doc, entry)
    json_doc = _add_build_section(  json_doc, entry)

    return json_doc


# -----------------------------------------------------------------------------
def _add_api_section(json_doc, entry):
    """
    Add an API section to the supplied JSON doc.

    """
    json_doc >>= 'api'
    for (api_name, api_path) in sorted(entry['api'].items()):
        json_doc += (api_name, api_path)
    json_doc <<= 'api'
    return json_doc


# -----------------------------------------------------------------------------
def _add_cli_section(json_doc, entry):
    """
    Add a CLI section to the supplied JSON doc.

    """
    json_doc >>= 'cli'
    for (cli_name, cli_path) in sorted(entry['cli'].items()):
        json_doc += (cli_name, cli_path)
    json_doc <<= 'cli'
    return json_doc


# -----------------------------------------------------------------------------
def _add_gui_section(json_doc, entry):
    """
    Add a GUI section to the supplied JSON doc.

    """
    json_doc >>= 'gui'
    for (gui_name, gui_path) in sorted(entry['gui'].items()):
        json_doc += (gui_name, gui_path)
    json_doc <<= 'gui'
    return json_doc


# -----------------------------------------------------------------------------
def _add_config_section(json_doc, entry):
    """
    Add a config section to the supplied JSON doc.

    """
    json_doc >>= 'config'
    json_doc += ('method',  entry['config']['method'])
    json_doc += ('tool',    entry['config']['tool'])
    json_doc += ('url',     entry['config']['url'])
    json_doc <<= 'config'
    return json_doc


# -----------------------------------------------------------------------------
def _add_build_section(json_doc, entry):
    """
    Add a build section to the supplied JSON doc.

    """
    json_doc >>= 'build'
    json_doc += ('method',  entry['build']['method'])
    json_doc += ('tool',    entry['build']['tool'])
    json_doc <<= 'build'
    return json_doc


# =============================================================================
# disabled pylint rule R0903 - too-few-public-methods
# because this class mainly uses operator overloading
# rather than traditional methods. Probably not OK for
# safety critical stuff -- but fine for formatting
# configuration files as we are doing here. (IMHO).
#
class VerticallyAlignedJSON():                          # pylint: disable=R0903
    """
    Vertically aligned JSON serialisation.

    This class is used to feed my OCD by generating
    JSON format configuration files with content
    that is nicely vertically aligned for human
    comprehension.

    """

    # -------------------------------------------------------------------------
    def __init__(self,
                 indent_size = 4,
                 content_col = 32):
        """
        Return a newly constructed inprint.Doc class.

        """
        self.indent_size    = indent_size
        self.content_col    = content_col

        # The very first '{' in the file does not
        # need to be preceeded by a newline.
        #
        self.newline_needed = False

        # The brace character that opens a new
        # section does not need to be followed
        # by a comma, and neither does the last
        # item in the section.
        #
        self.comma_needed   = False
        self.stack          = []
        self.buffer         = io.StringIO()

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Return document content as a string.

        """
        self.buffer.write('\n')
        return self.buffer.getvalue()

    # -------------------------------------------------------------------------
    def __irshift__(self, name):
        """
        Add a new section to the document and return self.

        The operator >>= function adds a new section
        with the specified name to the document and
        increases the indentation level.

        The parameter on the RHS can be set to None
        to add an anonymous section.

        """
        if name is not None:
            self.buffer.write('{newline}{indent}"{name}": {{'.format(
                                                newline = self._get_newline(),
                                                indent  = self._get_indent(),
                                                name    = name))
        else:
            self.buffer.write('{newline}{indent}{{'.format(
                                                newline = self._get_newline(),
                                                indent  = self._get_indent()))
        self.stack.append(name)
        self.comma_needed = False
        return self

    # -------------------------------------------------------------------------
    def __ilshift__(self, name):
        """
        Set the end of the current section and return self.

        The operator <<= function ends the current
        section and reduces the indentation level.

        If the parameter on the RHS of the operator
        is not None, then it is compared with the
        current section and an exception raised in
        the case of a mismatch.

        """
        prev = self.stack.pop()
        self.comma_needed = False
        self.buffer.write('{newline}{indent}}}'.format(
                                            newline = self._get_newline(),
                                            indent  = self._get_indent()))
        self.comma_needed = True
        if name is not None:
            assert prev == name
        return self

    # -------------------------------------------------------------------------
    def __iadd__(self, item):
        """
        Add an item to the document and return self.

        The operator += function adds the specified
        item to the document.

        """
        if item is None:
            self.buffer.write('{newline}'.format(
                                            newline = self._get_newline()))
            self.comma_needed = False
        else:
            assert len(item) == 2
            self._add_key_value_pair(key   = item[0],
                                     value = item[1])
            self.comma_needed = True
        return self

    # -------------------------------------------------------------------------
    def _add_key_value_pair(self, key, value):
        """
        Add a key-value pair to the document.

        """
        assert len(self.stack) > 0
        assert isinstance(key, str)

        key = '{indent}"{key}": '.format(
                                    indent  = self._get_indent(),
                                    key     = key)
        tab = self.content_col - len(key)
        if tab > 0:
            key += (' ' * tab)

        # Currently I'm only envisaging doing this
        # with simple key-value pairs where key and
        # value are both strings. This function could
        # be extended in future to handle different
        # types, but for the moment we just return
        # an error.
        #
        assert isinstance(value, str)
        self.buffer.write('{newline}{key}"{value}"'.format(
                                                newline = self._get_newline(),
                                                key     = key,
                                                value   = value))

    # -------------------------------------------------------------------------
    def _get_newline(self):
        """
        Return an appropriate line termination and newline as a string.

        """
        # The very first '{' in the file does not
        # need to be preceeded by a newline.
        #
        if not self.newline_needed:
            self.newline_needed = True
            return ''
        if self.comma_needed:
            return ',\n'
        else:
            return '\n'

    # -------------------------------------------------------------------------
    def _get_indent(self):
        """
        Return the current top-level indent as a string.

        """
        num_indents = len(self.stack)
        num_spaces  = num_indents * self.indent_size
        indent      = ' ' * num_spaces
        return indent
