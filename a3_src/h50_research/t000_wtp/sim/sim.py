# -*- coding: utf-8 -*-
"""
Development automation user interface experiments.

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


import os

import da.util


# -----------------------------------------------------------------------------
def step(dag):
    """
    Single step the simulation.

    """


# -----------------------------------------------------------------------------
def main():
    """
    Main Simulation.

    """
    print('RUN SIMULATION')
    dirpath_sim  = os.path.dirname(__file__)
    filepath_dag = os.path.join(dirpath_sim, 'default.dag.yaml')
    forward_dag  = da.util.load(filepath_dag)

    # reverse_dag  = collections.defautldict()
    # for (key, val) in forward_dag.items():
    #     for output in val['output']:
    #         for destination in output:


    import pprint
    pprint.pprint(nodes)

    nodes = set(node for node in dag.keys())
    import pprint
    pprint.pprint(nodes)

    for i in range(1):
        step(dag)


