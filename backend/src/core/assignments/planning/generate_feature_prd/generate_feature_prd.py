from pydantic import BaseModel

from write_prd_prompt import *
from ..base_assignment import BaseAssignment, AssignmentOutput


class WritePRDInput(BaseModel):
    requirement: str


class WritePRDAssignment(BaseAssignment):
    def __init__(self):
        self.nodes = {"openai": None}
        self.output = AssignmentOutput(
            "prd",
            OUTPUT_SCHEMA,
        )

    async def run(self, input: WritePRDInput) -> AssignmentOutput:
        # TBD: search and summary

        prompt = PROMPT_TEMPLATE.format(
            requirements=input.requirement, search_information="", format_example=""
        )

        chat_output = self.nodes["openai"].run(
            {
                "func_name": "complete",
                "params": {
                    "prompt": prompt,
                },
            },
        )

        self.output.parse(chat_output)
        return self.output
