import yaml
import os
import inspect
from pydantic import BaseModel, Field

from .tool_entity import (
    BaseToolEntity,
    FunctionToolEntity,
    State
)
from .model import Parameter, Response

from .swe_tool_entity import SWEToolEntity
from .da_tool_entity import DAToolEntity
from .example_stateful_tool_entity import ExampleStatefulToolEntity


# 示例工具函数
def serve_code_interpreter(code: str) -> dict[str, any]:
    from src.core.nodes.code_runner.code_runner import CodeRunnerNode, RunCodeInput

    code_runner_node = CodeRunnerNode()
    code_runner_node.init_python_repl()
    res = code_runner_node.run_code(RunCodeInput(code=code))

    return {
        "type": "success",
        "content": {
            "result": res,
        },
    }


FUNCTION_TOOL_ENTITIES = {
    "code_interpreter": serve_code_interpreter,
}

STATEFUL_TOOL_ENTITIES = {
    "example_stateful_tool": ExampleStatefulToolEntity,
}

def register_function_tool(func):
    FUNCTION_TOOL_ENTITIES[func.__name__] = func
    return func

def register_stateful_tool(cls):
    STATEFUL_TOOL_ENTITIES[cls.__name__] = cls
    return cls

class ToolConfig(BaseModel):
    name: str = Field(description="工具名称")
    entity_name: str = Field(description="工具实体名称")
    summary: str = Field(description="工具描述")
    parameters: list[Parameter] = Field(description="参数列表")
    responses: dict[str, Response] = Field(description="响应列表")


class Tool:
    config: ToolConfig
    entity: BaseToolEntity

    def __init__(self, config: ToolConfig):
        self.config = config
        entity_name = config.entity_name

        if entity_name in FUNCTION_TOOL_ENTITIES:
            self.entity = FunctionToolEntity(FUNCTION_TOOL_ENTITIES[entity_name])
        elif entity_name in STATEFUL_TOOL_ENTITIES:
            self.entity = STATEFUL_TOOL_ENTITIES[entity_name]()
        else:
            raise Exception(f"Tool entity {entity_name} not found.")

    # TODO: response check and type convert
    def call(self, **kwargs):
        return self.entity.call(**kwargs)

    def need_llm_generate_parameters(self) -> bool:
        return self.entity.need_llm_generate_parameters()

    def need_llm_generate_response(self) -> bool:
        return self.entity.need_llm_generate_response()

    def has_done(self) -> bool:
        return self.entity.current_state() == State.DONE

class Tools:
    tools: dict[str, Tool]

    def __init__(self,yaml_file_path:str):
        self.tools = {}
        # 获取调用此方法的栈帧
        stack = inspect.stack()
        caller_frame = stack[2]
        # 获取调用者的文件路径
        caller_path = caller_frame.filename
        # 获取调用者的目录路径
        caller_dir = os.path.dirname(caller_path)
        # 构建 openai.yaml 文件的绝对路径
        yaml_file_path = os.path.join(caller_dir, yaml_file_path)
        print(f'yaml_file_path:{yaml_file_path}')
        tools_yaml_path = yaml_file_path
        # 读取 tools.yaml 文件，初始化所有 tools
        with open(tools_yaml_path, "r") as f:
            config_obj = yaml.safe_load(f)
            for tool_name, tool_config in config_obj["tools"].items():
                self.tools[tool_name] = Tool(config=ToolConfig(**tool_config))

    def get_tool(self, tool_name: str) -> Tool:
        # 找到对应的工具
        tool = self.tools.get(tool_name)
        if tool is None:
            raise ValueError(f"No tool named {tool_name} found.")

        return tool

    def get_tool_summary(self, tool_name: str) -> str:
        # 在 tools.yaml 文件中找到对应的工具
        tool = self.tools.get(tool_name)
        if tool is None:
            raise ValueError(f"No tool named {tool_name} found.")

        return tool.config.summary

    def get_tools_list_summary(self, tools_list: list[str]) -> dict[str, str]:
        tools_summary = {}
        for tool_name in tools_list:
            summary = self.get_tool_summary(tool_name)
            tools_summary[tool_name] = summary
        return tools_summary
