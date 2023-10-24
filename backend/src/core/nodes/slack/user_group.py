import os
from typing import Any, Optional
from slack_sdk import WebClient
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.slack.slack_model import (
    CreateUserGroupInput,
    UsergroupInput,
    UpdateUserGroupInput,
    ListUserGroupInput,
)
from src.utils.router_generator import generate_node_end_points

slack_user_group_config = {
    "name": "Slack User Group",
    "description": "A node that interacts with Slack's user group.",
    "functions": {
        "create_usergroup": "Create a user group.",
        "disable_usergroup": "Disable a user group.",
        "enable_usergroup": "Enable a user group.",
        "list_usergroup": "List all user groups.",
        "update_usergroup": "Update a user group.",
    },
}


""" This function is only available for paid workspace """


@generate_node_end_points
class SlackUserGroup(BaseNode):
    config: NodeConfig = NodeConfig(**slack_user_group_config)

    def __init__(self):
        super().__init__()
        user_token = os.getenv("SLACK_USER_TOKEN")
        bot_token = os.getenv("SLACK_BOT_TOKEN")

        self.client = WebClient(token=user_token)  # Instantiate the Slack client

    def create_usergroup(self, input: CreateUserGroupInput):
        response = self.client.usergroups_create(
            name=input.name, handle=input.handle, description=input.description
        )
        return response.data

    def disable_usergroup(self, input: UsergroupInput):
        response = self.client.usergroups_disable(usergroup=input.usergroup)
        return response.data

    def enable_usergroup(self, input: UsergroupInput):
        response = self.client.usergroups_enable(usergroup=input.usergroup)
        return response.data

    def list_usergroup(self, input: ListUserGroupInput):
        response = self.client.usergroups_list()
        return response.data

    def update_usergroup(self, input: UpdateUserGroupInput):
        response = self.client.usergroups_update(
            usergroup=input.usergroup,
            name=input.name,
            handle=input.handle,
            description=input.description,
        )
        return response.data
