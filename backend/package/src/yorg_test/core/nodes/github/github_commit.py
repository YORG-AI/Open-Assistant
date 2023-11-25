from ..base_node import BaseNode, NodeConfig
from .github_node import GithubNode
from .github_model import (
    CreateCommitStatusCheckInput,
    GetCommitDateInput,
)

from datetime import datetime

github_commit_node_config = {
    "name": "github_commit",
    "description": "A node for interacting with GitHub commits.",
    "functions": {
        "create_commit_status_check": "Create a status check for a commit.",
        "get_commit_date": "Get the date of a commit.",
    },
}


class GithubCommitNode(GithubNode):
    config: NodeConfig = NodeConfig(**github_commit_node_config)

    def __init__(self):
        super().__init__()

    def create_commit_status_check(self, input: CreateCommitStatusCheckInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            commit = repo.get_commit(sha=input.sha)
            status = commit.create_status(
                state=input.state,
                target_url=input.target_url,
                description=input.description,
                context=input.context,
            )
            return {"status": "Status check created successfully.", "url": status.url}
        except Exception as e:
            return str(e)

    def get_commit_date(self, input: GetCommitDateInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            commit = repo.get_commit(sha=input.sha)
            date = commit.commit.committer.date
            return date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            return str(e)
