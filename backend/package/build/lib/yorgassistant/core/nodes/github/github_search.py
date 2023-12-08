from ..base_node import BaseNode, NodeConfig
from .github_node import GithubNode
from .github_model import (
    SearchCodeInput,
    SearchCommitsInput,
    SearchIssuesAndPRsInput,
    SearchLabelsInput,
    SearchRepositoriesInput,
    SearchTopicsInput,
    SearchUsersInput,
)

github_search_node_config = {
    "name": "github_search",
    "description": "A node for searching various entities on GitHub.",
    "functions": {
        "search_code": "Search code.",
        "search_commits": "Search commits.",
        "search_issues_and_prs": "Search issues and pull requests.",
        "search_labels": "Search labels.",
        "search_repositories": "Search repositories.",
        "search_topics": "Search topics.",
        "search_users": "Search users.",
    },
}


class GithubSearchNode(GithubNode):
    config: NodeConfig = NodeConfig(**github_search_node_config)

    def __init__(self):
        super().__init__()

    def search_code(self, input: SearchCodeInput):
        try:
            result = self.g.search_code(
                query=input.query, sort=input.sort, order=input.order
            )
            return [{"name": item.name, "path": item.path} for item in result]
        except Exception as e:
            return str(e)

    def search_commits(self, input: SearchCommitsInput):
        try:
            result = self.g.search_commits(
                query=input.query, sort=input.sort, order=input.order
            )
            return [
                {"sha": item.sha, "message": item.commit.message} for item in result
            ]
        except Exception as e:
            return str(e)

    def search_issues_and_prs(self, input: SearchIssuesAndPRsInput):
        try:
            result = self.g.search_issues(
                query=input.query, sort=input.sort, order=input.order
            )
            return [{"number": item.number, "title": item.title} for item in result]
        except Exception as e:
            return str(e)

    def search_labels(self, input: SearchLabelsInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            labels = repo.get_labels()
            return [
                {"id": label.id, "name": label.name}
                for label in labels
                if input.query.lower() in label.name.lower()
            ]
        except Exception as e:
            return str(e)

    def search_repositories(self, input: SearchRepositoriesInput):
        try:
            result = self.g.search_repositories(
                query=input.query, sort=input.sort, order=input.order
            )
            return [{"full_name": repo.full_name} for repo in result]
        except Exception as e:
            return str(e)

    def search_topics(self, input: SearchTopicsInput):
        try:
            result = self.g.search_topics(
                query=input.query, sort=input.sort, order=input.order
            )
            return [{"name": topic.name} for topic in result]
        except Exception as e:
            return str(e)

    def search_users(self, input: SearchUsersInput):
        try:
            result = self.g.search_users(
                query=input.query, sort=input.sort, order=input.order
            )
            return [{"login": user.login, "name": user.name} for user in result]
        except Exception as e:
            return str(e)
