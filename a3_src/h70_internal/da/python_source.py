# -*- coding: utf-8 -*-
"""
Python source file comment scraper.

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
import collections
import enum
import itertools
import os
import sys
import textwrap
import tokenize

import yaml


COMMENT_TYPE = enum.Enum('COMMENT_TYPE', ('DOCSTRING', 'COMMENT'))

MetaComment  = collections.namedtuple('MetaComment',
                                ['lo', 'hi', 'typ'])

MetaYaml     = collections.namedtuple('MetaYaml',
                                ['lo', 'hi', 'ctx_lo', 'ctx_hi', 'ctx_typ'])

MetaNode     = collections.namedtuple('MetaNode',
                                ['lo', 'hi', 'ctx_typ', 'path', 'node'])

Comment      = collections.namedtuple('Comment',
                                ['txt', 'meta'])

Embedded     = collections.namedtuple('Embedded',
                                ['dat', 'meta'])


# -----------------------------------------------------------------------------
def gen_top_level_class_names(ast_root):
    """
    Yield class names defined at the top level of the specified file.

    Classes defined inside functions are not returned.

    """
    for child in _iter_children_with_bodies(ast_root):
        if isinstance(child, ast.ClassDef):
            yield child.name


# -----------------------------------------------------------------------------
def gen_top_level_function_names(ast_root):
    """
    Yield function names defined at the top level of the specified AST.

    Methods inside classes and functions defined
    inside other functions are not returned.

    """
    for child in _iter_children_with_bodies(ast_root):
        if isinstance(child, ast.FunctionDef):
            yield child.name


# -----------------------------------------------------------------------------
def iter_embedded_data(module_name, root, file):
    """
    Yield each piece of embedded data in the file, with associated AST nodes.

    """
    iter_path = _iter_windowed_pairs(
                                gen_ast_paths_depth_first(root, module_name))

    # If iter_path is lazy then:
    # file2 = os.fdopen(os.dup(file.fileno), 'r')
    file.seek(0)
    (path, next_path) = next(iter_path)
    for embed in _gen_embedded_data_in_file(file):

        is_comment = embed.meta.ctx_typ == COMMENT_TYPE.COMMENT
        embed_lo   = embed.meta.ctx_lo
        embed_hi   = embed.meta.ctx_hi

        # Pump the AST node generator.
        while next_path and next_path[-1].lineno < embed_hi:
            (path, next_path) = next(iter_path)

        # Exactly preceding next (upcoming) node -- doxygen style comment.
        if next_path and is_comment and embed_hi + 1 == next_path[-1].lineno:
            node = next_path[-1]
            yield Embedded(dat  = embed.dat,
                           meta = MetaNode(lo      = embed.meta.lo,
                                           hi      = embed.meta.hi,
                                           ctx_typ = embed.meta.ctx_typ,
                                           path    = node.da_addr,
                                           node    = node))
            continue

        # AST node farthest from root is the 'best' (most specific) match.
        for node in reversed(path):
            node_lo = node.lineno
            node_hi = node.da_lineno_last
            if embed_lo >= node_lo and embed_hi <= node_hi:
                yield Embedded(dat  = embed.dat,
                               meta = MetaNode(lo      = embed.meta.lo,
                                               hi      = embed.meta.hi,
                                               ctx_typ = embed.meta.ctx_typ,
                                               path    = node.da_addr,
                                               node    = node))
                break


# -----------------------------------------------------------------------------
def _iter_windowed_pairs(itable):
    """
    Yield pairs of values taken sliding-window-wise from src.

    """
    src  = itertools.chain([None], itable, [None])
    prev = next(src)
    for item in src:
        yield(prev, item)
        prev = item


# -----------------------------------------------------------------------------
def gen_functions(module_name, source_text, root_node):
    """
    Yield functions and methods in the specified file.

    """
    source_lines = source_text.splitlines()
    for path in gen_ast_paths_depth_first(root_node, module_name):
        if not isinstance(path[-1], ast.FunctionDef):
            continue
        fcn_node = path[-1]

        # lineno starts at 1, indices start at 0.
        idx_lo     = fcn_node.lineno - 1
        fcn_indent = _indent_level(source_lines[idx_lo])

        # fcn_node.da_lineno_last is the line on
        # which the last child expression in the
        # function *starts*. It is not always the
        # actual last line in the function. To find
        # the actual last line in the function we
        # need to search forwards a little bit.
        #
        idx_file_end    = len(source_lines)               # Last line in file
        idx_last_child  = fcn_node.da_lineno_last - 1     # Last child in func.

        idx_hi          = idx_file_end
        for idx in range(idx_last_child, idx_file_end):
            line = source_lines[idx]
            if not line or _indent_level(line) > fcn_indent:
                continue
            idx_hi = idx
            break
        function_text = '\n'.join(source_lines[idx_lo:idx_hi])
        setattr(fcn_node, 'da_text', function_text)

        # embedded_data = list(_gen_embedded_data_in_file(
        #                         io.BytesIO(function_text.encode('utf-8'))))
        # setattr(fcn_node, 'da_embedded', embedded_data)

        yield fcn_node


# -----------------------------------------------------------------------------
def _indent_level(line):
    """
    Return the indent level of the specified line.

    """
    return len(line) - len(line.lstrip())


# -----------------------------------------------------------------------------
def gen_ast_paths_depth_first(root, module_name):
    """
    Yield paths to class and function blocks in depth first order.

    This function walks the AST in depth-first order,
    yielding the path to each AST node encountered
    that has a name attribute. At the time of writing,
    the only AST node types that have a name attribute
    are Class definition and Function definition
    nodes.

    Each node in the yielded path is also enhanced
    with a da_addr attribute and a da_lineno_last
    attribute.

    The da_lineno_last attribute, combined with the
    preexisting lineno attribute, serves to precisely
    identify the location of the node's subtree within
    the Python source file. (i.e. the body of the
    class or function definition).

    The da_addr attribute serves to identify the
    location of the node within the Python syntax
    tree.

    The ast.walk function in the Python standard
    library makes no guarantees as to the order
    with which it traverses the AST. At the time
    of writing, it uses a breadth-first traversal
    strategy.

    This function implements an iterative depth-first
    traversal which guarantees that nodes will be
    visited in the same order that they have in the
    original source file. This means that the start
    line number (the lineno attribute) will increase
    monotonically, a fact which may be exploited to
    make merging line-oriented information easier
    and more efficient.

    """
    setattr(root, 'name',    module_name)
    setattr(root, 'da_addr', module_name)
    setattr(root, 'lineno',  0)

    # The ast.walk function (used by the _last_line_in
    # calculation) does not visit comments - which
    # means that trailing comments at the end of the
    # file are ignored. Also, trailing comments in
    # any given function or other block may also be
    # ignored. Drat.
    #
    #   TODO: CHECK THIS.
    #
    # (Reason for using sys.maxsize rather than
    # _last_line_in as was)
    #
    setattr(root, 'da_lineno_last', sys.maxsize)
    iter_child = _iter_children_with_bodies(root)
    stack      = [(root, iter_child)]
    path       = [root]
    yield path

    while stack:
        # Disabling W0622 redefined-builtin because
        # assigning to '_' is how you are supposed
        # to use it dammit.
        #
        (_, iter_child) = stack[-1]                     # pylint: disable=W0622
        try:
            child = next(iter_child)
            stack.append((child, _iter_children_with_bodies(child)))
            if _has_name(child):
                path = [node for (node, _) in stack if _has_name(node)]
                addr = '.'.join([node.name for node in path])
                setattr(child, 'da_addr', addr)
                setattr(child, 'da_lineno_last', _last_line_in(child))
                yield path
        except StopIteration:
            stack.pop()


# -----------------------------------------------------------------------------
def get_module_name(filepath):
    """
    Return the name of the module associated with the specifieed filepath.

    """
    (dirpath, filename) = os.path.split(filepath)
    dirname             = os.path.basename(dirpath)
    if filename == '__init__.py':
        return dirname
    else:
        return os.path.splitext(filename)[0]


# -----------------------------------------------------------------------------
def _has_name(node):
    """
    Return true if node has a name.

    """
    return hasattr(node, 'name') and (node.name is not None)


# -----------------------------------------------------------------------------
def _has_body(node):
    """
    Return true if node has a body.

    """
    return 'body' in node._fields


# -----------------------------------------------------------------------------
def _iter_children_with_bodies(root):
    """
    Return an iterator over those direct child nodes of root that have bodies.

    Since our goal is to find function and class
    definitions, only nodes with bodies are worth
    traversing, as only these nodes have children
    of their own to explore.

    """
    return (node for node in ast.iter_child_nodes(root) if _has_body(node))


# -----------------------------------------------------------------------------
def _last_line_in(node):
    """
    Return the maximum line no. of any node within the subtree rooted at node.

    """
    return max([child.lineno for child in ast.walk(node) if
                                                  hasattr(child, 'lineno')])


# -----------------------------------------------------------------------------
def _gen_embedded_data_in_file(file):
    """
    Yield Embedded named tuples loaded from the specified file.

    """
    for embed in _gen_embedded_data(
                    _merge_comment_blocks(
                        _gen_comment_and_docstr_toks(file))):
        yield embed


# -----------------------------------------------------------------------------
def _gen_embedded_data(gen_blocks):
    """
    Yield Embedded named tuples populated with YAML from supplied text blocks.

    """
    for comment in gen_blocks:

        iter_lines = iter(comment.txt.splitlines())
        is_inside  = False         # Holds parser state.
        yaml_lines = []            # Acts as an accumulator.
        ctxmeta    = comment.meta  # Context metadata (Comment lo; hi; type)
        iline      = 0             # iline is used outside the loop also

        for (iline, line) in enumerate(iter_lines, start = ctxmeta.lo):

            # State transition: outside to inside
            if line.strip() == '---':
                yaml_lo   = iline
                is_inside = True
                continue

            # State transition: inside to outside
            elif line.strip() == '...':
                if yaml_lines:
                    # TODO: TRY ITERATING OVER A YAML.LOAD_ALL?
                    yield Embedded(dat  = yaml.load('\n'.join(yaml_lines)),
                                   meta = MetaYaml(lo      = yaml_lo,
                                                   hi      = iline,
                                                   ctx_lo  = ctxmeta.lo,
                                                   ctx_hi  = ctxmeta.hi,
                                                   ctx_typ = ctxmeta.typ))
                    yaml_lines = []
                is_inside = False
                continue

            # state is inside -> accumulate lines
            # state is outside -> do nothing
            if is_inside:
                yaml_lines.append(line)
            else:
                continue

        # At the end, if we have anything to return, yield it.
        if yaml_lines:
            yield Embedded(dat  = yaml.load('\n'.join(yaml_lines)),
                           meta = MetaYaml(lo      = yaml_lo,
                                           hi      = iline,
                                           ctx_lo  = ctxmeta.lo,
                                           ctx_hi  = ctxmeta.hi,
                                           ctx_typ = ctxmeta.typ))


# -----------------------------------------------------------------------------
def _merge_comment_blocks(gen_comm):
    """
    Yield merged comment blocks.

    ---
    type: generator

    args:
        gen_comm: A generator of named tuples of type 'Comment'

    yields:
        Named tuples of type 'Comment'.
    ...

    """
    def _iter_lookahead(itable):
        """
        Yield items in itable as a tuple together with a next-item lookahead.

        """
        itable_pad = itertools.chain(itable, [None])
        item       = itable_pad.__next__()
        for next_item in itable_pad:
            yield (item, next_item)
            item = next_item

    def _merge(accumulator):
        """
        Return a Comment named-tuple by merging together accumulated Comments.

        """
        return Comment(txt  = '\n'.join(comm.txt for comm in accumulator),
                       meta = MetaComment(lo  = accumulator[0].meta.lo,
                                          hi  = accumulator[-1].meta.hi,
                                          typ = accumulator[0].meta.typ))

    accumulator = []
    for (this_com, next_com) in _iter_lookahead(gen_comm):
        accumulator.append(this_com)
        is_continued = (     next_com is not None
                         and this_com.meta.typ == COMMENT_TYPE.COMMENT
                         and this_com.meta.hi == next_com.meta.lo - 1)
        if not is_continued:
            yield _merge(accumulator)
            accumulator.clear()

    if accumulator:
        yield _merge(accumulator)


# -----------------------------------------------------------------------------
def _gen_comment_and_docstr_toks(file):
    """
    Yield all comment and docstring tokens in the file as named tuples.

    Regular comment lines are straightforward,
    as these are represented by tokens of type
    tokenize.COMMENT, but docstrings present a
    bigger challenge as these are represented
    by tokens of type tokenize.STRING and must
    therefore be distinguished from string
    literal expressions.

    To perform this separation we can use the
    fact that string literals occur only within
    statements. We assume that all string tokens
    that occur outside of statements are
    docstrings.

    For example, indentation inside statements is
    not tokenised, so a preceeding tokenize.INDENT
    token indicates that the current token starts
    a new statement. I.e. can be presumed to be a
    docstring. This seems to reliably detects
    function and class level docstrings, but
    misses out module level docstrings as these
    are not indented.

    The documentation states that tokenize.NL
    indicates a non-terminating newline, whereas
    tokenize.NEWLINE indicates the end of a logical
    line, so if the preceeding token is
    tokenize.NEWLINE, we could infer that the
    current token starts a new statement. I.e. it
    is a (module level) docstring.

    This doesn't seem to be reliably matched by
    reality, as some experiments show the opposite
    behaviour, with a preceeding tokenize.NL
    indicating a module level docstring.

    In practice, our tests indicate that the best
    way to identify module level docstrings is to
    check if the start column is zero rather than
    to rely on preceding NEWLINE or NL tokens.

    This differs from publicly available exemplars,
    so I am a little concerned that we may be
    missing something here.

    ---
    type: generator

    args:
      file:
        An object that implements the readline function. E.g. a file object or
        an instance of any other class that is derived from io.IOBase.

    yields:
      Named tuples of type 'Comment', each containing a single docstring
      token or a commented line token, together with metadata describing
      the type of the token as well as the lower and upper line-number
      bound.

    preconditions:
     - The text in the file must contain syntactically valid Python.
     - No string tokens other than Docstring tokens may start at column zero.

    side_effects:
      - The current position of the file object is modified by this
        function because it calls the file.readline function to obtain
        data.
    ...

    """
    prev_tok = None
    for tok in tokenize.tokenize(file.readline):
        if tok.type == tokenize.COMMENT:
            yield Comment(txt  = tok.string.strip().lstrip('#'),
                          meta = MetaComment(lo  = tok.start[0],
                                             hi  = tok.end[0],
                                             typ = COMMENT_TYPE.COMMENT))
        elif tok.type == tokenize.STRING:
            is_after_indent   = prev_tok and prev_tok.type == tokenize.INDENT
            is_at_column_zero = tok.start[1] == 0
            if is_after_indent or is_at_column_zero:
                yield Comment(txt  = textwrap.dedent(
                                        ast.literal_eval(tok.string)).strip(),
                              meta = MetaComment(lo  = tok.start[0],
                                                 hi  = tok.end[0],
                                                 typ = COMMENT_TYPE.DOCSTRING))
        prev_tok = tok
