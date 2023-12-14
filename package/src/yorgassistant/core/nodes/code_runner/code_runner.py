import ast

from typing import Optional

from ...nodes.base_node import BaseNode, NodeConfig
from ...nodes.code_runner.code_runner_model import (
    RunCodeInput,
    RunCodeFromFileInput,
)
from ....utils.code_executor.python_process import PythonProcess
from ....utils.code_executor.python_repl import PythonREPL

code_runner_config = {
    "name": "code_runner",
    "description": "A simple node that run python code.",
    "functions": {
        "run_code": "Run python code in string format.",
        "run_code_from_file": "Run python code in specific files.",
    },
}


class CodeRunnerNode(BaseNode):
    config: NodeConfig = NodeConfig(**code_runner_config)

    pythonREPL: PythonREPL

    def __init__(self):
        super().__init__()
        self.pythonREPL = None

    # TODO: check if the input is valid

    def run_code(self, input: RunCodeInput):
        if self.pythonREPL is None:
            self.init_python_repl()
        return self.pythonREPL.run(input.code)

    def run_code_from_file(self, input: RunCodeFromFileInput):
        working_dir = input.working_dir
        if ' ' in input.working_dir:
            working_dir = f'"{input.working_dir}"'

        file_path = input.file_path
        if ' ' in input.file_path:
            file_path = f'"{input.file_path}"'

        proc = PythonProcess(
            working_dir=working_dir,
            python_file_path=file_path,
        )
        return proc.run()

    def init_python_repl(
        self, globals_: Optional[dict] = None, locals_: Optional[dict] = None
    ):
        self.pythonREPL = PythonREPL(globals_, locals_)
