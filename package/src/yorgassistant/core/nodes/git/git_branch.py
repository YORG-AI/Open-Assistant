from git import Commit

from ..base_node import BaseNode, NodeConfig
from .git_base_node import GitBaseNode
from .git_model import (
    GitRepositoryInput,
    GitBranchInput,
    GitPullInput,
    GitPushInput,
)

repository_node_config = {
    "name": "git_branch_node",
    "description": "A node that implements common git branch operations.",
    "functions": {
        "get_git_branch_list": "Add specific file(s) to git index.",
        "git_log_raw": "Get raw output string of git log.",
        "git_log": "Get list of commit info.",
        "git_log_commit_topk": "Get list of commit info, max traceback topk.",
        "git_switch_branch": "Switch to another branch.",
        "git_pull": "Git pull.",
        "git_push": "Git push.",
        "git_pull_remote": "Git pull with specified remote",
        "git_push_remote": "Git push with specified remote",
    },
}


def formatGitCommit(commit: Commit):
    return {
        "repo": str(commit.repo),
        "hexsha": commit.hexsha,
        "author": commit.author,
        "message": commit.message,
        "summary": commit.summary,  # first line of message
        "datetime": commit.committed_datetime,
    }


class GitBranchNode(GitBaseNode):
    config: NodeConfig = NodeConfig(**repository_node_config)

    def get_git_branch_list(self, input: GitRepositoryInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            repo_heads_names = [h.name for h in repo.heads]
            return {"branch": repo_heads_names}
        except Exception as e:
            return str(e)

    def git_switch_branch(self, input: GitBranchInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            repo.git.checkout(input.branch_name)
            return {"status": f"Successfully checkout git branch {input.branch_name}."}
        except Exception as e:
            return str(e)

    def git_log_raw(self, input: GitRepositoryInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            log_content = repo.git.log()
            return {"log": log_content}
        except Exception as e:
            return str(e)

    def git_log(self, input: GitRepositoryInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            log_content = repo.git.log()
            return {"log": log_content}
        except Exception as e:
            return str(e)

    def git_log_commit_topk(self, input: GitRepositoryInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            log_content = repo.git.log()
            return {"log": log_content}
        except Exception as e:
            return str(e)

    def git_pull(self, input: GitPullInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            result = repo.git.pull()
            return {"status": "Git pull success", "result": result}
        except Exception as e:
            return str(e)

    def git_pull_remote(self, input: GitPullInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            result = repo.git.push(input.remote)
            return {"status": "Git pull success", "result": result}
        except Exception as e:
            return str(e)

    def git_push(self, input: GitPushInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            result = repo.git.push()
            return {"status": "Git pull success", "result": result}
        except Exception as e:
            return str(e)

    def git_push_remote(self, input: GitPushInput):
        repo_path = input.path
        try:
            repo = self.g.Repo(repo_path)
            result = repo.git.push(input.remote)
            return {"status": "Git pull success", "result": result}
        except Exception as e:
            return str(e)
