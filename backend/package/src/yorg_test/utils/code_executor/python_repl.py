import sys

from io import StringIO
from typing import Optional


class PythonREPL:
    """
    Simple python REPL.
    """

    _globals: dict[str, any]
    _locals: dict[str, any]

    def __init__(self, _globals: Optional[dict] = None, _locals: Optional[dict] = None):
        self._globals = _globals if _globals is not None else {}
        self._locals = _locals if _locals is not None else {}

    def run(self, command: str) -> str:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, self._globals, self._locals)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = str(e)
        return output
