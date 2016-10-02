# -*- coding: utf-8 -*-
"""
Unit tests for the runtime.mil module.

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


# =============================================================================
class SpecifyVertexIter:
    """
    Specify the runtime.mil.vertex.Vertex.iter() method.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The Vertex.iter() method is callable.

        """
        import runtime.mil.vertex
        assert callable(runtime.mil.vertex.Vertex.iter)


# =============================================================================
class SpecifyVertexAllocate:
    """
    Specify the runtime.mil.vertex.Vertex.allocate() method.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The Vertex.allocate() method is callable.

        """
        import runtime.mil.vertex
        assert callable(runtime.mil.vertex.Vertex.allocate)


# =============================================================================
class SpecifyVertexReset:
    """
    Specify the runtime.mil.vertex.Vertex.reset() method.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The Vertex.reset() method is callable.

        """
        import runtime.mil.vertex
        assert callable(runtime.mil.vertex.Vertex.reset)


# =============================================================================
class SpecifyVertexPreStep:
    """
    Specify the runtime.mil.vertex.Vertex.pre_step() method.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The Vertex.pre_step() method is callable.

        """
        import runtime.mil.vertex
        assert callable(runtime.mil.vertex.Vertex.pre_step)

# =============================================================================
class SpecifyVertexStep:
    """
    Specify the runtime.mil.vertex.Vertex.step() method.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The Vertex.step() method is callable.

        """
        import runtime.mil.vertex
        assert callable(runtime.mil.vertex.Vertex.step)


# =============================================================================
class SpecifyVertexPostStep:
    """
    Specify the runtime.mil.vertex.Vertex.post_step() method.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The Vertex.post_step() method is callable.

        """
        import runtime.mil.vertex
        assert callable(runtime.mil.vertex.Vertex.post_step)


# =============================================================================
class SpecifyVertexGetRef:
    """
    Specify the runtime.mil.vertex.Vertex.get_ref() method.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The Vertex.get_ref() method is callable.

        """
        import runtime.mil.vertex
        assert callable(runtime.mil.vertex.Vertex.get_ref)

