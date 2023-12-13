from ..base_node import BaseNode, NodeConfig
from .github_node import GithubNode
from .github_model import (
    RepositoryInput,
    CreatePullRequestInput,
    GetPullRequestByNumberInput,
    GetPullRequestsByQueryInput,
    ModifyPRCommentInput,
)

github_pullrequest_node_config = {
    "name": "github_pullrequest",
    "description": "A node for interacting with GitHub pull requests.",
    "functions": {
        "create_new_pull_request": "Create a new pull request.",
        "get_pull_request_by_number": "Get pull request by number.",
        "get_pull_requests_by_query": "Get pull requests by query.",
        "modify_pr_comment": "Add and modify pull request comment."
    },
}

class GithubPullRequestNode(GithubNode):
    config: NodeConfig = NodeConfig(**github_pullrequest_node_config)

    def __init__(self):
        super().__init__()

    def create_new_pull_request(self, input: CreatePullRequestInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            pr = repo.create_pull(
                title=input.title,
                body=input.body,
                head=input.head,
                base=input.base
            )
            return pr.number
        except Exception as e:
            return str(e)

    def get_pull_request_by_number(self, input: GetPullRequestByNumberInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            pr = repo.get_pull(input.pr_number)
            return {
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "merged": pr.merged
            }
        except Exception as e:
            return str(e)

    def get_pull_requests_by_query(self, input: GetPullRequestsByQueryInput):
        try:
            search_result = self.g.search_issues(input.query, type="pr")
            prs = [{"number": pr.number, "title": pr.title} for pr in search_result]
            return prs
        except Exception as e:
            return str(e)

    def modify_pr_comment(self, input: ModifyPRCommentInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            pr = repo.get_pull(input.pr_number)
            comment = pr.get_comment(input.comment_id)
            comment.edit(body=input.body)
            return "Comment modified successfully."
        except Exception as e:
            return str(e)
