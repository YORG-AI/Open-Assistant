from pathlib import Path

from ..base_node import BaseNode, NodeConfig
from .git_base_node import GitBaseNode
from .file_io_model import FileInput, DirectoryInput, EditFileInput, EditFileLineInput


file_io_node_config = {
    "name": "file_io",
    "description": "A node that implements common file operations.",
    "functions": {
        "create_file": "Create a file.",
        "create_file_with_content": "Create a file with given content.",
        "delete_file": "Delete a file.",
        "create_directory": "Create a directory.",
        "edit_file": "Edit a file.",
        "edit_file_line": "Edit a line of a file.",
    },
}


class FileIONode(GitBaseNode):
    config: NodeConfig = NodeConfig(**file_io_node_config)

    def create_file(self, input: FileInput):
        file_path = Path(input.path)
        try:
            file_path.parents[0].mkdir(parents=True, exist_ok=True)
            Path(file_path).touch()
            return {"status": f"File {str(file_path)} created successfully."}
        except Exception as e:
            return str(e)

    def create_file_with_content(self, input: EditFileInput):
        file_path = Path(input.path)
        try:
            file_path.parents[0].mkdir(parents=True, exist_ok=True)
            Path(file_path).touch()
            with file_path.open("w", encoding="utf-8") as f:
                f.write(input.content)
            return {
                "status": f"File {str(file_path)} created successfully with given content."
            }
        except Exception as e:
            return str(e)

    def delete_file(self, input: FileInput):
        file_path = Path(input.path)
        try:
            file_path.parents[0].mkdir(parents=True, exist_ok=True)
            Path(file_path).unlink()
            return {"status": f"File {str(file_path)} deleted successfully."}
        except Exception as e:
            return str(e)

    def create_directory(self, input: DirectoryInput):
        file_path = Path(input.path)
        try:
            file_path.mkdir(parents=True, exist_ok=True)
            return {"status": f"Directory {str(file_path)} created successfully."}
        except Exception as e:
            return str(e)

    edit_file = create_file_with_content

    def edit_file_line(self, input: EditFileLineInput):
        file_path = Path(input.path)
        lines = []
        changed = []
        unchanged = []
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
            for k, v in input.change_list.items():
                if 0 <= k < len(lines):
                    lines[k] = v
                    changed.appned(k)
                else:
                    unchanged.append(k)

            with open(file_path, "w") as file:
                file.writelines(lines)

            return {
                "status": f"File {str(file_path)} changed successfully, lines {str(changed)} changed, lines {str(unchanged)} unchanged."
            }
        except Exception as e:
            return str(e)
