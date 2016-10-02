# -*- coding: utf-8 -*-
"""
Package containing a data validation schema for the bulk data catalog.

---
type:
    python_package

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


from good import (Any,
                  Extra,
                  Match,
                  Reject,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def get(idclass_schema_tab):
    """
    Return the data validation schema for the codeword register.

    """
    common = da.check.schema.common

    # The quantifier is used to define the
    # relationship between the bounding box
    # and the target entity.
    #
    quantifier = Any(

        # The target object is present everywhere within the ROI.
        #
        # Any declarations falling within the ROI can be considered a true
        # positive. On the other hand, an absence of declarations should only
        # be considered as a missed detection if all detection criteria have
        # been met by the target.
        #
        # Used for probability-of-detection KPI metrics.
        #
        'all'

        # A target object may be present somewhere within the ROI.
        #
        # A declaration falling within the ROI cannot definitively be
        # classified as either a true positive or a false alarm. This
        # quantifier is intended to be used in conjunction with not_exist
        # labels in false alarm rate tests to screen off parts of the data
        # stream that might contain real targets and that should not
        # contribute to false alarm rate metrics.
        #
        'exist',

        # Unless otherwise specified, no target object is present in any part
        # of the ROI.
        #
        # If no other label matches, then a detection in the ROI is
        # definitely a false alarm. Used for false alarm rate tests to
        # identify parts of the data stream that do not contain real targets.
        #
        'not_exist',

    )
    # The bounding_box is used to define a region
    # of interest within the image. In conjunction
    # with the lo/hi byte offsets it may be used
    # to
    bounding_box = Schema({

        # Upper left column (inclusive).
        'ulc':              int,

        # Upper left row (inclusive).
        'ulr':              int,

        # Lower right column (exclusive).
        'lrc':              int,

        # Lower right row (exclusive).
        'lrr':              int,

    })

    line_segment = Schema({

        # Upper left column (inclusive).
        'ulc':              int,

        # Upper left row (inclusive).
        'ulr':              int,

        # Lower right column (exclusive).
        'lrc':              int,

        # Lower right row (exclusive).
        'lrr':              int,

    })

    compact_target_type = Any(Match('generic_target'))

    extended_target_type = Any(Match('generic_horizon'))

    compact_target_label = Schema({

        # Bounding box.
        "box":              bounding_box,

        # Quantifier.
        'qua':              quantifier,

        # Target type.
        'typ':              compact_target_type

    })

    extended_target_label = Schema({

        # Line segment.
        'lin':              line_segment,

        # Quantifier.
        'qua':              quantifier,

        # Target type.
        'typ':              extended_target_type

    })

    return Schema({

        # Label format type.
        'typ':              common.LOWERCASE_NAME,

        # Label format version.
        'ver':              int,

        # Unique identifier (GUID).
        'uid':              common.LOWERCASE_HEX,

        # Trace to requirement.
        'req': [
                            idclass_schema_tab['item']
        ],

        # Trace to team member responsible.
        'rsp': [
                            idclass_schema_tab['team_member']
        ],

        # Start byte (inclusive) of byte range of interest.
        'lo':               common.NUMERIC_STRING,

        # End byte (exclusive) of byte range of interest.
        'hi':               common.NUMERIC_STRING,

        # Function specific label payload.
        'lbl': Any(
                            compact_target_label,
                            extended_target_label
        ),

        Extra:              Reject

    })
