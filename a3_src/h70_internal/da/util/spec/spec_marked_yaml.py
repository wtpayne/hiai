# -*- coding: utf-8 -*-
"""
Unit tests for the marked_yaml module.

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


import inspect


# =============================================================================
class SpecifyCreateNodeClass:
    """
    Specify the da.util.marked_yaml.create_node_class() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_class(self):
        """
        It returns a Class object.

        """
        import da.util.marked_yaml
        DictNode = da.util.marked_yaml.create_node_class(dict)
        assert inspect.isclass(DictNode)


# =============================================================================
class SpecifyNodeConstructorConstructYamlMap:
    """
    Specify the NodeConstructor.construct_yaml_map() method.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_class(self):
        """
        It returns a DictNode object.

        """
        import yaml
        import da.util.marked_yaml
        node_ctor = da.util.marked_yaml.NodeConstructor()
        node      = yaml.nodes.MappingNode(tag   = 'tag',
                                           value = ())
        assert isinstance(node_ctor.construct_yaml_map(node),
                          da.util.marked_yaml.DictNode)


# =============================================================================
class SpecifyNodeConstructorConstructYamlSeq:
    """
    Specify the NodeConstructor.construct_yaml_seq() method.

    """

# =============================================================================
class SpecifyNodeConstructorConstructYamlStr:
    """
    Specify the NodeConstructor.construct_yaml_str() method.

    """
