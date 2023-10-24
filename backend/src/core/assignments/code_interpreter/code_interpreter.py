from enum import Enum
from pydantic import BaseModel, Field

from ..base_assignment import BaseAssignment, AssignmentConfig, AssignmentOutput
from .code_interpreter_backend import InterpreterBackend
from .code_interpreter_prompt import *


from src.utils.output_parser import RawOutputParser
from src.utils.router_generator import generate_assignment_end_point
from src.utils.singleton import Singleton

code_interpreter_config = {
    "name": "code_interpreter",
    "description": "Ask question to LLM and execute code.",
}


class ActionType(str, Enum):
    FILE = "file"
    QUERY = "query"


class CodeInterpreterInput(BaseModel):
    type: ActionType = Field(default=ActionType.QUERY, description="Type of input.")
    content: str = Field(description="Content of input.")


class CodeInterpreterOutput(BaseModel):
    history: list[dict] = Field(description="History of LLM.")
    can_continue: bool = Field(description="Whether conversation can continue.")


@generate_assignment_end_point
class CodeInterpreterAssignment(BaseAssignment):
    config: AssignmentConfig = AssignmentConfig(**code_interpreter_config)

    def __init__(self):
        self.interpreter_backend = InterpreterBackend()
        self.output = AssignmentOutput(
            "interpreter_output",
            OUTPUT_SCHEMA,
            RawOutputParser,
        )
        self.can_continue = True

    async def run(self, input: CodeInterpreterInput) -> AssignmentOutput:
        match input.type:
            case ActionType.FILE:
                self.interpreter_backend.add_file(input.content)
            case ActionType.QUERY:
                self.interpreter_backend.add_query(input.content)
                resp = self.interpreter_backend.run()
                self.can_continue = self.interpreter_backend.handle_resp(resp)

        # TODO use assignment output instead
        self.output.load(
            {
                "history": self.interpreter_backend.conversation,
                "can_continue": self.can_continue,
            }
        )

        return self.output
