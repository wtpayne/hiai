# -*- coding: utf-8 -*-
"""
Dataflow graph data source (reader/player/input-adapter) module.

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
import cv2

__all__ = ()


# -----------------------------------------------------------------------------
def allocate(cfg):                                      # pylint: disable=W0613
    """
    Allocate memory and other system resources for vertex data structures.

    """
    inputs = {}
    state = {
        'reader':   None,
        'msg_num':  None
    }
    outputs = {
        'ctrl': {},
        'vid':  {},
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
    inputs_schema = good.Schema({})

    state_schema = good.Schema({
        'reader':   good.Any(),
        'msg_num':  good.Any()
    })

    outputs_schema = good.Schema({
        'ctrl':     good.Any(),
        'vid':      good.Any(),
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
    video_capture = cv2.VideoCapture                    # pylint: disable=E1101
    state['reader']             = video_capture(cfg['filepath'])
    state['msg_num']            = 0

    outputs['ctrl']             = {}
    outputs['vid']['msg_num']   = 0
    outputs['vid']['frame']     = None
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
    isok, frame = state['reader'].read()
    if not isok:
        raise StopIteration
    else:
        state['msg_num']            = state['msg_num'] + 1
        outputs['vid']['msg_num']   = state['msg_num']
        outputs['vid']['frame']     = frame
        outputs['ctrl']['slog_ena'] = bool(state['msg_num'] % 3 == 0)


# -----------------------------------------------------------------------------
def post_step(inputs, state, outputs):
    """
    Execute post-step data transfer operations and data integrity checks.

    """
    validate(inputs, state, outputs)
