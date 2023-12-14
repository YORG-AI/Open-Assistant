import json
import logging

from typing import Optional
from pydantic import BaseModel, Field
from pathlib import Path

from ..base_agent import BaseAgent, AgentConfig
from .software_engineer_prompt import *
from .repo_manager import RepoManager, FileAction

from ...nodes import (
    DocumentLoaderNode,
    OpenAINode,
    ChatInput,
    Message,
    GitRepoNode,
    GitRemoteRepositoryInput,
)

from ....utils.output_parser import LLMOutputParser


REPO_PATH = Path("src/data/git")


software_engineer_config = {
    "name": "software_engineer",
    "description": "A agent for software engineer.",
}


class Plan(BaseModel):
    action: str = Field(description="Plan action.")
    file_path: str = Field(description="File path for action.")
    description: str = Field(description="Description for action.")

    def to_markdown(self):
        action_str = self.action
        match self.action:
            case "add":
                action_str = f"**Add** a new file at {self.file_path}"
            case "remove":
                action_str = f"**Remove** file at {self.file_path}"
            case "modify":
                action_str = f"**Modify** file at {self.file_path}"

        return f"""
- {action_str}
- {self.description}
"""

    def __str__(self):
        action_str = ""
        match self.action:
            case "add":
                action_str = f"Add a new file at {self.file_path}"
            case "remove":
                action_str = f"Remove file at {self.file_path}"
            case "modify":
                action_str = f"Modify file at {self.file_path}"

        return action_str


class SoftwareEngineerAgent(BaseAgent):
    config: AgentConfig = AgentConfig(**software_engineer_config)

    def __init__(self):
        self.document_loader_node = DocumentLoaderNode()
        self.feature_description = ""
        self.plans: list[Plan] = []
        self.repo_url = ""
        self.model_name = "gpt-4-1106-preview"
        self.git_node = GitRepoNode()
        self.repo_manager: Optional[RepoManager] = None
        self.file_actions: list[FileAction] = []
        self._init_openai_node()

    def set_repo_url(self, repo_url: str):
        """
        Set repo url.
        """
        self.repo_url = repo_url
        repo_path = REPO_PATH / Path(repo_url).name
        self.git_node.git_clone(
            input=GitRemoteRepositoryInput(
                url=repo_url,
                path=repo_path,
            )
        )
        self.repo_manager = RepoManager(repo_path)

        # repo structure prompt
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=REPO_STRUCTURE_PROMPT.format(
                    file_tree=self.repo_manager.file_tree_str,
                ),
            )
        )

    def set_local_repo(self, repo_name: str):
        """
        Set local repo path.
        """
        repo_path = REPO_PATH / repo_name
        self.repo_manager = RepoManager(repo_path)

        # repo structure prompt
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=REPO_STRUCTURE_PROMPT.format(
                    file_tree=self.repo_manager.file_tree_str,
                ),
            )
        )

    def set_feature_description(self, feature_description: str):
        """
        Set feature description.
        """
        # add feature description system message to openai node
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=FEATURE_PROMPT.format(feature_description=feature_description),
            )
        )

        self.feature_description = feature_description

    def set_focus_files(self):
        """
        Set focus files of agent for feature development.
        """
        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.model_name,
                message_text=FOCUS_FILE_PATH_PROMPT.format(
                    format_example=FOCUS_FILE_PATH_EXAMPLE,
                ),
            ),
        )

        files = LLMOutputParser.parse_output(resp.message.content)["files"]
        for file in files:
            try:
                self.repo_manager.add_focus_file(file)
            except FileNotFoundError:
                logging.warning(f"File {file} does not exist.")

    def design_plan(self):
        """
        Design high level plan for feature development.
        """
        if len(self.repo_manager.focus_files) == 0:
            logging.warning("No focus files are set. Please set focus files first.")

        focus_files_dict = self.repo_manager.get_focus_files_content()
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

        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.model_name,
                message_text=PLAN_PROMPT.format(
                    format_example=PLAN_FORMAT_EXAMPLE,
                ),
            ),
        )

        plan = LLMOutputParser.parse_output(resp.message.content)["plan"]
        for action, file_path, description in plan:
            self.plans.append(
                Plan(
                    action=action.lower(), file_path=file_path, description=description
                )
            )

    def implement(self):
        """
        Implement plan, generate a list of file actions.
        """
        for plan in self.plans:
            match plan.action:
                case "add":
                    file_action = self._add_file(plan)
                case "remove":
                    file_action = self._remove_file(plan)
                case "modify":
                    file_action = self._modify_file(plan)
                case _:
                    raise ValueError(f"Unknown action {plan.action}.")

            self.file_actions.append(file_action)
            yield file_action

    def apply_file_action(self):
        self.repo_manager.apply_file_actions(self.file_actions)
        self.file_actions = []

    def _add_file(self, plan: Plan):
        assert plan.action == "add"

        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.model_name,
                message_text=ADD_FILE_PROMPT.format(
                    file_path=plan.file_path,
                    action_description=plan.description,
                ),
            )
        )

        content = resp.message.content

        while content.startswith('"') and content.endswith('"'):
            content = content[1:-1]

        return FileAction(
            action="add",
            file_path=plan.file_path,
            content=content,
        )

    def _remove_file(self, plan: Plan):
        return FileAction(
            action="remove",
            file_path=plan.file_path,
        )

    def _modify_file(self, plan: Plan):
        assert plan.action == "modify"

        resp = self.openai_node.chat(
            input=ChatInput(
                model=self.model_name,
                message_text=MODIFY_FILE_PROMPT.format(
                    file_path=plan.file_path,
                    file_content=self.repo_manager.get_file_content(
                        plan.file_path, limit_lines=5000
                    ),
                    action_description=plan.description,
                ),
            )
        )

        content = resp.message.content

        while content.startswith('"') and content.endswith('"'):
            content = content[1:-1]

        return FileAction(
            action="modify",
            file_path=plan.file_path,
            content=content,
        )

    def _init_openai_node(self):
        """
        Initialize OpenAI node.
        Add global system messages.
        """
        self.openai_node = OpenAINode()

        # software engineer prompt
        self.openai_node.add_single_message(
            Message(
                role="system",
                content=SDE_PROMPT,
            )
        )

    # Getter and Setter

    def add_focus_file(self, file_path):
        """
        Add file to repo.
        """
        self.repo_manager.add_focus_file(file_path)

    def remove_focus_file(self, file_path):
        """
        Remove file from repo.
        """
        self.repo_manager.remove_focus_file(file_path)

    def get_focus_files(self):
        """
        Get focus files.
        """
        return self.repo_manager.focus_files

    def clear_focus_files(self):
        """
        Clear focus files.
        """
        self.repo_manager.focus_files = {}

    def add_plan(self, plan: Plan):
        """
        Add plan to implement plan.
        """
        self.plans.append(plan)

    def remove_plan(self, plan: Plan):
        """
        Remove plan from implement plan.
        """
        self.plans.remove(plan)

    def get_plan(self):
        """
        Get feature implemetation plan.
        """
        return self.plans

    def set_plans(self, plans: list[Plan]):
        """
        Set feature implementation plan.
        """
        self.plans = plans

    def get_file_actions(self):
        """
        Get file actions.
        """
        return self.file_actions
