from pydantic import BaseModel, Field

from ..base_assignment import BaseAssignment, AssignmentOutput, AssignmentConfig

from src.core.nodes.base_node import NodeInput
from src.core.nodes import (
    DataAnalysisNode,
    LoadDataInput,
    OpenAINode,
    ChatInput,
    CodeRunnerNode,
    RunCodeInput,
)

from src.core.assignments.data.analyze_data_prompt import *


from src.utils.output_parser import LLMOutputParser
from src.utils.router_generator import generate_assignment_end_point


class AnalyzeDataInput(BaseModel):
    data_file_paths: list[str] = Field(description="Path of data files (json or csv).")
    queries: list[str] = Field(description="Queries for data analysis.")


analyze_data_config = {
    "name": "analyze_data",
    "description": "Analyze data with bunch of queries.",
}


@generate_assignment_end_point
class AnalyzeDataAssignment(BaseAssignment):
    config: AssignmentConfig = AssignmentConfig(**analyze_data_config)

    def __init__(self):
        self.chat_node = OpenAINode()
        self.code_runner_node = CodeRunnerNode()
        self.data_analysis_node = DataAnalysisNode()

        self.nodes = {
            "openai": self.chat_node,
            "code_runner": self.code_runner_node,
            "data_analysis": self.data_analysis_node,
        }
        self.output = AssignmentOutput(
            "data_analysis",
            OUTPUT_SCHEMA,
            LLMOutputParser,
        )

    async def run(self, input: AnalyzeDataInput) -> AssignmentOutput:
        pass
        # step 1: load data
        # for file_path in input.data_file_paths:
        #     load_data_input = LoadDataInput(
        #         source_type=file_path.split(".")[-1].lower(),
        #         source_path=file_path,
        #     )

        #     self.data_analysis_node.load_data(load_data_input)

        # # step 2: run queries
        # df_num = len(self.data_analysis_node.data)
        # if df_num > 1:
        #     # multiple dataframes
        #     pass
        # elif df_num == 1:
        #     # single dataframes
        #     chat_input = ChatInput(
        #         model="gpt-4",
        #         message_text=self._construct_single_df_prompt(input.queries),
        #     )
        # else:
        #     raise Exception("No data loaded.")

        # raw_chat_output = self.chat_node.chat(chat_input)
        # chat_output = LLMOutputParser.parse_output(raw_chat_output)
        # if "Answer" not in chat_output:
        #     raise Exception("No answer found.")

        # # step 3: run code

        # # create python environment
        # if df_num > 1:
        #     # multiple dataframes
        #     pyenv = {
        #         f"df{i+1}": df
        #         for i, df in enumerate(self.data_analysis_node.data.values())
        #     }
        # elif df_num == 1:
        #     # single dataframes
        #     pyenv = {"df": self.data_analysis_node.data.values()[0]}

        # # init python environment
        # self.code_runner_node.init_python_repl(locals_=pyenv)
        # run_code_output = []
        # for code in chat_output["Answer"]:
        #     run_code_input = RunCodeInput(
        #         code=code,
        #     )
        #     run_code_output.append(self.code_runner_node.run_code(run_code_input))

        # # step 4: return code output to LLM

        # # TODO: implement chat with memory in OpenAI node

        # # step 5: return LLM output to user

    def _construct_single_df_prompt(self, querys: list[str], row_num: int = 5):
        for value in self.data_analysis_node.data.values():
            header = value.head(row_num).to_markdown()
            break

        queries_str = "\n".join([f"{i}: {query}" for i, query in enumerate(querys)])

        prompt = SINGLE_DF.format(
            df_header=header,
        ) + GEN_CODE.format(
            output_format=CODE_FORMAT,
            queries=queries_str,
        )

        return prompt
