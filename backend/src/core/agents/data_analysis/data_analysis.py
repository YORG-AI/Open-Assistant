import os
from pydantic import BaseModel, Field
from pathlib import Path
import pandas as pd
import re

from ..base_agent import BaseAgent, AgentConfig
from .data_analysis_prompt import *

from src.core.nodes import (
    OpenAINode,
    ChatConfig,
    OpenAIResp,
    CodeRunnerNode,
    Message,
    RunCodeInput,
    FunctionDefinition,
    DataAnalysisNode,
    LoadDataInput,
    ChatInput,
)

data_analysis_config = {
    "name": "data_analysis",
    "description": "A agent for data analysis.",
}

from src.utils.output_parser import LLMOutputParser

PROJ_PATH = Path("src/data/documents")


class StepPlan(BaseModel):
    code: str = Field(description="Step execution code.")
    result: str = Field(description="code result.")


class DataAnalysisAgent(BaseAgent):
    config: AgentConfig = AgentConfig(**data_analysis_config)

    def __init__(self):
        self.LLMmodel = "gpt-4-1106-preview"
        self.maximum_steps = 100
        self.openai_node = None
        self.code_runner_node = CodeRunnerNode()
        self.file_path_list = []
        self.data_schema_dict = {}
        self.project_type = None
        self.project_requirement = None

        self.step_plan = []
        self.step_report = []
        self.step_code = []
        self.step_result = []
        self.step_numbers = 0
        self.base_dir = ""

        self.conversation = []

    def _init_openai_node(self):
        """
        Initialize OpenAI node.
        """
        self.openai_node = OpenAINode()
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=DA_PROMPT,
            )
        )

    ### Working part

    def set_project_name(self, project_name: str):
        self.project_name = project_name
        # self.base_dir = PROJ_PATH / project_name
        if not self.base_dir.exists():
            self.base_dir.mkdir(parents=True)

    def add_file(self, file_name: str):  # Add new file existed in the project directory
        prompt = f"Add new file."

        file_type = file_name.split(".")[-1]
        file_path = os.path.join(self.base_dir, file_name)
        prompt += FILE_INFOMATION_PROMPT.format(
            file_name=file_name,
            file_type=file_type,
            file_path=file_path,
        )

        if file_type == "csv" or file_type == "json" or file_type == "xlsx":
            self.data_schema_dict["file_name"] = self.get_data_schema(file_path)

        self.conversation.append(
            {
                "role": "system",
                "content": f"Add new {file_type} file {file_name} at {file_path}.",
            }
        )
        self.file_path_list.append(file_path)

    def add_file_path(self, file_path: str):  # Add new file by path
        prompt = f"Add new file."

        file_type = file_path.split(".")[-1]
        file_name = file_path.split("/")[-1]
        prompt += FILE_INFOMATION_PROMPT.format(
            file_name=file_name,
            file_type=file_type,
            file_path=file_path,
        )

        if file_type == "csv" or file_type == "json" or file_type == "xlsx":
            self.data_schema_dict["file_name"] = self.get_data_schema(file_path)

        self.conversation.append(
            {
                "role": "system",
                "content": f"Add new {file_type} file {file_name} at {file_path}.",
            }
        )
        self.file_path_list.append(file_path)

    def set_project_requirement(self, requirement: str):
        self.project_requirement = requirement

    def get_data_schema(self, file_path):
        file_name = os.path.basename(file_path)
        file_type = file_name.split(".")[-1]
        if file_type == "csv":
            df = pd.read_csv(file_path)
        elif file_type == "json":
            df = pd.read_json(file_path)
        elif file_type == "xlsx":
            df = pd.read_excel(file_path)

        schema = {}
        for column in df.columns:
            dtype = str(df[column].dtype)
            if dtype == "object":
                dtype_detail = "string"
            elif "int" in dtype or "float" in dtype:
                dtype_detail = {
                    "type": dtype,
                    "min": df[column].min(),
                    "max": df[column].max(),
                }
            else:
                dtype_detail = dtype

        schema[column] = dtype_detail
        schema_str = str(schema)
        data_schema = DATA_SCHEMA.format(data_schema=schema_str, data_sample=df.head(3))

        return data_schema

    # generate planner prompt
    # remeber to call self._init_openai_node() to refreash the history
    def plan_project_type(self):
        self._init_openai_node()
        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.LLMmodel,
                message_text=PROJECT_TYPE_SELECTOR_PROMPT.format(
                    project_requirement=self.project_requirement
                ),
            )
        )
        resp_content = resp.message.content
        return resp_content

    def set_project_type(self, project_type: str):
        self.project_type = project_type

    # obtain data analyze plan from gpt
    def extract_plan(self, planner_output):
        # print(planner_output)
        steps = re.split(r"\n\n---\n\n", planner_output.strip())

        steps = [
            element
            for element in steps
            if (element.startswith("# Step") or element.startswith("---\n\n# Step"))
        ]

        # Stripping any leading/trailing whitespaces from each step for cleanliness
        self.step_plan = [step.strip() for step in steps]
        self.step_numbers = len(self.step_plan)

    def obtain_step_plan(self):
        planner_prompt = PLANNER_PROMPT[self.project_type].format(
            project_requirement=self.project_requirement,
            data_schema=str(self.data_schema_dict),
        )
        self._init_openai_node()
        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.LLMmodel,
                message_text=planner_prompt,
            )
        )
        resp_content = resp.message.content
        self.extract_plan(resp_content)
        self.step_report = [0 for i in range(self.maximum_steps)]
        self.step_code = [0 for i in range(self.maximum_steps)]
        self.step_result = [0 for i in range(self.maximum_steps)]

    def step_code_generator(self, step_number):
        if step_number == 0:  # first step
            step_code_prompt = (
                CODE_INTERPRETER_PREFIX
                + STEP_FILLER_BODY_STEP1.format(
                    project_requirement=self.project_requirement,
                    file_info=str(self.file_path_list),
                    data_schema=str(self.data_schema_dict),
                    step_plan=self.step_plan[step_number],
                )
                + CODE_INTERPRETER_SUFFIX
            )
        else:
            step_code_prompt = (
                CODE_INTERPRETER_PREFIX
                + STEP_FILLER_BODY_STEP_NOT1.format(
                    project_requirement=self.project_requirement,
                    file_info=str(self.file_path_list),
                    data_schema=str(self.data_schema_dict),
                    step_number_p=step_number,
                    step_number=step_number + 1,
                    step_code=self.step_code[step_number - 1],
                    step_result=self.step_result[step_number - 1],
                    step_plan=self.step_plan[step_number],
                )
                + CODE_INTERPRETER_SUFFIX
            )

        self._init_openai_node()
        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.LLMmodel,
                message_text=step_code_prompt,
            )
        )
        # logging.debug(resp.message.content)
        resp_content = resp.message.content

        match = re.search(r"```python\n(.*?)```", resp_content, re.DOTALL)

        if match:
            python_code = match.group(1)
        else:
            python_code = "no code generated"

        if python_code.startswith("```python"):
            python_code = python_code[10:]
        if python_code.endswith("```"):
            python_code = python_code[:-3]

        self.step_code[step_number] = python_code
        return python_code

    def do_code_revise(self, code, requirement, step_number):
        self._init_openai_node()
        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.LLMmodel,
                message_text=CODE_REVISE_PROMPT.format(
                    file_info=str(self.file_path_list),
                    data_schema=str(self.data_schema_dict),
                    code=code,
                    requirement=requirement,
                ),
            )
        )
        resp_content = resp.message.content

        match = re.search(r"```python\n(.*?)```", resp_content, re.DOTALL)

        if match:
            python_code = match.group(1)
        else:
            python_code = "no code generated"

        if python_code.startswith("```python"):
            python_code = python_code[10:]
        if python_code.endswith("```"):
            python_code = python_code[:-3]
            # update the revised code
        self.step_code[step_number] = python_code
        return python_code

    def step_result_filler(self, result, step_number):
        self.step_result[step_number] = result

    def step_report_generator(self, step_number):
        if step_number < self.step_numbers - 1:  # not last step
            step_report_prompt = STEP_PARAGRAPH_PROMPT.format(
                project_requirement=self.project_requirement,
                step_number=step_number + 1,
                step_plan=self.step_plan[step_number],
                step_code=self.step_code[step_number],
                step_result=self.step_result[step_number],
            )
        # TODO: add sample report for each type of task

        elif step_number == self.step_numbers - 1:
            step_report_prompt = STEP_FILLER_BODY_STEP_CONCLUSION.format(
                project_requirement=self.project_requirement,
                previous_report=self.step_report[step_number - 1],
                step_plan=self.step_plan[step_number],
            )

        self._init_openai_node()
        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.LLMmodel,
                message_text=step_report_prompt,
            )
        )
        resp_content = resp.message.content
        self.step_report[step_number] = resp_content

    # Getter and Setter
    def add_focus_file(self, file_path):
        """
        Add file to repo.
        """
        self.repo_manager.add_focus_file(file_path)
