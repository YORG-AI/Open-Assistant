from typing import Callable
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class NodeInput(BaseModel):
    func_name: str
    func_input: BaseModel


class NodeConfig(BaseModel):
    name: str = Field(description="Node 名称")
    description: str = Field(default="", description="Node 描述")
    functions: dict[str, str] = Field(default={}, description="Node 所有功能描述")


class BaseNode(ABC):
    config: NodeConfig
    func_mapping: dict[str, Callable]

    def __init__(self):
        # initialize func_mapping
        self.func_mapping = {}
        avail_funcs = [
            func_name for func_name in dir(self) if not func_name.startswith("_")
        ]
        for func_name in self.config.functions.keys():
            if func_name not in avail_funcs:
                raise Exception(
                    f"Node {self.config.name} does not contain {func_name} method."
                )
            else:
                self.func_mapping[func_name] = getattr(self, func_name)

    def run(self, input: NodeInput):
        if input.func_name not in self.func_mapping.keys():
            raise Exception(
                f"Node {self.config.name} does not contain {input.func_name} method."
            )
        else:
            return self.func_mapping[input.func_name](input.func_input)
