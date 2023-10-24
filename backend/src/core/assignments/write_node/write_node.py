from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_fixed

from .write_node_prompt import *
from ..base_assignment import BaseAssignment, AssignmentOutput, AssignmentConfig

from src.core.nodes.base_node import NodeInput
from src.core.nodes.openai.openai import OpenAINode
from src.core.nodes.openai.openai_model import ChatInput
from src.utils.output_parser import LLMOutputParser
from src.utils.router_generator import generate_assignment_end_point


class WriteNodeInput(BaseModel):
    node_name: str = Field(description="Name of a node.")
    operations: Operations = Field(description="Operations of a node.")


write_node_config = {
    "name": "write_node",
    "description": "Write a node.",
}


@generate_assignment_end_point
class WriteNodeAssignment(BaseAssignment):
    config: AssignmentConfig = AssignmentConfig(**write_node_config)

    def __init__(self):
        self.nodes = {"openai": OpenAINode()}
        self.output = AssignmentOutput(
            "node",
            OUTPUT_SCHEMA,
            LLMOutputParser,
        )

    @retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
    async def run(self, input: WriteNodeInput) -> AssignmentOutput:
        # TBD: search and summary

        prompt = PROMPT_TEMPLATE.format(
            node_name=input.node_name,
            operations_list=input.operations,
            base_node_code=BASE_NODE_CODE,
            example_node_code=NODE_EXAMPLE,
            format_example=FORMAT_EXAMPLE,
        )

        node_input = NodeInput(
            func_name="chat",
            func_input=ChatInput(
                model="gpt-4",
                message_text=prompt,
            ),
        )

        text_output = self.nodes["openai"].run(node_input)
        self.output.load(text_output)
        return self.output
