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
from .example_stateful_tool_entity import ExampleStatefulToolEntity
from ..config import YamlPathConfig

# 示例工具函数
def serve_code_interpreter(code: str) -> dict[str, any]:
    from ...nodes.code_runner.code_runner import CodeRunnerNode, RunCodeInput

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
    "swe_tool":SWEToolEntity,
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
    _tool_type: str  # 使用一个内部变量来存储 tool_type 的值

    def __init__(self, config: ToolConfig):
        self.config = config
        entity_name = config.entity_name

        if entity_name in FUNCTION_TOOL_ENTITIES:
            self.entity = FunctionToolEntity(FUNCTION_TOOL_ENTITIES[entity_name])
            self._tool_type = 'function'
        elif entity_name in STATEFUL_TOOL_ENTITIES:
            self.entity = STATEFUL_TOOL_ENTITIES[entity_name]()
            self._tool_type = 'stateful'
        else:
            raise Exception(f"Tool entity {entity_name} not found.")

    @property
    def tool_type(self):
        return self._tool_type

    @tool_type.setter
    def tool_type(self, value):
        self._tool_type = value
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

    def __init__(self):
        self.tools = {}
        # 获取调用此方法的栈帧
        stack = inspect.stack()
        caller_frame = stack[1]
        # 获取调用者的文件路径
        caller_path = caller_frame.filename
        # 获取调用者的目录路径
        caller_dir = os.path.dirname(caller_path)
        # 构建 openai.yaml 文件的绝对路径
        yaml_file_path = os.path.join(caller_dir, YamlPathConfig.tools_yaml_path)
        tools_yaml_path = yaml_file_path
        # 读取 tools.yaml 文件，初始化所有 tools
        with open(tools_yaml_path, "r") as f:
            config_obj = yaml.safe_load(f)
            for tool_name, tool_config in config_obj["tools"].items():
                self.tools[tool_name] = Tool(config=ToolConfig(**tool_config))

    def set_tools_yaml_path(yaml_path:str):
        # 检查 yaml_path 是否为绝对路径
        if not os.path.isabs(yaml_path):
            # 获取调用此方法的栈帧
            stack = inspect.stack()
            caller_frame = stack[1]
            # 获取调用者的文件路径
            caller_path = caller_frame.filename
            # 获取调用者的目录路径
            caller_dir = os.path.dirname(caller_path)
            # 构建 yaml 文件的绝对路径
            full_yaml_path = os.path.join(caller_dir, yaml_path)
        else:
            full_yaml_path = yaml_path
        # 获取 yaml 文件所在的目录
        yaml_dir = os.path.dirname(full_yaml_path)
        # 如果目录不存在，则创建它
        os.makedirs(yaml_dir, exist_ok=True)
        # 设置 yaml_path
        YamlPathConfig.tools_yaml_path = full_yaml_path

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