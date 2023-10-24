from pydantic import BaseModel
from markdown import markdown

from ipykernel.ipkernel import IPythonKernel
from ipykernel.comm import Comm
from dotenv import load_dotenv

import ipywidgets as widgets

from .handler import Handler, HandlerInput
from .gpt_handler import GPTHandler
from .swe_agent_handler import SoftwareEngineerAgentHandler
from .ds_agent_handler import DataScientistAgentHandler
from .file_upload_handler import FileUploadHandler
from .display_handler import DisplayHandler


import json
import logging


load_dotenv()

logging.basicConfig(filename="ykernel.log", level=logging.DEBUG)


class YKernel(IPythonKernel):
    implementation = "Y Kernel"
    implementation_version = "1.0"
    language = "no-op"
    language_version = "0.1"
    language_info = {
        "name": "python",
        "mimetype": "text/x-python",
        "file_extension": ".py",
    }
    banner = "Y Kernel - as useful as a parrot"

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(YKernel, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ds_handler = DataScientistAgentHandler(self)

        self.handlers: dict[str, Handler] = {
            "gpt": GPTHandler(self),
            "software_engineer": SoftwareEngineerAgentHandler(self),
            "data_analysis": self.ds_handler,
            "ds_query": self.ds_handler,
            "ds_upload_file": self.ds_handler,
            "display": DisplayHandler(self),
        }

        self.outputs: dict[str, list] = {}  # cell_id -> output[text]
        self._register_comm_handler()

    async def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        try:
            info = json.loads(code)
        except Exception as e:
            # If the code is not JSON, execute it as Python code
            resp = await self._default_handler(
                code,
                silent,
                store_history,
                user_expressions,
                allow_stdin,
            )

            self._after_execute()

            return resp

        input = HandlerInput(
            cell_type=info["type"],
            code=info["code"],
            cell_id=info["cell_id"],
            yorg_upload_files=info["yorg_upload_files"]
            if "yorg_upload_files" in info
            else [],
        )

        logging.info(f"before execute {input.cell_type}")
        logging.info(self.outputs)

        if input.cell_type == "auto_refresh":
            # if it's auto refresh cell, just trigger the get output comm
            self._send_comm_obj("custom_get_output", {})
            return {
                "status": "ok",
                "execution_count": self.shell.execution_count,
                "payload": [],
                "user_expressions": {},
            }

        resp = {}

        if input.cell_type in self.handlers:
            # if the cell type is handled by a handler, use the handler to handle it
            self.handlers[info["type"]].handle(
                input,
                silent,
                store_history,
                user_expressions,
                allow_stdin,
            )

            return_count = self.shell.execution_count
            self.shell.execution_count += 1
            resp = {
                "status": "ok",
                "execution_count": return_count,
                "payload": [],
                "user_expressions": {},
            }

        elif input.cell_type == "python" or input.cell_type == "ds_code":
            # if need to run python code, execute it use super class (ipykernel) method
            resp = await self._default_handler(
                input.code,
                silent,
                store_history,
                user_expressions,
                allow_stdin,
            )
        else:
            logging.warning(f"Unknown cell type: {input.cell_type}")
            resp = {
                "status": "ok",
                "execution_count": self.shell.execution_count,
                "payload": [],
                "user_expressions": {},
            }
        
        self._after_execute()
        return resp
        

        

    def do_shutdown(self, restart):
        for handler in self.handlers.values():
            handler.do_shutdown(restart)

        super().do_shutdown(restart)

    async def _default_handler(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):
        result = await super().do_execute(
            code,
            silent,
            store_history,
            user_expressions,
            allow_stdin,
        )

        return result




    def _register_comm_handler(self):
        def handle_cell_output(comm, msg):
            cell_id = msg["content"]["data"]["cell_id"]
            outputs = msg["content"]["data"]["outputs"]

            cell_output = []
            for output in outputs:
                if output.get("name") == "stdout":
                    cell_output.append(output["text"])

            self.outputs[cell_id] = cell_output

        def handle_all_cell_output(comm, msg):
            all_cell_outputs = msg["content"]["data"]
            for single_cell_output in all_cell_outputs:
                cell_id = single_cell_output["cell_id"]
                outputs = single_cell_output["outputs"]
                self.outputs[cell_id] = outputs
            
            output_str = json.dumps(self.outputs, indent=4)
            logging.debug(f"all_cell_output: {output_str}")

        self.comm_manager.register_target("custom_cell_output", handle_cell_output)
        self.comm_manager.register_target(
            "custom_all_cell_output", handle_all_cell_output
        )

    def _after_execute(self):
        self._send_comm_obj("custom_insert_cell", {"type": "auto_refresh", "code": ""})

        logging.debug(f"after_execute: {self.outputs}")

    def _before_execute(self):
        self._send_comm_obj("custom_get_output", {})

        logging.debug(f"before_execute: {self.outputs}")

    def _send_comm_obj(self, target_name: str, data: any):
        """
        Send comm message (must be able to be converted to JSON format) to frontend.
        """
        comm = Comm(target_name=target_name, data=data, show_warning=False)
        comm.send()
        comm.close()

    def _send_comm_model(self, target_name: str, data: BaseModel):
        """
        Send object message to frontend.
        """
        comm = Comm(target_name=target_name, data=data.json(exclude_none=True), show_warning=False)
        comm.send()
        comm.close()

    def _send_widget(self, widget: widgets.Widget):
        """
        Send widget to frontend.
        """
        self.send_response(
            self.iopub_socket,
            "display_data",
            {
                "data": {
                    "application/vnd.jupyter.widget-view+json": widget.get_view_spec()
                },
                "metadata": {},
            },
        )

    def _send_markdown(self, content: str):
        """
        Send markdown (html) content to frontend.
        """
        html_content = markdown(
            content,
            extensions=["fenced_code", "codehilite"],
            extension_configs={
                "codehilite": {
                    "use_pygments": True,
                    "css_class": "highlight",
                    "pygments_style": "solarized-light",
                    "guess_lang": False,
                }
            },
        )

        self.send_response(
            self.iopub_socket,
            "display_data",
            {"data": {"text/html": html_content}},
        )


if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=YKernel)
