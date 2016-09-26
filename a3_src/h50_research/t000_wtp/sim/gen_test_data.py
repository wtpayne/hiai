# -*- coding: utf-8 -*-
"""
Test data generator.

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

# -----------------------------------------------------------------------------
def init(state):
    """
    Initialise state.

    """
    return {
        'itnum': 0
    }

# -----------------------------------------------------------------------------
def step(cfg, ctrl, input, state):
    """
    Single-step the model.

    """
    itnum = state['itnum']
    result = {
        'cfg':    { 'itnum': itnum },
        'ctrl':   { 'itnum': itnum },
        'ins':    { 'itnum': itnum },
        'svc_01': { 'itnum': itnum },
        'svc_02': { 'itnum': itnum },
        'svc_03': { 'itnum': itnum },
        'svc_04': { 'itnum': itnum },
        'srr_01': { 'itnum': itnum },
        'srr_02': { 'itnum': itnum },
        'srr_03': { 'itnum': itnum },
        'srr_04': { 'itnum': itnum },
    }
    itnum += 1

    # Output
    state['itnum'] = itnum
    event_log      = dict()
    stats_log      = dict()
    diag           = dict()
    return (state, result, event_log, stats_log, diag)


