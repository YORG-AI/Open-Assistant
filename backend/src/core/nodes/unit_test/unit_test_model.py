from typing import Optional
from pydantic import BaseModel, Field


class CodeInput(BaseModel):
    code: str = Field(description="Python code to be generate unit test.")


class UnitTestOutput(BaseModel):
    unit_test: str = Field(description="Unit test for the given code.")


class CodeFromFileInput(BaseModel):
    working_dir: str = Field(description="Working directory for the code.")
    file_path: str = Field(description="Entry python file to be executed.")
    kwargs: Optional[dict] = Field(default={}, description="Keyword arguments.")
