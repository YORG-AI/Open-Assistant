import json
import logging
import os
import subprocess

from typing import Optional
from pydantic import BaseModel, Field
from pathlib import Path

from .understand_codebase_prompt import *
from ..base_assignment import BaseAssignment, AssignmentConfig, AssignmentOutput
from .repo_file_handler import RepoFileHandler

from src.core.nodes import (
    OpenAINode,
    AsyncOpenAINode,
    ChatInput,
    Message,
    GitRepoNode,
    GitRemoteRepositoryInput,
)

from src.utils.output_parser import LLMOutputParser


class Understanding(BaseModel):
    file_path: str = Field(description="File path for focus file.")
    related_code: str = Field(description="LLM think related code content")
    description: str = Field(description="Description for understanding of codebase.")

    def to_markdown(self):
        return f"""
- {self.file_path} 
{self.related_code} 
{self.description}
"""
    def __str__(self) -> str:
        return self.file_path + " " + self.related_code + " " + self.description + "\n"


REPO_PATH = Path("src/data/git")


understand_codebase_config = {
    "name": "understand_codebase",
    "description": "Load github repo and understand codebase.",
}


class CodeBaseAssignment(BaseAssignment):
    config: AssignmentConfig = AssignmentConfig(**understand_codebase_config)

    def __init__(self):
        self.repo_url = ""
        self.repo_path = ""
        self.root_path = ""
        self.file_tree_str = ""
        self.user_feature : list[str] = []
        self.related_content = ""
        self.abstarct = ""
        self.related_files: list[str] = []
        self.readme_content = ""
        self.user_query_code : list[str] = []
        self.understandings : list[list[Understanding]] = []
        self.dependencies = {}
        self.classes={}
        self.git_node = GitRepoNode()
        self.repo_handler : Optional[RepoFileHandler] = None
        self._init_openai_node()
    
    
    def set_repo_url(self, repo_url: str):
        """
        Set repo url.
        """
        self.repo_url = repo_url
        self.repo_path = REPO_PATH / Path(repo_url).name
        self.git_node.git_clone(
            input=GitRemoteRepositoryInput(
                url=repo_url,
                path=self.repo_path,
            )
        )
        self.repo_handler = RepoFileHandler(self.repo_path)
        
        content = REPO_STRUCTURE_PROMPT.format(
                    file_tree=self.repo_handler.file_tree_str,
                )

        # repo structure prompt
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=content,
            )
        )

    def set_local_repo(self, repo_name: str):
        """
        Set local repo path.
        """
        self.repo_path = REPO_PATH / repo_name
        self.repo_handler = RepoFileHandler(self.repo_path)

        # repo structure prompt
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=REPO_STRUCTURE_PROMPT.format(
                    file_tree=self.repo_handler.file_tree_str,
                ),
            )
        )

    def set_query_related_files(self, file_path):
        self.related_files.append(file_path)

    def set_abstarct(self, abstract):
        self.abstarct = abstract

    def generate_code_dependencies(self):
        # obtain .py file dependencies
        self.dependencies = self.repo_handler._generate_file_dependencies()
        
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=FILE_DEPENDENCIES_PROMPT.format(
                    dependencies_template = DEPENDENCIES_TEMPLATE,
                    file_dependencies=self.dependencies,
                ),
            )
        )
        return self.dependencies


    def generate_code_classes(self):
        # obtain .py file dependencies
        self.classes = self.repo_handler._generate_file_classes()
        
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=FILE_CLASSES_PROMPT.format(
                    classes_template = CLASSES_TEMPLATE,
                    file_classes=self.classes,
                ),
            )
        )
        return self.classes

    def set_code_base_query(self, user_feature: str, query_related_code: str, related_content: str):
        """
        Set feature description.
        """
        self.user_feature.append(user_feature)
        self.user_query_code.append(query_related_code)
        self.related_content = related_content


        # add feature description system message to openai node
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=SET_FEATURE_PROMPT.format(
                    query_related_code = self.user_query_code,
                    user_feature = self.user_feature,
                    related_content = self.related_content,
                    ),
            )
        )

    async def set_possiblly_related_file(self):
        await self.set_focus_files()
        focus_files_dict = self.repo_handler.get_focus_files_content()
        focus_files_str = "\n".join(
            [
                f"{file_path}:\n{file_content}"
                for file_path, file_content in focus_files_dict.items()
            ]
        )
        # add focus files system message to openai node
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=FOCUS_FILE_PROMPT.format(
                    focus_files=focus_files_str,
                ),
            )
        )


    async def understand_codebase(self):
        
        resp = await self.openai_node.chat(
            input=ChatInput(
                model="gpt-4-1106-preview",
                message_text=UNDERSTANDING_CODEBASE_PROMPT.format(
                    format_example=UNDERSTANDING_CODEBASE_TEMPLATE,
                ),
            ),
        )
        understanding = LLMOutputParser.parse_output(resp.message.content)["understanding"]
        undstanding = []
        for file_path, related_code, description in understanding:
            undstanding.append(
                Understanding(
                    file_path=file_path, 
                    related_code = related_code,
                    description=description
                )
            )
        if len(understanding) > 0 :
            self.abstarct = undstanding[0].description
        else:
            self.abstarct = ""
        self.understandings.append(undstanding)

    

    async def set_focus_files(self):
        """
        Set focus files of agent for feature development.
        """
        resp = await self.openai_node.chat(
            input=ChatInput(
                model="gpt-4-1106-preview",
                message_text=FOCUS_FILE_PATH_PROMPT.format(
                    format_example=FOCUS_FILE_PATH_EXAMPLE,
                ),
            ),
        )

        files = LLMOutputParser.parse_output(resp.message.content)["files"]
        for file in files:
            try:
                self.repo_handler.add_focus_file(file)
            except FileNotFoundError:
                logging.warning(f"File {file} does not exist.")

        
    def _init_openai_node(self):
        """
        Initialize OpenAI node.
        Add global system messages.
        """
        self.openai_node = AsyncOpenAINode()

        # software engineer prompt
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=CODEBASE_PROMPT,
            )
        )

    # def add_data_file(self, file_path: Path, type: str):
    #     file_name = file_path.name
    #     file_type = file_path.suffix[1:]

    #     try:
    #         loaded_file = self.file_loader.load_data(name=file_name,
    #                 source_type=file_type,
    #                 source_path=str(file_path))
        
    #         if loaded_file == "":
    #             return False
    #         else:
    #             if type == "pm_spec":
    #                 self.load_pm_spec_from_file(loaded_file)
    #             elif type == "pm_requirement":
    #                 self.load_pm_requirements_from_file(loaded_file)
    #             return True
    #     except ValueError as e:
    #         print(f"Error occurred: {e}")


    # def set_code_base(self, code_base):
    #     self.code_base = code_base
    #     self.openai_node.add_single_message(
    #         Message(
    #             role="system",
    #             content=CODE_BASE_PROMPT.format(
    #                 code_base = self.code_base
    #             ),
    #         )
    #     )
    
    # def load_file_content(self, document_data):
    #     """
    #     Load PM Specification from a given file.
    #     """
    #     # Assuming the document's content is directly the pm_spec
    #     try:
    #         content = document_data[0]
    #         page_content = content.page_content
    #         self.pm_spec = page_content
    #     except ValueError as e:
    #         print(e)

    #     self.openai_node.add_single_message(
    #         Message(
    #             role="system",
    #             content=PM_SPEC_PROMPT.format(
    #                 pm_spec = self.pm_spec
    #             ),
    #         )
    #     )

    # def load_pm_requirements_from_file(self, document_data):
    #     """
    #     Load PM Requirements from a given file.
    #     """
    #     content = document_data[0]
    #     page_content = content.page_content
    #     self.pm_requirements = page_content
        
    #     self.openai_node.add_single_message(
    #         Message(
    #             role="system",
    #             content=PM_REQUIREMENTS_PROMPT.format(
    #                 pm_requirement = self.pm_requirements
    #             ),
    #         )
    #     )


    # Getter and Setter

    def add_focus_file(self, file_path):
        """
        Add file to repo.
        """
        self.repo_handler.add_focus_file(file_path)

    def remove_focus_file(self, file_path):
        """
        Remove file from repo.
        """
        self.repo_handler.remove_focus_file(file_path)

    def get_focus_files(self):
        """
        Get focus files.
        """
        return self.repo_handler.focus_files

    def clear_focus_files(self):
        """
        Clear focus files.
        """
        self.repo_handler.focus_files = {}
    
    def get_understanding(self):
        """
        Get feature implemetation plan.
        """
        return self.understandings

    def set_understanding(self, understanding: list[Understanding]):
        """
        Set feature implementation plan.
        """
        self.understanding = understanding

