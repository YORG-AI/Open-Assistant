import os
from slack_sdk import WebClient
from pydantic import BaseModel
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.slack.slack_model import (
    MessageInput,
    UpdateMessageInput,
    DeleteMessageInput,
    GetPermalinkMessageInput,
    SearchMessageInput,
)
from src.utils.router_generator import generate_node_end_points

slack_message_config = {
    "name": "slack_message",
    "description": "A node that interacts with Slack's message.",
    "functions": {
        "post_message": "Post a message.",
        "update_message": "Update a message.",
        "delete_message": "Delete a message.",
        "getPermalink_message": "Get a permalink to a message.",
        "search_message": "Search for messages matching a query.",
    },
}


@generate_node_end_points
class SlackMessage(BaseNode):
    config: NodeConfig = NodeConfig(**slack_message_config)

    def __init__(self):
        super().__init__()
        user_token = os.getenv("SLACK_USER_TOKEN")
        bot_token = os.getenv("SLACK_BOT_TOKEN")

        self.client = WebClient(token=user_token)  # Instantiate the Slack client

    def post_message(self, input: MessageInput):
        response = self.client.chat_postMessage(channel=input.channel, text=input.text)
        return response.data

    def update_message(self, input: UpdateMessageInput):
        response = self.client.chat_update(
            channel=input.channel, text=input.text, ts=input.ts
        )
        return response.data

    def delete_message(self, input: DeleteMessageInput):
        response = self.client.chat_delete(channel=input.channel, ts=input.ts)
        return response.data

    def getPermalink_message(self, input: GetPermalinkMessageInput):
        response = self.client.chat_getPermalink(
            channel=input.channel, message_ts=input.message_ts
        )
        return response.data

    def search_message(self, input: str):
        response = self.client.search_messages(query=input)
        return response.data
