# -*- coding: utf-8 -*-
"""
Long term target tracking.

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

import good

__all__ = ()


# -----------------------------------------------------------------------------
def allocate(cfg):                                      # pylint: disable=W0613
    """
    Allocate memory and other system resources for vertex data structures.

    """
    inputs = {
        'ctrl': {},
        'stt':  {}
    }
    state = {}
    outputs = {
        'ltt':  {},
        'diag': {},
        'slog': {},
        'elog': {}
    }
    return (inputs, state, outputs)


# -----------------------------------------------------------------------------
def validate(inputs, state, outputs):
    """
    Validate the data structures for this vertex.

    """
    inputs_schema = good.Schema({
        'ctrl':     good.Any(),
        'stt':      good.Any()
    })

    state_schema = good.Schema({})

    outputs_schema = good.Schema({
        'ltt':      good.Any(),
        'diag':     good.Any(),
        'slog':     good.Any(),
        'elog':     good.Any()
    })

    inputs_schema(inputs)
    state_schema(state)
    outputs_schema(outputs)


# -----------------------------------------------------------------------------
def reset(cfg, inputs, state, outputs):                 # pylint: disable=W0613
    """
    Reset vertex data structures back to a known good state.

    """
    inputs['ctrl']              = {}
    inputs['stt']['msg_num']    = 0

    state = {}

    outputs['ltt']['msg_num']   = 0
    outputs['diag']             = {}
    outputs['slog']             = {}
    outputs['elog']             = {}


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
    outputs['ltt']['msg_num'] = inputs['stt']['msg_num']


# -----------------------------------------------------------------------------
def post_step(inputs, state, outputs):
    """
    Execute post-step data transfer operations and data integrity checks.

    """
    validate(inputs, state, outputs)
