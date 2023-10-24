import base64
from markdown import markdown

from ipykernel.kernelbase import Kernel
from ipykernel.comm import Comm

from .handler import Handler, HandlerInput
from pathlib import Path
import logging

FILE_DIR = Path("./file_dir")


class FileUploadHandler(Handler):
    def __init__(self, kernel: Kernel):
        super().__init__(kernel)

    def handle(
        self,
        input: HandlerInput,
        silent: bool,
        store_history: bool,
        user_expressions: any,
        allow_stdin: bool,
    ):
        yorg_upload_files = input.yorg_upload_files
        # print(yorg_upload_files)
        FILE_DIR.mkdir(parents=True, exist_ok=True)

        first_file = True

        for file in yorg_upload_files:
            if "content" not in file or "name" not in file:
                continue

            try:
                header, encoded = file["content"].split("base64,", 1)
                data = base64.b64decode(encoded)
                logging.debug((FILE_DIR / file["name"]).resolve())
                # print(decoded_data)
                # Get the MIME type of the file.
                # mime_type = mimetypes.guess_type(decoded_data)[0]

                # Write the decoded data to a file.
                with open(FILE_DIR / file["name"], "wb") as f:
                    f.write(data)

                if first_file:
                    self._send_comm_obj(
                        f"custom_set_text",
                        {
                            "cell_id": input.cell_id,
                            "operation": "set",
                            "text": "",
                        },
                    )
                    first_file = False

                self._send_comm_obj(
                    f"custom_set_text",
                    {
                        "cell_id": input.cell_id,
                        "operation": "append",
                        "text": f"\"📁 Uploaded {file['name']} to {FILE_DIR.resolve()}\"",
                    },
                )
            except Exception as e:
                logging.debug(e)
                continue

    def do_shutdown(self, restart: bool):
        pass
