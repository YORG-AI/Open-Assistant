import os
from slack_sdk import WebClient
from pydantic import BaseModel
from fastapi import File, UploadFile, Depends, Form
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.slack.slack_model import (
    # FileUploadInput,
    FileDeleteInput,
    FileGetInput,
    FileListInput,
    FileUploadInput,
)
import logging
from src.utils.router_generator import generate_node_end_points

slack_file_config = {
    "name": "slack_file",
    "description": "A node that interacts with Slack's file.",
    "functions": {
        "upload_file": "Upload a file.",
        "delete_file": "Delete a file.",
        "get_file": "Get a file.",
        "list_file": "List all files.",
    },
}


logger = logging.getLogger(__name__)


def get_file_upload_input(
    channel: str = Form(...), file: UploadFile = File(...)
) -> FileUploadInput:
    return FileUploadInput(channel=channel, file=file)


@generate_node_end_points
class SlackFile(BaseNode):
    config: NodeConfig = NodeConfig(**slack_file_config)

    def __init__(self):
        super().__init__()
        user_token = os.getenv("SLACK_USER_TOKEN")
        bot_token = os.getenv("SLACK_BOT_TOKEN")

        self.client = WebClient(token=user_token)  # Instantiate the Slack client

    def upload_file(self, input: FileUploadInput = Depends(get_file_upload_input)):
        try:
            response = self.client.files_upload(
                channel=input.channel,
                file=input.file.file,
                filename=input.file.filename,
                initial_comment="Here's the file I uploaded!",  # You can customize this message as needed
            )
            return response.data
        except Exception as e:
            logger.error("Error uploading file: {}".format(e))
            return {"error": f"Failed to upload file. Reason: {str(e)}"}

    def delete_file(self, input: FileDeleteInput):
        response = self.client.files_delete(file=input.file)
        return response.data

    def get_file(self, input: FileGetInput):
        response = self.client.files_info(file=input.file)
        return response.data

    def list_file(self, input: FileListInput):
        response = self.client.files_list()
        return response.data
