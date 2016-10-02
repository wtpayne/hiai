# -*- coding: utf-8 -*-
"""
Dataflow graph data sink (output visualisation and recording) module.

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

import cv2
import good

__all__ = ()


# -----------------------------------------------------------------------------
def allocate(cfg):                                      # pylint: disable=W0613
    """
    Allocate memory and other system resources for vertex data structures.

    """
    inputs = {
        'cfg':  {},
        'ctrl': {},
        'ctk':  {},
        'vid':  {},
        'diag': {},
        'slog': {},
        'elog': {}
    }
    state = {}
    outputs = {}

    return (inputs, state, outputs)


# -----------------------------------------------------------------------------
def validate(inputs, state, outputs):
    """
    Validate the data structures for this vertex.

    """
    inputs_schema = good.Schema({
        'cfg':      {'enable_ui': bool},
        'ctrl':     {},
        'ctk':      good.Any(),
        'vid':      good.Any(),
        'diag':     good.Any(),
        'slog':     good.Any(),
        'elog':     good.Any()
    })

    state_schema = good.Schema({})

    outputs_schema = good.Schema({})

    inputs_schema(inputs)
    state_schema(state)
    outputs_schema(outputs)


# -----------------------------------------------------------------------------
def reset(cfg, inputs, state, outputs):                 # pylint: disable=W0613
    """
    Reset vertex data structures back to a known good state.

    """
    inputs['cfg']   = cfg
    inputs['ctrl']  = {}
    inputs['ctk']   = {}
    inputs['vid']   = {}
    inputs['diag']  = {}
    inputs['slog']  = {}
    inputs['elog']  = {}

    state           = {}

    outputs         = {}


# -----------------------------------------------------------------------------
def pre_step(inputs, state, outputs):
    """
    Execute pre-step data transfer operations and data integrity checks.

    """
    validate(inputs, state, outputs)


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):                       # pylint: disable=W0613
    """
    Run a single algorithm step.

    """
    frame = inputs['vid']['frame']
    frame = cv2.resize(                                 # pylint: disable=E1101
                frame, (512, 512), cv2.INTER_LINEAR)    # pylint: disable=E1101

    if inputs['cfg']['enable_ui']:
        cv2.namedWindow("frame", 1)                     # pylint: disable=E1101
        cv2.imshow("frame", frame)                      # pylint: disable=E1101
        cv2.waitKey(1)                                  # pylint: disable=E1101
        import time
        time.sleep(0.01)

    # import ptpython.repl
    # ptpython.repl.embed(globals(), locals())


# -----------------------------------------------------------------------------
def post_step(inputs, state, outputs):
    """
    Execute post-step data transfer operations and data integrity checks.

    """
    validate(inputs, state, outputs)
