from enum import Enum
from markdown import markdown
from pathlib import Path

import base64

from src.core.agents.data_scientist.data_scientist import DataScientistAgent

from ipykernel.kernelbase import Kernel
from .handler import Handler, HandlerInput
from ipykernel.comm import Comm

import ipywidgets as widgets

import logging


class DataScientistAgentHandler(Handler):
    DS_DATA_FILE_DIR = Path("src/data/ds_data")

    def __init__(self, kernel: Kernel):
        super().__init__(kernel)
        self.agent = DataScientistAgent()
        self.DS_DATA_FILE_DIR.mkdir(parents=True, exist_ok=True)

    def handle(
        self,
        input: HandlerInput,
        silent: bool,
        store_history: bool,
        user_expressions: any,
        allow_stdin: bool,
    ):
        match input.cell_type:
            case "data_analysis":
                upload_file_button = widgets.Button(
                    description="Upload file",
                    disabled=False,
                    button_style="",
                    tooltip="Trigger file upload cell",
                    icon="upload",
                )

                query_button = widgets.Button(
                    description="Query",
                    disabled=False,
                    button_style="",
                    tooltip="Trigger query cell",
                    icon="search",
                )

                def upload_file_button_clicked(b):
                    self._send_comm_obj(
                        "custom_insert_cell", {"type": "ds_upload_file", "code": ""}
                    )

                def query_button_clicked(b):
                    self._send_comm_obj(
                        "custom_insert_cell", {"type": "ds_query", "code": ""}
                    )

                upload_file_button.on_click(upload_file_button_clicked)
                query_button.on_click(query_button_clicked)

                self._send_widget(widgets.HBox([upload_file_button, query_button]))
            case "ds_query":
                # add all files to the agent
                code = self.agent.query(input.code)
                self._send_comm_obj(
                    "custom_insert_cell", {"type": "ds_code", "code": code}
                )
            case "ds_upload_file":
                yorg_upload_files = input.yorg_upload_files
                first_file = True
                for file in yorg_upload_files:
                    if "content" not in file or "name" not in file:
                        continue

                    try:
                        header, encoded = file["content"].split("base64,", 1)
                        data = base64.b64decode(encoded)
                        logging.debug((self.DS_DATA_FILE_DIR / file["name"]).resolve())
                        # Write the decoded data to a file.
                        with open(self.DS_DATA_FILE_DIR / file["name"], "wb") as f:
                            f.write(data)

                        if first_file:
                            self._send_comm_obj(
                                f"custom_set_text",
                                {
                                    "cell_id": input.cell_id,
                                    "operation": "clear",
                                },
                            )
                            first_file = False

                        self._send_comm_obj(
                            f"custom_set_text",
                            {
                                "cell_id": input.cell_id,
                                "operation": "append",
                                "text": f"\"📁 Uploaded {file['name']} to {self.DS_DATA_FILE_DIR.resolve()}\"",
                            },
                        )

                        self.agent.add_data_file(self.DS_DATA_FILE_DIR / file["name"])

                        self._send_markdown(
                            f"""
📊 Data file {file['name']}:

**path**: {(self.DS_DATA_FILE_DIR / file["name"]).resolve()}

**summary**:

{self.agent.get_data_file_summary(file['name'])}

"""
                        )

                    except Exception as e:
                        logging.debug(e)
                        continue

    def do_shutdown(self, restart: bool):
        pass
