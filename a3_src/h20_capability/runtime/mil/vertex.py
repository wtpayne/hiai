# -*- coding: utf-8 -*-
"""
MIL (Model-In-the-Loop) dataflow graph vertex class module.

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


import importlib


# =============================================================================
class Vertex():
    """
    Vertex object.

    """

    # -------------------------------------------------------------------------
    def __init__(self, cfg, module_name):
        """
        Vertex constroctor.

        Allocate and initialise vertex data structures.

        """
        self.module = importlib.import_module(module_name)
        self.allocate(cfg)
        self.reset(cfg)

    # -------------------------------------------------------------------------
    def iter(self):
        """
        Vertex iteration.

        """
        self.pre_step()
        self.step()
        self.post_step()

    # -------------------------------------------------------------------------
    def allocate(self, cfg):
        """
        Allocate memory for vertex data structures.

        """
        (self.inputs, self.state, self.outputs) = self.module.allocate(cfg)

    # -------------------------------------------------------------------------
    def reset(self, cfg):
        """
        Reset or zeroize vertex data structures.

        """
        self.module.reset(cfg, self.inputs, self.state, self.outputs)

    # -------------------------------------------------------------------------
    def pre_step(self):
        """
        Pre-step data transfer operations and integrity checks.

        """
        self.module.pre_step(self.inputs, self.state, self.outputs)

    # -------------------------------------------------------------------------
    def step(self):
        """
        Step the vertex algorithm.

        """
        self.module.step(self.inputs, self.state, self.outputs)

    # -------------------------------------------------------------------------
    def post_step(self):
        """
        Post-step data transfer operations and integrity checks.

        """
        self.module.post_step(self.inputs, self.state, self.outputs)

    # -------------------------------------------------------------------------
    def get_ref(self, path):
        """
        Return the specified reference.

        """
        ref = self.__dict__
        for name in path:
            ref = ref[name]
        return ref
