# -*- coding: utf-8 -*-
"""
A PyYAML loader that annotates position in source documents.

The loader is based on `SafeConstructor`, i.e.,
the behaviour of `yaml.safe_load`, but in addition:

 - Every dict/list/unicode is replaced with
   DictNode/ListNode/StringNode, which subclasses
   dict/list/unicode to add the attributes
   `start_mark` and `end_mark`. (See the yaml.error
   module for the `Mark` class.)

 - Every string is always returned as unicode, no
   ASCII-ficiation is attempted.

 - Note that int/bool/... are returned unchanged
   for now

This module is modified/adapted from Dag Sverre
Seljebotn's GitHub Gist:
    https://gist.github.com/dagss/5008118

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2012, Dag Sverre Seljebotn and Ondrej Certik"

license:
    "Licensed under the BSD 3-clause license.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are
    met:

        Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.

        Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the
        distribution.

        Neither the name of the copyright holders nor the names of other
        contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    AS IS AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
    A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
    HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
    LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
    DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
    THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
...
"""


from yaml.composer import Composer
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.resolver import Resolver
from yaml.parser import Parser
from yaml.constructor import SafeConstructor

import da.util


# -----------------------------------------------------------------------------
def create_node_class(node_type):
    """
    Return an object of a custom type to represent items of the specified type.

    """
    # Pylint rule R0903 (too-few-public-methods)
    # has been disabled as the  class design is
    # determined by the YAML library architecture,
    # and is not under our control. (It is a POD
    # object rather than a true Class, and has no
    # methods other than its' construction and
    # initialisation functions).
    #
    class NodeClass(node_type):                         # pylint: disable=R0903
        """
        Represent a node in the YAML AST.

        Implements an interface defined by the YAML module.

        """

        def __init__(self, obj, start_mark, end_mark):
            """
            Part of the NodeClass creation sequence defined by the YAML module.

            """
            if node_type in da.util.string_types():
                # str is immutable so we can't change it after __new__
                node_type.__init__(self)
            else:
                node_type.__init__(self, obj)
            self.start_mark = start_mark
            self.end_mark   = end_mark

        # Pylint rule W0613 (unused-argument)
        # disabled as arguments are required
        # to be present to conform with YAML
        # interface.
        #
        def __new__(cls, obj, start_mark, end_mark):    # pylint: disable=W0613
            """
            Part of the NodeClass creation sequence defined by the YAML module.

            """
            return node_type.__new__(cls, obj)

    NodeClass.__name__ = '%s_node' % node_type.__name__
    return NodeClass


DictNode   = create_node_class(dict)
ListNode   = create_node_class(list)
StringNode = create_node_class(str)


# =============================================================================
class NodeConstructor(SafeConstructor):
    """
    Custom YAML NodeConstructor class that supports marking of line numbers.

    """

    # To support lazy loading, the original
    # constructors first yield an empty object,
    # then fill them in when iterated. Due to
    # laziness we omit this behaviour (and will
    # only do "deep construction") by first
    # exhausting iterators, then yielding
    # copies.
    #
    def construct_yaml_map(self, node):
        """
        Return a node class representing a line-marked dictionary.

        """
        obj, = SafeConstructor.construct_yaml_map(self, node)
        return DictNode(obj, node.start_mark, node.end_mark)

    def construct_yaml_seq(self, node):
        """
        Return a node class representing a line-marked sequence.

        """
        obj, = SafeConstructor.construct_yaml_seq(self, node)
        return ListNode(obj, node.start_mark, node.end_mark)

    def construct_yaml_str(self, node):
        """
        Return a node class representing a line-marked string.

        """
        obj = SafeConstructor.construct_scalar(self, node)
        assert da.util.is_string(obj)
        return StringNode(obj, node.start_mark, node.end_mark)


NodeConstructor.add_constructor(
        u'tag:yaml.org,2002:map',
        NodeConstructor.construct_yaml_map)

NodeConstructor.add_constructor(
        u'tag:yaml.org,2002:seq',
        NodeConstructor.construct_yaml_seq)

NodeConstructor.add_constructor(
        u'tag:yaml.org,2002:str',
        NodeConstructor.construct_yaml_str)


# =============================================================================
# Pylint rule R0901 (too-many-ancestors) disabled
# as class design is determined by the YAML library
# architecture, and is not under our control.
#
class Loader(Reader,                                    # pylint: disable=R0901
             Scanner,
             Parser,
             Composer,
             NodeConstructor,
             Resolver):
    """
    Custom YAML Loader class that supports marking of line numbers.

    """

    def __init__(self, stream):
        """
        Return an instance of this customised YAML Loader class.

        """
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        NodeConstructor.__init__(self)
        Resolver.__init__(self)
