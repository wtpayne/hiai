# -*- coding: utf-8 -*-
"""
Exception classes for da systems.

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
class ImplementationNotPresentError(RuntimeError):
    """
    Exception to be raised when a feature is not yet implemented.

    We allow features to be introduced incrementally
    to production software, disabled or enabled by
    suitable runtime configuration.

    This exception serves both as a searchable
    indicator of unfinished work and also as an
    indicator of configuration errors during
    testing.

    The Python built-in exception NotImplementedError
    is not suitable as it is intended for a different
    use-case. Its' documentation explicitly states
    that it is intended to be used (only?) for abstract
    methods in a base class that need to be overridden.

    """

    pass


# =============================================================================
class AbortSilently(Exception):
    """
    Exception to be raised when the display of a message is undesirable.

    This exception is raised when we have already displayed an error
    message and just need the program to abort.

    """

    pass


# =============================================================================
class AbortWithoutStackTrace(Exception):
    """
    Exception to be raised when the display of a stack trace is undesirable.

    Raising this exception will not result in a
    stack trace in the CLI, so it should not be
    used to indicate errors in running components
    of the build system, but should instead be
    used to indicate incorrect or invalid input
    being provided to the build. E.g. bad parameters,
    bad configuration files or other build input
    file errors.

    ---
    type: class
    attributes:
        message:
            Human readable string describing the
            reason for the abort.
        filepath:
            If specified, this is a string holding
            the fully qualified path to the file
            within which a fault was found.
            Otherwise None.
        line_number:
            If specified, this is an integer
            indicating the line number in
            filepath where a fault was found.
            Otherwise None.
    ...
    """

    def __init__(self, message, filepath = None, line_number = None):
        """
        Return a new instance of the AbortWithoutStackTrace Exception class.

        ---
        type: constructor
        args:
            message:
                Human readable string describing
                the reason for the abort.
            filepath:
                If specified, this is a string
                holding the fully qualified path
                to the file within which a fault
                was found. Otherwise None.
            line_number:
                If specified, this is an integer
                indicating the line number in
                filepath where a fault was found.
                Otherwise None.
        ...

        """
        # We need to be careful to call the base
        # class with the parameters that it needs
        # - as we will have difficulty unpickling
        # it otherwise.
        #
        super(AbortWithoutStackTrace, self).__init__(message)
        self.message     = message
        self.filepath    = filepath
        self.line_number = line_number
