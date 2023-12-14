from fastapi import UploadFile, File, Form
from typing import Optional

import pandas as pd

from ..base_node import BaseNode, NodeConfig
from .data_analysis_model import (
    LoadDataInput,
    CleanDataInput,
)
from ...common_models import (
    UserProperties,
    DEFAULT_DATA_ANALYSIS_FOLDER,
)

data_analysis_node_config = {
    "name": "data_analysis",
    "description": "A node for data analysis tasks.",
    "functions": {
        "load_data_from_file": "Load data from a given file.",
        "load_data": "Load data from a given source.",
        "clean_data": "Clean the loaded data.",
    },
}


class DataAnalysisNode(BaseNode):
    config: NodeConfig = NodeConfig(**data_analysis_node_config)

    data: dict[str, pd.DataFrame | str] = None  # To hold the loaded data
    user_properties = None  # To hold the user properties

    def __init__(self):
        super().__init__()
        self.data = {}

    def load_data_from_file(
        self,
        input: UploadFile = File(...),
        properties: UserProperties = Form(...),
    ):
        source_path = (
            DEFAULT_DATA_ANALYSIS_FOLDER
            / properties.user_id
            / properties.session_id
            / input.filename
        )
        source_path.parent.mkdir(parents=True, exist_ok=True)
        self.user_properties = properties
        with open(source_path, "wb") as buffer:
            buffer.write(input.file.read())
        load_data_input = LoadDataInput(
            source_type=input.filename.split(".")[-1].lower(),
            source_path=str(source_path),
        )
        return self.load_data(
            load_data_input=load_data_input,
        )

    def load_data(self, input: LoadDataInput):
        if input.name is None:
            input.name = input.source_path.split("/")[-1].split(".")[0]
        try:
            if input.source_type == "csv":
                self.data[input.name] = pd.read_csv(input.source_path)
            elif input.source_type == "json":
                self.data[input.name] = pd.read_json(input.source_path)
            else:
                self.data[input.name] = input.source_path
            # Add more source types as needed
            return f"Data loaded successfully."
        except Exception as e:
            return f"An error occurred while loading the data: {e}"

    def clean_data(self, input: CleanDataInput):
        try:
            if input.name in self.data.keys():
                return "No data loaded to clean."

            if input.drop_columns:
                self.data[input.name].drop(columns=input.drop_columns, inplace=True)

            if input.fill_na:
                self.data[input.name].fillna(value=input.fill_na, inplace=True)

            return "Data cleaned successfully."
        except Exception as e:
            return f"An error occurred while cleaning the data: {e}"
