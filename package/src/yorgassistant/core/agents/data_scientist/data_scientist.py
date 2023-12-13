from pathlib import Path

import pandas as pd
import logging

from .data_scientist_prompt import *
from ..base_agent import BaseAgent, AgentConfig

from ...nodes import (
    OpenAINode,
    ChatInput,
    DataAnalysisNode,
    LoadDataInput,
)

data_scientist_config = {
    "name": "data_scientist",
    "description": "A agent for data scientist.",
}


class DataScientistAgent(BaseAgent):
    config: AgentConfig = AgentConfig(**data_scientist_config)

    def __init__(self):
        self.openai_node = OpenAINode()
        self.data_analysis_node = DataAnalysisNode()

        self._init_openai_node()

    def add_data_file(self, file_path: Path):
        file_name = file_path.name
        file_type = file_path.suffix[1:]

        self.data_analysis_node.load_data(
            input=LoadDataInput(
                name=file_name,
                source_type=file_type,
                source_path=str(file_path),
            )
        )

        logging.warning(f"{file_name} loaded as {file_type}.")
        logging.warning(file_type == "csv" or file_type == "json")
        logging.warning(
            DATA_FILE_PROMPT.format(
                file_name=file_name,
                file_path=file_path,
                n=5,
                content=self.get_data_file_summary(file_name, 5),
            )
        )
        if file_type == "csv" or file_type == "json":
            # set system message about the data file
            self.openai_node.add_system_message(
                DATA_FILE_PROMPT.format(
                    file_name=file_name,
                    file_path=file_path,
                    n=5,
                    content=self.get_data_file_summary(file_name, 5, "markdown"),
                )
            )
            logging.warning(f"openai_history")
            logging.warning(self.openai_node.history)
        else:
            self.openai_node.add_system_message(
                COMMON_FILE_PROMPT.format(
                    file_name=file_name,
                    file_path=file_path,
                )
            )

    def get_data_file_summary(self, file_name: str, head_n: int = 5, output_type: str = "html"):
        if self.data_analysis_node.data.get(file_name) is None:
            return "Data file not found."

        if isinstance(self.data_analysis_node.data[file_name], pd.DataFrame):
            if output_type == "html":
                return self.data_analysis_node.data[file_name].head(head_n).to_html()
            elif output_type == "markdown":
                return self.data_analysis_node.data[file_name].head(head_n).to_markdown()
            else:
                return self.data_analysis_node.data[file_name].head(head_n).to_string()

        with open(self.data_analysis_node.data[file_name], "r") as f:
            content = f.read(300)
            if f.read(1) != "":
                content += "..."

        return content

    def query(self, query: str) -> str:
        resp = self.openai_node.chat(
            input=ChatInput(
                model="gpt-4",
                message_text=QUERY_PROMPT.format(query=query),
                append_history=True,
            )
        )

        code = resp.message.content

        if code.startswith("```python"):
            code = code[10:]

        if code.endswith("```"):
            code = code[:-3]

        return code

    def _init_openai_node(self):
        self.openai_node.add_system_message(
            DS_PROMPT,
        )
