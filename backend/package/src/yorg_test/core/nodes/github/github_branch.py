from ..base_node import BaseNode, NodeConfig
from .github_node import GithubNode
from .github_model import (
    RepositoryInput,
    GetBranchInput,
    GetBranchHeadCommitInput,
    GetBranchProtectionStatusInput,
    GetBranchRequiredStatusChecksInput,
)

github_branch_node_config = {
    "name": "github_branch",
    "description": "A node for interacting with GitHub branches.",
    "functions": {
        "get_list_of_branches": "Get a list of branches.",
        "get_branch": "Get a specific branch.",
        "get_head_commit_of_branch": "Get the HEAD commit of a branch.",
        "get_protection_status_of_branch": "Get the protection status of a branch.",
        "see_required_status_checks_of_branch": "See the required status checks of a branch.",
    },
}


class GithubBranchNode(GithubNode):
    config: NodeConfig = NodeConfig(**github_branch_node_config)

    def __init__(self):
        super().__init__()

    def get_list_of_branches(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            branches = repo.get_branches()
            return [branch.name for branch in branches]
        except Exception as e:
            return str(e)

    def get_branch(self, input: GetBranchInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            branch = repo.get_branch(branch=input.branch_name)
            return branch.name
        except Exception as e:
            return str(e)

    def get_head_commit_of_branch(self, input: GetBranchHeadCommitInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            branch = repo.get_branch(branch=input.branch_name)
            return branch.commit.sha
        except Exception as e:
            return str(e)

    def get_protection_status_of_branch(self, input: GetBranchProtectionStatusInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            protection = repo.get_branch_protection(branch=input.branch_name)
            return protection.url
        except Exception as e:
            return str(e)

    def see_required_status_checks_of_branch(
        self, input: GetBranchRequiredStatusChecksInput
    ):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            protection = repo.get_branch_protection(branch=input.branch_name)
            return protection.required_status_checks
        except Exception as e:
            return str(e)
