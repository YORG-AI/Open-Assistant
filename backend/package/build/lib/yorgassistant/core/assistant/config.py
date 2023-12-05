import uuid
from collections import deque
from typing import List, Optional
from pydantic import BaseModel, Field
import time
import yaml
import os
import re
import logging
import json

class MessageRecord(BaseModel):
    role: str = Field(description="角色")
    content: str = Field(description="内容")

class YamlPathConfig:
    threads_yaml_path = 'threads.yaml'
    assistants_yaml_path = 'assistants.yaml'

class AssistantConfig(BaseModel):
    id: str = Field(description="助手 ID")
    object: str = Field(default="assistant", description="对象类型")
    created_at: int = Field(description="创建时间")
    name: str = Field(description="助手名称")
    description: Optional[str] = Field(default=None, description="助手描述")
    model: str = Field(description="模型")
    instructions: str = Field(description="指令")
    tools: list[dict] = Field(description="工具")
    file_ids: list[str] = Field(default=[], description="文件 ID")
    metadata: dict = Field(default={}, description="元数据")

class ThreadsConfig(BaseModel):
    id: str = Field(description="线程 ID")
    object: str = Field(default="thread", description="对象类型")
    created_at: int = Field(description="创建时间")
    assistant_id: Optional[str] = Field(description="助手 ID")
    message_history: deque[List[MessageRecord]] = Field(
        deque(maxlen=10), description="消息"
    )
    metadata: dict = Field(default={}, description="元数据")

    def to_dict(self):
        # Convert the ThreadsConfig object to a dictionary
        data = self.__dict__.copy()
        # Convert the deque to a list
        data["message_history"] = list(data["message_history"])
        return data

    @classmethod
    def from_dict(cls, data):
        # Convert the list back to a deque
        data["message_history"] = deque(data["message_history"], maxlen=10)
        return cls(**data)