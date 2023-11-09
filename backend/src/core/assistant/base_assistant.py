import yaml
from typing import Callable, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

"""
{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1698984975,
  "name": "Math Tutor",
  "description": null,
  "model": "gpt-4",
  "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "file_ids": [],
  "metadata": {}
}
"""

class AssistantInput(BaseModel):
    func_name: str
    func_input: BaseModel


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


class BaseAssistant(ABC):
    config: AssistantConfig
    func_mapping: dict[str, Callable]

    def __init__(self, config: AssistantConfig):
        self.config = config
        import os

        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建 tools.yaml 文件的绝对路径
        tools_yaml_path = os.path.join(current_dir, 'tools.yaml')

        # 使用绝对路径打开 tools.yaml 文件
        with open(tools_yaml_path, 'r') as f:
            tools_yaml = yaml.safe_load(f)
        for tool in self.config.tools:
            if tool['type'] not in tools_yaml['tools']:
                raise ValueError(f"Tool {tool['type']} not found in tools.yaml")

  

  