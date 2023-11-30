import ast
import os
import subprocess
import logging

from pathlib import Path
from itertools import islice
from typing import Optional
from pydantic import BaseModel, Field

from src.core.nodes import Document


class FileAction(BaseModel):
    action: str = Field(description="Plan action.")
    file_path: str = Field(description="File path for action.")
    content: Optional[str] = Field(description="Content for action.")

    def __str__(self):
        output = f"""
# {self.file_path}

"""

        if self.content is not None:
            if self.content.startswith("```"):
                output += f"""
{self.content}

"""
            else:
                output += f"""
```python
{self.content}
```

"""
        else:
            output += f"""
**Remove this file.**

"""
        return output


class RepoFileHandler:
    """
    This class is responsible for managing the files of the software engineer.
    It will manage all the file from a single git repo.
    """

    root_path: Optional[Path]
    focus_files: set[str]
    file_tree_str: str
    readme_content: str

    def __init__(self, repo_path: Path):
        self.root_path = repo_path
        self.focus_files = set()
        self.file_tree_str = self._generate_file_tree_str()
        self.file_dependencies = {}
        self.file_classes = {}

    def add_focus_file(self, file_path):
        """
        Add a file to the interest file set.
        """
        full_path = file_path

        if os.path.exists(full_path):
            if file_path in self.focus_files:
                logging.warning(f"Try to add existing file {file_path}.")
            self.focus_files.add(file_path)
        else:
            raise FileNotFoundError(f"File {full_path} does not exist.")

    def remove_focus_file(self, file_path):
        """
        Remove a file from the interest file set.
        """
        if file_path in self.focus_files:
            self.focus_files.remove(file_path)
        else:
            logging.warning(f"Try to remove unexisting file {file_path}.")

    def set_focus_file(self, focus_files: list[str]):
        """
        Set the focus file.
        """
        self.focus_files.clear()
        for file in focus_files:
            self.add_focus_file(file)

    def get_focus_files_content(self, limit_files: int = 5):
        """
        Get the content of the focus files (only output first 5 files).
        """
        return {
            file_path: file_content
            for file_path, file_content in islice(
                zip(self.focus_files, map(self.get_file_content, self.focus_files)),
                limit_files,
            )
        }

    def get_file_content(self, file_path: str, limit_lines: int = 200):
        """
        Get the content of a file.
        """
        full_path = file_path

        if os.path.exists(full_path):
            with open(full_path, "r") as f:
                lines = []
                line = f.readline()
                while line:
                    lines.append(line)
                    line = f.readline()
                    if len(lines) > limit_lines:
                        lines.append("... (too many lines)")
                        break

                return "\n".join(lines)
        else:
            raise FileNotFoundError(f"File {full_path} does not exist.")

    def _add_file(self, file_path: str, content: str):
        """
        Add a file to the repo.
        """
        full_path = self.root_path / file_path

        if os.path.exists(full_path):
            raise FileExistsError(f"File {full_path} already exists.")
        else:
            with open(full_path, "w") as f:
                f.write(content)

    def _remove_file(self, file_path: str):
        """
        Remove a file from the repo.
        """
        full_path = self.root_path / file_path

        if os.path.exists(full_path):
            os.remove(full_path)
        else:
            raise FileNotFoundError(f"File {full_path} does not exist.")

    def _modify_file(self, file_path: str, content: str):
        """
        Modify a file in the repo.
        """
        full_path = self.root_path / file_path

        if os.path.exists(full_path):
            with open(full_path, "w") as f:
                f.write(content)
        else:
            raise FileNotFoundError(f"File {full_path} does not exist.")

    def _generate_file_tree_str(self):
        result = subprocess.run(
            ["tree", "."], stdout=subprocess.PIPE, cwd=self.root_path
        )
        result.check_returncode()
        return result.stdout.decode("utf-8")

    def _load_readme(self):
        readme_file_names = ["README.md", "README", "README.txt"]
        for readme_file_name in readme_file_names:
            readme_path = self.root_path / readme_file_name
            if os.path.exists(readme_path):
                with open(readme_path, "r") as f:
                    return f.read()

        return ""

    
    def _get_imports_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            node = ast.parse(f.read())

        imports = []
    
        for n in ast.walk(node):
            # if isinstance(n, ast.Import):
            #     for alias in n.names:
            #         imports.append(alias.name)
            if isinstance(n, ast.ImportFrom):
                module = n.module
                for alias in n.names:
                    imports.append(f"{module}.{alias.name}")
        return imports
    
    def _generate_file_dependencies(self):
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            for filename in filenames:
                if filename.endswith('.py'):
                    full_path = os.path.join(dirpath, filename)
                    self.file_dependencies[full_path] = self._get_imports_from_file(full_path)
        return self.file_dependencies
    
    def _get_classes_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            node = ast.parse(f.read())
        
        classes = []
        classes = [n.name for n in ast.walk(node) if isinstance(n, ast.ClassDef)]
        return classes


    def _generate_file_classes(self):
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            for filename in filenames:
                if filename.endswith('.py'):
                    full_path = os.path.join(dirpath, filename)
                    classes_in_file = self._get_classes_from_file(full_path)
                    self.file_classes[full_path] = classes_in_file
        return self.file_classes



    def _generate_third_party_list(self):
        with open("requirements.txt", "r") as f:
            third_party_libraries = [line.split('==')[0] for line in f.readlines()]
        return third_party_libraries
