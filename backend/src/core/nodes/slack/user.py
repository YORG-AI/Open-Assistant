import os
from slack_sdk import WebClient
from typing import Any, Optional
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.slack.slack_model import UserInput, UserListInput
from src.utils.router_generator import generate_node_end_points

slack_user_config = {
    "name": "Slack User",
    "description": "A node that interacts with Slack's user.",
    "functions": {
        "info_users": "Get information about a user.",
        # "list_users": "List all users.",
    },
}


@generate_node_end_points
class SlackUser(BaseNode):
    config: NodeConfig = NodeConfig(**slack_user_config)

    def __init__(self):
        super().__init__()
        user_token = os.getenv("SLACK_USER_TOKEN")
        bot_token = os.getenv("SLACK_BOT_TOKEN")

        self.client = WebClient(token=user_token)  # Instantiate the Slack client

    def info_users(self, input: UserInput):
        response = self.client.users_info(user=input.user)
        return response.data

    def list_users(self, input: UserListInput):
        response = self.client.users_list()
        return response.data
