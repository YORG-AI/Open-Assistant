from typing import Optional
from pydantic import BaseModel, Field


class RunCodeInput(BaseModel):
    code: str = Field(description="Python code to be executed.")


class RunCodeFromFileInput(BaseModel):
    working_dir: str = Field(description="Working directory for the code.")
    file_path: str = Field(description="Entry python file to be executed.")

    kwargs: Optional[dict] = Field(default={}, description="Keyword arguments.")
