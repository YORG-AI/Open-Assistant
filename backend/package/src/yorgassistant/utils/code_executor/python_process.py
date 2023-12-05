import subprocess
import queue
import threading
import time

from typing import Optional
from pydantic import BaseModel, Field


class PythonProcess(BaseModel):
    # TODO: check arg legal
    working_dir: str = Field(default="/tmp", description="Working directory.")
    args: list[str] = Field(default=[], description="Arguments for python process.")
    python_exec: str = Field(default="python3", description="Python executable path.")
    python_file_path: str = Field(default="main.py", description="Python file path.")

    def run(self):
        cmd = [self.python_exec] + self.args + [self.python_file_path]
        return subprocess.run(
            [
                "bash -c 'cd {dir} && {real_cmd}'".format(
                    dir=self.working_dir, real_cmd=" ".join(cmd)
                ),
            ],
            shell=True,
            stderr=subprocess.PIPE,
        )

    #     cmd = [self.python_exec] + self.args + [self.python_file_path]

    #     proc = subprocess.Popen(
    #         [
    #             "bash -c 'cd {dir} && {real_cmd}'".format(
    #                 dir=self.working_dir, real_cmd=" ".join(cmd)
    #             ),
    #         ],
    #         shell=True,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #     )

    #     stdout_queue = queue.Queue()
    #     stderr_queue = queue.Queue()

    #     stdout_th = threading.Thread(
    #         target=self._output_reader, args=(1, proc, stdout_queue)
    #     )
    #     stderr_th = threading.Thread(
    #         target=self._output_reader, args=(2, proc, stderr_queue)
    #     )

    #     stdout_th.start()
    #     stderr_th.start()

    #     stdout_buf = ""
    #     stderr_buf = ""

    #     try:
    #         while proc.poll() is None:
    #             try:
    #                 line = stdout_queue.get(block=False)
    #                 print(line, end="")
    #                 stdout_buf += line
    #                 line = stderr_queue.get(block=False)
    #                 print(line, end="")
    #                 stderr_buf += line
    #             except queue.Empty:
    #                 pass
    #             time.sleep(0.002)
    #     finally:
    #         proc.terminate()
    #         try:
    #             proc.wait(timeout=0.5)
    #         except subprocess.TimeoutExpired:
    #             pass

    #     stdout_th.join()
    #     stderr_th.join()

    #     return subprocess.CompletedProcess(
    #         args=proc.args,
    #         returncode=proc.returncode,
    #         stdout=stdout_buf,
    #         stderr=stderr_buf,
    #     )

    # def _output_reader(self, id, proc, out_queue):
    #     if id == 1:
    #         for line in iter(proc.stdout.readline, b""):
    #             out_queue.put(line.decode("utf-8"))
    #     elif id == 2:
    #         for line in iter(proc.stderr.readline, b""):
    #             out_queue.put(line.decode("utf-8"))
