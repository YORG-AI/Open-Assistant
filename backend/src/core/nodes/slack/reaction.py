import os
from slack_sdk import WebClient
from pydantic import BaseModel
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.slack.slack_model import ReactionInput
from src.utils.router_generator import generate_node_end_points

slack_reaction_config = {
    "name": "slack_reaction",
    "description": "A node that interacts with Slack's reaction.",
    "functions": {
        "add_reaction": "Add reaction to a message.",
        "get_reaction": "Get reaction to a message.",
        "remove_reaction": "Remove reaction to a message.",
    },
}


@generate_node_end_points
class SlackReaction(BaseNode):
    config: NodeConfig = NodeConfig(**slack_reaction_config)

    def __init__(self):
        super().__init__()
        user_token = os.getenv("SLACK_USER_TOKEN")
        bot_token = os.getenv("SLACK_BOT_TOKEN")

        self.client = WebClient(token=user_token)  # Instantiate the Slack client

    def add_reaction(self, input: ReactionInput):
        response = self.client.reactions_add(
            channel=input.channel, name=input.name, timestamp=input.ts
        )
        return response.data

    def get_reaction(self, input: ReactionInput):
        response = self.client.reactions_get(channel=input.channel, timestamp=input.ts)
        return response.data

    def remove_reaction(self, input: ReactionInput):
        response = self.client.reactions_remove(
            channel=input.channel, name=input.name, timestamp=input.ts
        )
        return response.data
