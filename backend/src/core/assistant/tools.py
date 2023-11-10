import yaml
from typing import Any, Dict, Callable
import os
import inspect

# 示例工具函数
def serve_code_interpreter(text: str) -> Dict[str, Any]:
    # 这里是你的代码解释器的实现
    return {'type':'success','context':'test success'}

def serve_data_analyzer(data: object) -> Dict[str, Any]:
    # 这里是你的代码解释器的实现
    return {'type':'success','context':'test success'}



class Tools:
    def __init__(self):
        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建 tools.yaml 文件的绝对路径
        tools_yaml_path = os.path.join(current_dir, 'tools.yaml')

        with open(tools_yaml_path, 'r') as f:
            self.tools_config = yaml.safe_load(f)

  
        # 将工具函数映射到工具名称
        self.tools = {name: func for name, func in globals().items() if inspect.isfunction(func)}

    def call(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        # 在 tools.yaml 文件中找到对应的工具
        tool_config = self.tools_config.get('tools').get(tool_name)
        if tool_config is None:
            raise ValueError(f"No tool named {tool_name} found.")

        # 获取 operationId
        operation_id = tool_config.get('get', {}).get('operationId')
        if operation_id is None:
            raise ValueError(f"No operationId found for tool {tool_name}.")

        # 获取对应的函数
        tool = self.tools.get(operation_id)
        if tool is None:
            raise ValueError(f"No function found for operationId {operation_id}.")

        return tool(**parameters)

    def get_tool_summary(self, tool_name: str) -> str:
        # 在 tools.yaml 文件中找到对应的工具
        tool_config = self.tools_config.get('tools').get(tool_name)
        if tool_config is None:
            raise ValueError(f"No tool named {tool_name} found.")

        # 获取 summary
        summary = tool_config.get('get', {}).get('summary')
        if summary is None:
            raise ValueError(f"No summary found for tool {tool_name}.")

        return summary

    def get_tools_list_summary(self, tools_list:list) -> dict:
        tools_summary = {}
        print(f'tools_list:{tools_list}')
        for tool_name in tools_list:
            summary = self.get_tool_summary(tool_name)
            tools_summary[tool_name] = summary
        return tools_summary
