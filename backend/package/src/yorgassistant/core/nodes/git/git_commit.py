from pathlib import Path
import os
from dotenv import load_dotenv

from .git_base_node import GitBaseNode
from .git_model import (
    GitAddFileInput,
    GitRepositoryInput,
    GitCommitInput,
)
from ..base_node import BaseNode, NodeConfig

load_dotenv()  # This will load variables from .env into the environment

repository_node_config = {
    "name": "git_commit",
    "description": "A node that implements common git operations related to git commit.",
    "functions": {
        "git_add_files": "Add specific file(s) to git index.",
        "git_add_all": "Add all files in directory.",
        "git_commit": "Make a commit with message in the repository.",
        "git_commit_with_author": "Make a commit with message and given author in the repository.",
        "git_add_commit": "Add files and commit (shorthand of git add -A and git commit).",
        "git_reset_all": "Restore the index, undo git add.",
        "get_untracked_files": "Get list of untracked files of current repo",
    },
}


class GitCommitNode(GitBaseNode):
    config: NodeConfig = NodeConfig(**repository_node_config)

    def git_add_files(self, input: GitAddFileInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            for path in input.paths:
                repo.git.add(path)
            return {
                "status": f"Files {input.paths} are added successfully to index of repo {input.path}."
            }
        except Exception as e:
            return str(e)

    def git_add_all(self, input: GitRepositoryInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            repo.git.add(all=True)
            return {
                "status": f"Files {input.paths} are added successfully to index of repo {input.path}."
            }
        except Exception as e:
            return str(e)

    def get_untracked_files(self, input: GitRepositoryInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            return {"untracked": repo.untracked_files}
        except Exception as e:
            return str(e)

    def git_commit(self, input: GitCommitInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            result = repo.git.commit("-m", input.message)
            return {"status": "Git commit success", "message": result.message}
        except Exception as e:
            return str(e)

    def git_commit_with_author(self, input: GitCommitInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            result = repo.git.commit("-m", input.message, author=input.author)
            return {"status": "Git commit success", "message": result.message}
        except Exception as e:
            return str(e)

    def git_add_commit(self, input: GitCommitInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            repo.git.add(all=True)
            result = repo.git.commit("-m", input.message)
            return {"status": "Git commit success", "message": result.message}
        except Exception as e:
            return str(e)

    def git_reset_all(self, input: GitRepositoryInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            repo.git.reset()
            return {"status": f"Successfully reset git index"}
        except Exception as e:
            return str(e)

    def git_reset_files(self, input: GitRepositoryInput):
        repo_path = input.path
        done_reset = []
        try:
            repo = self.g.Repo(repo_path)
            for path in input.paths:
                repo.git.reset(path)
                done_reset.append(path)
            return {
                "status": f"Successfully reset git index",
                "reset_files": done_reset,
            }
        except Exception as e:
            return str(e)
