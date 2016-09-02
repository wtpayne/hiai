# -*- coding: utf-8 -*-
"""
Module containing checks for various design complexity measures.

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


import json
import os.path

import bunch
import radon.raw
import radon.complexity
import radon.metrics

import da.build
import da.log
import da.lwc.file
import da.lwc.search
import da.lwc.discover


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(error_handler):
    """
    Send errors to error_handler if supplied files exceed complexity limits.

    """
    while True:
        build_element = (yield)

        filepath = build_element['filepath']
        if not filepath.endswith('.py'):            # Ignore non-python files.
            continue

        if da.lwc.file.is_test_related(filepath):   # Ignore tests
            continue

        # Gather complexity metrics for each function in the file...
        complexity_log = {}
        module_name    = da.python_source.get_module_name(filepath)
        for function in da.python_source.gen_functions(
                                    module_name = module_name,
                                    source_text = build_element['content'],
                                    root_node   = build_element['ast']):

            (raw, mccabe, halstead, ratios) = _analyse(function)

            # Send metrics to nonconformity decision maker.
            setattr(function, 'da_raw',      raw)
            setattr(function, 'da_mccabe',   mccabe)
            setattr(function, 'da_halstead', halstead)
            setattr(function, 'da_ratios',   ratios)
            setattr(function, 'da_filepath', filepath)
            for nonconformity in _gen_nonconformities(function):
                error_handler.send(nonconformity)

            # Format complexity metrics for logging.
            complexity_log[function.da_addr] = {
                'raw':      raw._asdict(),
                'mccabe':   mccabe._asdict(),
                'halstead': halstead._asdict(),
                'ratios':   ratios.toDict()
            }

        # Write to log file.
        dirpath_log         = build_element['dirpath_log']
        filepath_complexity = os.path.join(dirpath_log, 'complexity.jseq')
        da.util.ensure_dir_exists(dirpath_log)
        with open(filepath_complexity, 'wt') as file_log:
            file_log.write(json.dumps(complexity_log,
                                      sort_keys = True,
                                      indent    = 4))


# -----------------------------------------------------------------------------
def _analyse(function):
    """
    Return complexity analysis for function.

    """
    # Raw metrics.
    raw = radon.raw.analyze(function.da_text)

    # McCabe cyclomatic complexity.
    mccabe_list = radon.complexity.cc_visit_ast(function)
    assert len(mccabe_list) == 1
    mccabe = mccabe_list[0]

    # Halstead maintainability index.
    halstead = radon.metrics.h_visit_ast(function)

    # Ratios
    ratios = bunch.Bunch({
        'lloc_pcl':   float(raw.lloc)          / (float(raw.comments) + 1.0),
        'mccabe_pcl': float(mccabe.complexity) / (float(raw.comments) + 1.0),
        'effort_pcl': float(halstead.effort)   / (float(raw.comments) + 1.0)
    })

    return (raw, mccabe, halstead, ratios)


# -----------------------------------------------------------------------------
def _gen_nonconformities(func):
    """
    Yield radon  nonconformity reports for function.

    Raw metrics:
    ===========
    loc      - Number of lines including comments and whitespace.
    sloc     - Number of lines including comments but not whitespace.
    lloc     - Logical lines (including comments).
    comments - Comment lines
    multi    - lines taken up by multiline strings
    blank    - whitespace-only lines

    McCabe metrics:
    ===============
    name
    lineno
    col_offset
    is_method
    classname
    endline
    closures
    complexity

    Halstead metrics:
    =================
    h1                - Num distinct operators - operator vocabulary.
    h2                - Num distinct operands - operand vocabulary.
    vocabulary        - Operator vocabulary + operand vocabulary.
    N1                - Num operator occurrances - length in operators.
    N2                - Num operand occurrances - length operands.
    length            - Operator occurrances + operand occurrances.
    calculated_length - vocabulary * log(vocabulary).
    volume            - length * log(vocabulary).
    difficulty        - distinct operators * avg. uses of each operand.
    effort            - difficulty * volume.
    time              - scaled effort (seconds).
    bugs              - scaled volume.

    """
    for (err_id, name, metric, limit) in (
            ('r01', 'Logical lines',     func.da_raw.lloc,               60),
            ('r02', 'McCabe complexity', func.da_mccabe.complexity,      18),
            ('r03', 'Halstead vocab.',   func.da_halstead.vocabulary,    50),
            ('r04', 'Halstead length',   func.da_halstead.length,        50),
            ('r05', 'Halstead effort',   func.da_halstead.effort,       800),
            ('r05', 'Halstead time',     func.da_halstead.time,         100),
            ('r06', 'Halstead bugs',     func.da_halstead.bugs,        0.08),
            ('r07', 'lloc/comment',      func.da_ratios.lloc_pcl,      25.0),
            ('r08', 'mmcabe/comment',    func.da_ratios.mccabe_pcl,     7.0),
            ('r09', 'effort/comment',    func.da_ratios.effort_pcl,   300.0)):
        if metric > limit:
            yield {
                'tool':     'radon',
                'msg_id':   err_id,
                'msg':      '{name} {metric} > {limit} in {fcn}'.format(
                                              name   = name,
                                              metric = metric,
                                              limit  = limit,
                                              fcn    = func.da_addr),
                'file':     func.da_filepath,
                'line':     func.lineno
            }
