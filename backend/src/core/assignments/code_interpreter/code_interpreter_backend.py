import json
import os
from enum import Enum
from abc import ABC, abstractmethod

from src.core.nodes import (
    OpenAINode,
    CompleteInput,
    OpenAIResp,
    CodeRunnerNode,
    Message,
    RunCodeInput,
    FunctionDefinition,
    DataAnalysisNode,
    LoadDataInput,
)

from .code_interpreter_prompt import *


class InterpreterBackend:
    """
    Backend for AnalyzeDataAssignment.
    """

    openai_node: OpenAINode
    code_runner_node: CodeRunnerNode
    functions: dict[str, callable]
    conversation: list[dict[str, str]]

    def __init__(self):
        self.openai_node = OpenAINode()
        self.code_runner_node = CodeRunnerNode()
        self.data_analysis_node = DataAnalysisNode()
        self.functions = {
            "run_code": lambda code: self.code_runner_node.run_code(
                RunCodeInput(
                    code=code,
                )
            )
        }
        self.conversation = []

        self.openai_node.add_function(
            FunctionDefinition(
                name="run_code",
                description="Executes python code and returns the output",
                parameters=[
                    FunctionDefinition.FunctionParameter(
                        name="code",
                        description="Python code to run.",
                        required=True,
                    )
                ],
            )
        )

    def add_file(self, file_path: str):
        prompt = f"Add new file."

        file_name = os.path.basename(file_path)
        file_type = file_name.split(".")[-1]
        prompt += FILE_INFOMATION_PROMPT.format(
            file_name=file_name,
            file_type=file_type,
            file_path=file_path,
        )

        if file_type == "csv" or file_type == "json":
            self.data_analysis_node.load_data(
                LoadDataInput(
                    name=file_name,
                    source_type=file_type,
                    source_path=file_path,
                )
            )
            prompt += DF_CONTENT_PROMPT.format(
                n=5,
                content=self.data_analysis_node.data[file_name].head(5),
            )

        self.conversation.append(
            {
                "role": "system",
                "content": f"Add new {file_type} file {file_name} at {file_path}.",
            }
        )

        self.openai_node.add_single_message(
            Message(
                role="system",
                content=prompt,
            ),
        )

    def add_query(self, query: str):
        self.conversation.append(
            {
                "role": "user",
                "content": query,
            }
        )

        self.openai_node.add_single_message(
            Message(
                role="user",
                content=PREFIX + query + SUFFIX,
            ),
        )

    def run(self) -> OpenAIResp:
        return self.openai_node.complete(
            CompleteInput(
                model="gpt-4",
                use_streaming=False,
            ),
        )

    def handle_resp(self, resp: OpenAIResp) -> bool:
        handlers = [
            TextMessageHandler(),
            FunctionCallHandler(),
        ]

        can_continue = True

        for handler in handlers:
            if can_continue and handler.verify(resp):
                can_continue = handler.handle(self, resp)

        return can_continue

    def get_history(self) -> list[dict[str, str]]:
        return self.openai_node.history


class RespHandler(ABC):
    @abstractmethod
    def verify(self, resp: OpenAIResp) -> bool:
        pass

    @abstractmethod
    def handle(self, backend: InterpreterBackend, resp: OpenAIResp) -> bool:
        pass


class TextMessageHandler(RespHandler):
    def verify(self, resp: OpenAIResp) -> bool:
        return (
            resp.message.role is not None
            and resp.message.content is not None
            and resp.finish_reason != "function_call"
        )

    def handle(self, backend: InterpreterBackend, resp: OpenAIResp) -> bool:
        backend.conversation.append(
            resp.message.dict(exclude_none=True),
        )
        if resp.message.role == "assistant":
            try:
                data = json.loads(resp.message.content)
                if "role" in data and "content" in data:
                    if data["role"] == "function_call":
                        function_call = data["content"]
                        function_name = function_call["function"].strip(".")[-1]
                        code = function_call["code"]

                        if function_name in [
                            function_desp["name"]
                            for function_desp in backend.openai_node.functions
                        ]:
                            func = backend.functions[function_name]  # get function
                            try:
                                backend.conversation.append(
                                    {
                                        "role": "system",
                                        "content": "```python\n{code}\n```".format(
                                            code=code
                                        ),
                                    }
                                )
                                # backend.openai_node.add_single_message(
                                #     Message(
                                #         role="system",
                                #         content=f"Call function {function_name}({arguments_str})",
                                #     ),
                                # )

                                result = func(code)  # call function

                                backend.conversation.append(
                                    {
                                        "role": "function",
                                        "name": function_name,
                                        "content": result,
                                    }
                                )
                                backend.openai_node.add_single_message(
                                    Message(
                                        role="function",
                                        name=function_name,
                                        content=result,
                                    ),
                                )
                            except json.JSONDecodeError:
                                # TODO: handle argument error
                                backend.conversation.append(
                                    {
                                        "role": "system",
                                        "content": f"GPT generate wrong function arguments: {format(code)}",
                                    }
                                )

                                backend.openai_node.add_single_message(
                                    Message(
                                        role="system",
                                        content=f"GPT generate wrong function arguments: {format(code)}",
                                    ),
                                )
                                return False
                            except Exception as e:
                                backend.conversation.append(
                                    {
                                        "role": "system",
                                        "content": f"Backend error: {e}",
                                    }
                                )

                                backend.openai_node.add_single_message(
                                    Message(
                                        role="system",
                                        content=f"Backend error: {e}",
                                    ),
                                )
                            return True
            except json.JSONDecodeError:
                pass
        else:
            backend.openai_node.add_single_message(resp.message)
        return True


class FunctionCallHandler(RespHandler):
    def verify(self, resp: OpenAIResp) -> bool:
        return (
            resp.message.function_call is not None
            and resp.finish_reason == "function_call"
        )

    def handle(self, backend: InterpreterBackend, resp: OpenAIResp) -> bool:
        # TODO: call function and get result
        function_name = resp.message.function_call.name
        arguments_str = resp.message.function_call.arguments

        if function_name in [
            function_desp["name"] for function_desp in backend.openai_node.functions
        ]:
            func = backend.functions[function_name]  # get function
            try:
                arguments = json.loads(arguments_str)  # get arguments
                backend.conversation.append(
                    {
                        "role": "system",
                        "content": "```python\n{code}\n```".format(
                            code=arguments["code"].strip('"')
                        ),
                    }
                )
                # backend.openai_node.add_single_message(
                #     Message(
                #         role="system",
                #         content=f"Call function {function_name}({arguments_str})",
                #     ),
                # )

                result = func(**arguments)  # call function

                backend.conversation.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": result,
                    }
                )
                backend.openai_node.add_single_message(
                    Message(
                        role="function",
                        name=function_name,
                        content=result,
                    ),
                )
            except json.JSONDecodeError:
                # TODO: handle argument error
                backend.conversation.append(
                    {
                        "role": "system",
                        "content": f"GPT generate wrong function arguments: {format(arguments_str)}",
                    }
                )

                backend.openai_node.add_single_message(
                    Message(
                        role="system",
                        content=f"GPT generate wrong function arguments: {format(arguments_str)}",
                    ),
                )
                return False
            except Exception as e:
                backend.conversation.append(
                    {
                        "role": "system",
                        "content": f"Backend error: {e}",
                    }
                )

                backend.openai_node.add_single_message(
                    Message(
                        role="system",
                        content=f"Backend error: {e}",
                    ),
                )
            return True
