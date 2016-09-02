# -*- coding: utf-8 -*-
"""
Miscellaneous utility functions.

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


import collections
import functools
import itertools
import json
import operator
import os


# -----------------------------------------------------------------------------
def coroutine(fun):
    """
    Return a decorator function that primes communications with a coroutine.

    """
    def primed(*args, **kwargs):
        """
        Wrapper for coroutines that 'primes' it by sending the first message.

        """
        coro = fun(*args, **kwargs)
        coro.send(None)
        return coro
    return primed


# -----------------------------------------------------------------------------
def string_types():
    """
    Return the string types for the current Python version.

    """
    is_python_2 = str is bytes
    if is_python_2:
        return (str, unicode)  # pylint: disable=E0602
    else:
        return (str, bytes)


# -----------------------------------------------------------------------------
def is_string(obj):
    """
    Return true if obj is a string. Works in Python 2 and Python 3.

    """
    return isinstance(obj, string_types())


# -----------------------------------------------------------------------------
@coroutine
def index_builder_coro(index = None):
    """
    Return a coroutine that builds an index (map) from supplied tuples.

    The last element in each tuple is treated as the payload value
    that is to be indexed, and the preceeding elements as a hierarchy
    of indices by which it is to be indexed.

    The index itself is a nested default-dictionary with len(tup)
    levels of nesting, containing a list at the innermost level
    to hold the payload.

    >>> builder = index_builder_coro()
    >>> builder.send(None)
    >>> index   = builder.send(('a', 'b', 1))
    >>> index   = builder.send(('a', 'c', 2))
    >>> print(json.dumps(index, sort_keys=True))
    {"a": {"b": [1], "c": [2]}}

    """
    _dedict   = collections.defaultdict
    _repeat   = itertools.repeat
    _reduce   = functools.reduce
    _partial  = functools.partial
    _getitem  = operator.getitem
    tupl      = yield None
    if index is None:
        index = _reduce(lambda ctor, _: _partial(_dedict, ctor),
                        _repeat(None, len(tupl) - 1), list)()
    while True:
        tmp = index
        _reduce(_getitem, tupl[:-1], tmp).append(tupl[-1])
        tupl = yield index


# -----------------------------------------------------------------------------
def build_index(itable_tup):
    """
    Return an index for an iterable container of tuples, all the same length.

    The last element in each tuple is treated as the payload value
    that is to be indexed, and the preceeding elements as a hierarchy
    of indices by which it is to be indexed.

    The index itself is a nested default-dictionary with len(tup)
    levels of nesting, containing a list at the innermost level
    to hold the payload.

    >>> idx = build_index((('a','b', 1), ('a','c', 2)), 3)
    >>> import json
    >>> print(json.dumps(idx, sort_keys=True))
    {"a": {"b": [1], "c": [2]}}

    This function is a bit of an exercise in making use of the
    functional programming capabilities that come with Python,
    so the  implementation is a little more terse and opaque
    than it might otherwise be...

    For each tuple in iter_tup, we construct a slot in the index
    using the lazy initialisation capability that is provided by
    the collections.defaultdict class. All but the last element
    in the tuple are used for indexing. The last element is the
    payload which gets added to the inner list after the structure
    has been initialised. The basic capability is provided by
    the nested defaultdict data structure returned from the idx_ctor
    function, which in turn is built with the aid of the higher
    order lambda function (_partial(_dedict, ctor)).

    All this is plugged together using calls to functools.reduce,
    which is used to construct the custom index data structure; to
    add each tuple to the index, as well as to iterate over the
    input.

    """
    _dedict   = collections.defaultdict
    _chain    = itertools.chain
    _repeat   = itertools.repeat
    _reduce   = functools.reduce
    _partial  = functools.partial
    _getitem  = operator.getitem

    # Peek ahead to determine the tuple length (& reconstitute the iterator).
    iter_tup  = iter(itable_tup)
    try:
        first_tup = iter_tup.__next__()
    except StopIteration:
        return {}
    idx_depth = len(first_tup) - 1
    iter_all  = _chain([first_tup], iter_tup)

    # Create a constructor for a custom index data structure.
    idx_ctor = _reduce(lambda ctor, _: _partial(_dedict, ctor),
                       _repeat(None, idx_depth), list)

    # This function adds a sigle tuple to the custom index data structure.
    def _add_tup_to_idx(idx, tup):
        """
        Add a sigle tuple to the custom index data structure.

        """
        _reduce(_getitem, tup[:-1], idx).append(tup[-1])
        return idx

    # This iterates over all tuples adding each to the index in turn.
    return _reduce(_add_tup_to_idx, iter_all, idx_ctor())


# -----------------------------------------------------------------------------
# TODO: Refactor this so the parameters go in a named tuple and re-enable the
#       pylint warning.
def walkobj(obj,                                  # pylint: disable=R0912,R0913
            gen_leaf    = False,
            gen_nonleaf = False,
            gen_path    = False,
            gen_obj     = False,
            path        = (),
            memo        = None):
    """
    Generate a walk over a treelike structure of mappings and other iterables.

    Adapted from:
    http:/code.activestate.com/recipes/577982-recursively-walk-python-objects/

    This function performs a (depth-first left to right recursive) traversal
    over the provided data structure, which we assume to consist of a finite;
    treelike arrangement of nested collections.Mapping and collections.Iterable
    types.

    This function can be configured to yield information about nodes in the
    tree: leaf nodes; non-leaf (internal) nodes or both.

    The information that is yielded may also be configured: the path to the
    node can be delivered as can the object at the node itself.

    """
    # If the object is elemental, it cannot be decomposed, so we must
    # bottom out the recursion and yield the object and its' path before
    # returning control back up the stack.
    is_itable    = isinstance(obj, collections.Iterable)
    is_leaf      = (not is_itable) or is_string(obj)

    if is_leaf:
        if gen_leaf:
            if gen_path and gen_obj:
                yield (path, obj)
            elif gen_path:
                yield path
            elif gen_obj:
                yield obj
        return

    # Since this is a recursive function, we need to be on our guard against
    # any references to objects back up the call stack (closer to the root of
    # the tree). Any such references would be circular, leading to an infinite
    # tree, and causing us to blow our stack in a fit of unbounded recursion.
    #
    # If we detect that we've already visited this object (using identity not
    # equality), then the safe thing to do is to halt the recursive descent
    # and return control back up the stack.
    _id = id(obj)
    if memo is None:
        memo = set()
    if _id in memo:
        return
    memo.add(_id)

    # If the object is not elemental (i.e. it is an Iterable), then it
    # may be decomposed, so we should recurse down into each component,
    # yielding the results as we go. Of course, we need different iteration
    # functions for mappings vs. other iterables.
    def mapiter(mapping):
        """
        Return an iterator over the specified mapping or other iterable.

        This function selects the appropriate iteration function to use.

        """
        return getattr(mapping, 'iteritems', mapping.items)()
    itfcn = mapiter if isinstance(obj, collections.Mapping) else enumerate

    for pathpart, component in itfcn(obj):

        childpath = path + (pathpart,)
        if gen_nonleaf:
            if gen_path and gen_obj:
                yield (childpath, component)
            elif gen_path:
                yield childpath
            elif gen_obj:
                yield component

        for result in walkobj(obj         = component,
                              gen_leaf    = gen_leaf,
                              gen_nonleaf = gen_nonleaf,
                              gen_path    = gen_path,
                              gen_obj     = gen_obj,
                              path        = childpath,
                              memo        = memo):
            yield result

    # We only need to guard against infinite recursion within a branch of
    # the call-tree. There is no danger in visiting the same item instance
    # in sibling branches, so we can forget about objects once we are done
    # with them and about to pop the stack.
    memo.remove(_id)
    return


# -----------------------------------------------------------------------------
def flatten_ragged(raggedlist, memo = None):
    """
    Flatten a 'ragged' list (a list-of-lists).

    """
    # If the object is elemental, it cannot be decomposed, so we must
    # bottom out the recursion and yield the object and its' path before
    # returning control back up the stack.
    is_itable    = isinstance(raggedlist, collections.Iterable)

    is_leaf      = (not is_itable) or is_string(raggedlist)

    if is_leaf:
        yield raggedlist
        return

    # Since this is a recursive function, we need to be on our guard against
    # any references to objects back up the call stack (closer to the root of
    # the tree). Any such references would be circular, leading to an infinite
    # tree, and causing us to blow our stack in a fit of unbounded recursion.
    #
    # If we detect that we've already visited this object (using identity not
    # equality), then the safe thing to do is to halt the recursive descent
    # and return control back up the stack.
    _id = id(raggedlist)
    if memo is None:
        memo = set()
    if _id in memo:
        return
    memo.add(_id)

    for element in flatten_ragged(raggedlist, memo):
        yield element

    # We only need to guard against infinite recursion within a branch of
    # the call-tree. There is no danger in visiting the same item instance
    # in sibling branches, so we can forget about objects once we are done
    # with them and about to pop the stack.
    memo.remove(_id)
    return


# -----------------------------------------------------------------------------
def decompose_map(srcmap):
    """
    Yield a single entry dict for each key-value pair in the specified mapping.

    """
    for key, value in sorted(srcmap.items()):
        yield {key: value}


# -----------------------------------------------------------------------------
def write_jseq(filepath, iterable):
    """
    Write a sequence of JSON objects to the specified file.

    """
    with open(filepath, 'wt') as file:
        for item in iterable:
            file.write('{line}\n'.format(
                                    line = json.dumps(item, sort_keys = True)))


# -----------------------------------------------------------------------------
def load(filepath):
    """
    Load the specified file with the format determined by the file extension.

    """
    # The yaml module is not part of the standard library. It is part of
    # the configuration controlled runtime environment in a0_env. We import
    # it in function scope becausse the util module is imported before a0_env
    # is enabled in the bootstrap process.
    import yaml

    if filepath.endswith('.yaml'):
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)

    if filepath.endswith('.json'):
        with open(filepath, 'r') as file:
            return json.load(file)

    else:
        raise RuntimeError('File format not supported: %s', filepath)


# -----------------------------------------------------------------------------
def ensure_dir_exists(path):
    """
    Ensure that a specified directory exists, creating it if necessary.

    """
    try:
        os.makedirs(path)
    except OSError:
        if not os.path.isdir(path):
            raise


# -----------------------------------------------------------------------------
def ensure_file_exists(filepath):
    """
    Ensure that a specified file exists, creating it if necessary.

    """
    dirpath = os.path.dirname(filepath)
    ensure_dir_exists(dirpath)
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as _:
            pass


# -----------------------------------------------------------------------------
def merge_dicts(first, second):
    """
    Merge two dictionaries. second takes priority.

    """
    return dict(_merge_dicts(first, second))


# -----------------------------------------------------------------------------
def _merge_dicts(first, second):
    """
    Merge two dictionaries (recursive function). second takes priority.

    """
    for key in set(first.keys()).union(second.keys()):
        _in_first  = key in first
        _in_second = key in second
        if _in_first and _in_second:
            _isdict_first  = isinstance(first[key], dict)
            _isdict_second = isinstance(second[key], dict)
            if _isdict_first and _isdict_second:
                yield (key, dict(_merge_dicts(first[key], second[key])))
            else:
                # second overwrites first if both are present.
                yield(key, second[key])
        elif _in_first:
            yield (key, first[key])
        else:
            yield (key, second[key])


# -----------------------------------------------------------------------------
def iter_yaml_docs(text):
    """
    Yield text sections corresponding to YAML documents in the specified text.

    """
    iter_lines = iter(text.splitlines())
    is_inside  = False
    doc_lines  = []

    for line in iter_lines:

        # State transition: outside to inside
        if line.strip() == '---':
            is_inside = True
            continue

        # State transition: inside to outside
        elif line.strip() == '...':
            if doc_lines:
                yield '\n'.join(doc_lines)
                doc_lines = []
            is_inside = False
            continue

        # state is inside -> accumulate lines
        # state is outside -> do nothing
        if is_inside:
            doc_lines.append(line)
        else:
            continue

    # At the end, if we have anything to return, yield it.
    if doc_lines:
        yield '\n'.join(doc_lines)


# -----------------------------------------------------------------------------
def iter_dirs(dirpath_root):
    """
    Yield directory names & paths found immediately under dirpath_root.

    """
    for name in os.listdir(dirpath_root):
        path = os.path.join(dirpath_root, name)
        if not os.path.isdir(path):
            continue
        yield (name, path)


# -----------------------------------------------------------------------------
def iter_files(dirpath_root):
    """
    Yield file names & paths found immediately under dirpath_root.

    """
    for name in os.listdir(dirpath_root):
        path = os.path.join(dirpath_root, name)
        if not os.path.isfile(path):
            continue
        yield (name, path)
