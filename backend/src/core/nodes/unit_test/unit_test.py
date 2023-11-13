from typing import Optional
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.unit_test.unit_test_model import (
    CodeInput,
    UnitTestOutput,
    CodeFromFileInput,
)
from src.core.nodes.openai.openai import OpenAINode
from src.core.nodes import Message, ChatInput
from src.utils.router_generator import generate_node_end_points
from src.core.nodes.unit_test.unit_test_prompt import *

unit_test_config = {
    "name": "unit_test",
    "description": "generate the unit test for the given code.",
    "functions": {"generate_unit_test": "generate the unit test."},
}


@generate_node_end_points
class UnitTestNode(BaseNode):
    config: NodeConfig = NodeConfig(**unit_test_config)

    def __init__(self):
        super().__init__()
        self.init_openai_node()

    def generate_unit_test(self, input: CodeInput):
        # 1. 获得Code
        # 2. 调用GPT，生成对应code的unit_test
        resp = self.openai_node.chat(
            input=ChatInput(
                model="gpt-4",
                message_text=UNIT_TEST_CODE_PROMPT.format(
                    test_code=input.code,
                ),
            ),
        )
        # TODO 格式化content，仅获取unit test的code部分
        """
        if code.startswith("```python"):
            code = code[10:]

        if code.endswith("```"):
            code = code[:-3]

        return code
        """
        # print('resp: ')
        # print(resp)
        # print('resp type: ')
        # print(type(resp))

        # print(resp.message.content)
        return resp.message.content

    def init_openai_node(self):
        self.openai_node = OpenAINode()
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=STE_PROMPT,
            )
        )
