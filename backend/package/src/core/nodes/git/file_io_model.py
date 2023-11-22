from pydantic import BaseModel


class FileInput(BaseModel):
    path: str


class DirectoryInput(BaseModel):
    path: str


# replace the entire file content with the new content
class EditFileInput(FileInput):
    content: str


# change file content at specific line int -> str
class EditFileLineInput(FileInput):
    change_list: list[int, str]
