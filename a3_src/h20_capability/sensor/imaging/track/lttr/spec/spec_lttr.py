# -*- coding: utf-8 -*-
"""
Unit tests for the sensor.imaging.track.lttr module.

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
class SpecifyAllocate:
    """
    specify the sensor.imaging.track.lttr.allocate() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        the allocate() function is callable.

        """
        import sensor.imaging.track.lttr
        assert callable(sensor.imaging.track.lttr.allocate)


# =============================================================================
class SpecifyValidate:
    """
    Specify the sensor.imaging.track.lttr.validate() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The validate() function is callable.

        """
        import sensor.imaging.track.lttr
        assert callable(sensor.imaging.track.lttr.validate)


# =============================================================================
class SpecifyReset:
    """
    Specify the sensor.imaging.track.lttr.reset() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The reset() function is callable.

        """
        import sensor.imaging.track.lttr
        assert callable(sensor.imaging.track.lttr.reset)


# =============================================================================
class SpecifyPreStep:
    """
    Specify the sensor.imaging.track.lttr.pre_step() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The pre_step() function is callable.

        """
        import sensor.imaging.track.lttr
        assert callable(sensor.imaging.track.lttr.pre_step)


# =============================================================================
class SpecifyStep:
    """
    Specify the sensor.imaging.track.lttr.step() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The step() function is callable.

        """
        import sensor.imaging.track.lttr
        assert callable(sensor.imaging.track.lttr.step)


# =============================================================================
class SpecifyPostStep:
    """
    Specify the sensor.imaging.track.lttr.post_step() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The post_step() function is callable.

        """
        import sensor.imaging.track.lttr
        assert callable(sensor.imaging.track.lttr.post_step)
