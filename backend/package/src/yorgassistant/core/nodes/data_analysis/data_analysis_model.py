from pydantic import BaseModel
from typing import List, Dict, Union, Optional


class LoadDataInput(BaseModel):
    name: Optional[str]  # Name of the file, if no provided, use the file name
    source_type: str  # 'csv', 'json', etc.
    source_path: str  # File path or URL


class CleanDataInput(BaseModel):
    name: str  # Name of the file to clean
    drop_columns: Optional[List[str]]  # List of column names to drop
    fill_na: Optional[
        Dict[str, Union[str, float, int]]
    ]  # Dictionary specifying what value to replace NaN with for each column
