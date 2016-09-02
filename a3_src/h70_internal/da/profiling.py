# -*- coding: utf-8 -*-
"""
Profiling module.

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

import contextlib
import cProfile
import io
import os
import pstats

import logging


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def context(enable, dirpath_bld_log):
    """
    Context manager to switch profiling on and off.

    """
    if not enable:
        yield
        return

    logging.info('Start profiling')
    profiler = cProfile.Profile()
    profiler.enable()

    try:

        yield

    finally:

        logging.info('End profiling')
        profiler.disable()
        stats_buffer  = io.StringIO()
        profile_stats = pstats.Stats(profiler, stream = stats_buffer)
        profile_stats.sort_stats('cumulative')
        profile_stats.print_stats(20)
        filepath_profile_log = os.path.join(dirpath_bld_log, 'profile.log.txt')

        with open(filepath_profile_log, 'w') as file:
            file.write(stats_buffer.getvalue())
