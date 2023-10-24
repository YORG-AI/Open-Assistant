import os
from slack_sdk import WebClient
from typing import Any, Optional
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.slack.slack_model import (
    ConversationJoinInput,
    ConversationLeaveInput,
    ConversationCreateInput,
    ConversationHistoryInput,
    ConversationArchiveInput,
    ConversationKickInput,
    ConversationMarkInput,
    ConversationRenameInput,
    ConversationInfoInput,
    ConversationListInput,
)

from fastapi import HTTPException
from src.utils.router_generator import generate_node_end_points


slack_conversation_config = {
    "name": "slack_conversation",
    "description": "Slack Conversation Node",
    "functions": {
        "join_conversation": "Join a conversation",
        "leave_conversation": "Leave a conversation",
        "create_conversation": "Create a conversation",
        "history_conversation": "Get conversation history",
        "info_conversation": "Get conversation info",
        "archive_conversation": "Archive a conversation",
        "kick_conversation": "Kick a user from a conversation",
        "mark_conversation": "Mark a conversation",
        "rename_conversation": "Rename a conversation",
        "list_conversation": "List all conversations",
    },
}

# channel methods have already been deprecated
# now, using conversation methods
@generate_node_end_points
class SlackConversation(BaseNode):
    config: NodeConfig = NodeConfig(**slack_conversation_config)

    def __init__(self):
        super().__init__()
        user_token = os.getenv("SLACK_USER_TOKEN")
        bot_token = os.getenv("SLACK_BOT_TOKEN")

        self.client = WebClient(token=user_token)  # Instantiate the Slack client

    def join_conversation(self, input: ConversationJoinInput):
        response = self.client.conversations_join(channel=input.channel)
        return response.data

    def leave_conversation(self, input: ConversationLeaveInput):
        response = self.client.conversations_leave(channel=input.channel)
        return response.data

    def create_conversation(self, input: ConversationCreateInput):
        response = self.client.conversations_create(name=input.name)
        return response.data

    def history_conversation(self, input: ConversationHistoryInput):
        response = self.client.conversations_history(channel=input.channel)
        return response.data

    def archive_conversation(self, input: ConversationArchiveInput):
        response = self.client.conversations_archive(channel=input.channel)
        return response.data

    def info_conversation(self, input: ConversationInfoInput):
        response = self.client.conversations_info(channel=input.channel)
        return response.data

    def kick_conversation(self, input: ConversationKickInput):
        response = self.client.conversations_kick(
            channel=input.channel, user=input.user
        )
        return response.data

    def mark_conversation(self, input: ConversationMarkInput):
        response = self.client.conversations_mark(channel=input.channel, ts=input.ts)
        return response.data

    def list_conversation(self, input: ConversationListInput):
        response = self.client.conversations_list()
        return response.data

    def rename_conversation(self, input: ConversationRenameInput):
        response = self.client.conversations_rename(
            channel=input.channel, name=input.name
        )
        return response.data
