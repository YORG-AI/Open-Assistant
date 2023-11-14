import yaml
import os

from pydantic import BaseModel, Field

from .tool_entity import (
    BaseToolEntity,
    FunctionToolEntity,
)
from .model import Parameter, Response

from .swe_tool_entity import SWEToolEntity
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
    "example_stateful_tool_entity": ExampleStatefulToolEntity,
    "swe_tool_entity": SWEToolEntity,
}


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
        return self.entity.current_state() == "done"


class Tools:
    tools: dict[str, Tool]

    def __init__(self):
        self.tools = {}

        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建 tools.yaml 文件的绝对路径
        tools_yaml_path = os.path.join(current_dir, "tools.yaml")

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
