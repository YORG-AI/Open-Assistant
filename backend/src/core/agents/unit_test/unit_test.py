import json
import logging

from typing import Optional
from pydantic import BaseModel, Field
from pathlib import Path

from ..base_agent import BaseAgent, AgentConfig
from .unit_test_prompt import *

from src.core.nodes import (
    OpenAINode,
    ChatInput,
    Message,
    UnitTestNode,
)

from src.core.nodes.unit_test.unit_test_model import *
from src.utils.output_parser import LLMOutputParser

unit_test_config = {
    "name": "unit_test",
    "description": "A agent for generating unit test on specific code.",
}


class UnitTestAgent(BaseAgent):
    config: AgentConfig = AgentConfig(**unit_test_config)

    def __init__(self) -> None:
        super().__init__()
        self.unit_test_node = UnitTestNode()
        self.input_code = ""

    def set_input_code(self, input_code: str):
        """
        Set the input code
        """
        self.input_code = input_code

    def _generate_unit_test(self):
        resp = self.unit_test_node.generate_unit_test(CodeInput(code=self.input_code))
        # print("_generate_unit_test: ")
        # print(resp)
        return resp
