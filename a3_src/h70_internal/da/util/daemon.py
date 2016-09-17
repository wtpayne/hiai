# -*- coding: utf-8 -*-
"""
Module containing daemonisation code.

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


import atexit
import os
import signal
import sys
import time


# =============================================================================
class BaseDaemon:
    """
    A generic daemon class.

    Usage: subclass the daemon class and override the run() method.

    """

    # -------------------------------------------------------------------------
    def __init__(self, pidfile):
        """
        Ctor.

        """
        self.pidfile = pidfile

    # -------------------------------------------------------------------------
    def daemonize(self):
        """
        Deamonize class. UNIX double fork mechanism.

        """
        try:

            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)

        except OSError as err:

            sys.stderr.write('fork #1 failed: {0}\n'.format(err))
            sys.exit(1)

        # decouple from parent environment
        os.chdir('/')
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:

                # exit from second parent
                sys.exit(0)
        except OSError as err:
            sys.stderr.write('fork #2 failed: {0}\n'.format(err))
            sys.exit(1)

        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        null_stdin  = open(os.devnull, 'r')
        null_stdout = open(os.devnull, 'a+')
        null_stderr = open(os.devnull, 'a+')

        os.dup2(null_stdin.fileno(), sys.stdin.fileno())
        os.dup2(null_stdout.fileno(), sys.stdout.fileno())
        os.dup2(null_stderr.fileno(), sys.stderr.fileno())

        # write pidfile
        atexit.register(self.delpid)

        pid = str(os.getpid())
        with open(self.pidfile, 'w+') as file:
            file.write(pid + '\n')

    # -------------------------------------------------------------------------
    def delpid(self):
        """
        Delete pid.

        """
        os.remove(self.pidfile)

    # -------------------------------------------------------------------------
    def start(self):
        """
        Start the daemon.

        """
        # Check for a pidfile to see if the daemon already runs
        try:
            with open(self.pidfile, 'r') as pfile:

                pid = int(pfile.read().strip())
        except IOError:
            pid = None

        if pid:
            message = "pidfile {0} already exist. " + \
                    "Daemon already running?\n"
            sys.stderr.write(message.format(self.pidfile))
            sys.exit(1)

        # Start the daemon
        self.daemonize()
        self.run()

    # -------------------------------------------------------------------------
    def stop(self):
        """
        Stop the daemon.

        """
        # Get the pid from the pidfile
        try:
            with open(self.pidfile, 'r') as pfile:
                pid = int(pfile.read().strip())
        except IOError:
            pid = None

        if not pid:
            message = "pidfile {0} does not exist. " + \
                    "Daemon not running?\n"
            sys.stderr.write(message.format(self.pidfile))
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            str_err = str(err.args)
            if str_err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print(str(err.args))
                sys.exit(1)

    # -------------------------------------------------------------------------
    def restart(self):
        """
        Restart the daemon.

        """
        self.stop()
        self.start()

    # -------------------------------------------------------------------------
    def run(self):
        """
        You should override this method when you subclass Daemon.

        It will be called after the process has been daemonized by
        start() or restart().

        """
        raise NotImplementedError(
                        'The run method should be overridden by the subclass')
