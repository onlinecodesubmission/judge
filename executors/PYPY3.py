import os

from .PYPY import PYTHON_FS
from .python import PythonExecutor
from judgeenv import env

try:
    from cptbox.syscalls import sys_mkdir, sys_unlink
except ImportError:
    pass


class Executor(PythonExecutor):
    command = env['runtime'].get('pypy3')
    test_program = "print(__import__('sys').stdin.read(), end='')"
    name = 'PYPY3'
    fs = PYTHON_FS + ([env['runtime']['pypy3dir']] if 'pypy3dir' in env['runtime'] else [])

    def get_security(self):
        sec = super(Executor, self).get_security()

        def unsafe_pypy3dir(debugger):
            # Relies on the fact this user can't access here.
            return debugger.readstr(debugger.uarg0).startswith(env['runtime']['pypy3dir'])

        if not os.access(env['runtime']['pypy3dir'], os.W_OK):
            sec[sys_mkdir] = unsafe_pypy3dir
            sec[sys_unlink] = unsafe_pypy3dir
        return sec

initialize = Executor.initialize