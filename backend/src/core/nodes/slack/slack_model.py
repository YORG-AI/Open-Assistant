from pydantic import BaseModel
from fastapi import UploadFile, File
from pathlib import Path
import os
from typing import Optional, List, Any


# Pydantic models
class MessageInput(BaseModel):
    channel: str
    text: str


class UpdateMessageInput(BaseModel):
    channel: str
    text: str
    ts: str


class ReactionInput(BaseModel):
    channel: str
    name: str
    ts: str


class DeleteMessageInput(BaseModel):
    channel: str
    ts: str


class SearchMessageInput(BaseModel):
    query: str


class GetPermalinkMessageInput(BaseModel):
    channel: str
    message_ts: str


class ConversationJoinInput(BaseModel):
    channel: str


class ConversationLeaveInput(BaseModel):
    channel: str


class ConversationCreateInput(BaseModel):
    name: str


class ConversationHistoryInput(BaseModel):
    channel: str


class ConversationArchiveInput(BaseModel):
    channel: str


class ConversationKickInput(BaseModel):
    channel: str
    user: str


class ConversationListInput(BaseModel):
    pass


class ConversationMarkInput(BaseModel):
    channel: str
    ts: str


class ConversationRenameInput(BaseModel):
    channel: str
    name: str


class ConversationInfoInput(BaseModel):
    channel: str


class FileDeleteInput(BaseModel):
    file: str


class FileUploadInput(BaseModel):
    channel: str
    file: UploadFile


class FileListInput(BaseModel):
    pass


class FileGetInput(BaseModel):
    file: str


class UserInput(BaseModel):
    user: str


class UserListInput(BaseModel):
    pass


class CreateUserGroupInput(BaseModel):
    name: str
    handle: str
    description: str


class UsergroupInput(BaseModel):
    usergroup: str


class UpdateUserGroupInput(BaseModel):
    usergroup: str
    name: str
    handle: str
    description: str


class ListUserGroupInput(BaseModel):
    pass
