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
        # 初始化 func_mapping
        self.func_mapping = {}
        avail_funcs = [
            func_name for func_name in dir(self) if not func_name.startswith("_")
        ]
        # 读取 YAML 文件
        with open('tools.yaml', 'r') as file:
            tools_dict = yaml.safe_load(file)
        available_tools = list(tools_dict['tools'].keys())  # 获取 tools 部分的内容
        for tool in self.config.tools:
            func_name = tool["type"]
            if func_name not in available_tools or func_name not in avail_funcs:
                raise ValueError(f'Tool {func_name} not defined in YAML file.')
            elif func_name in avail_funcs:
                self.func_mapping[func_name] = getattr(self, func_name)

    def run(self, input: AssistantInput):
        if input.func_name not in self.func_mapping.keys():
            raise Exception(
                f"Assistant {self.config.name} does not contain {input.func_name} method."
            )
        else:
            return self.func_mapping[input.func_name](input.func_input)