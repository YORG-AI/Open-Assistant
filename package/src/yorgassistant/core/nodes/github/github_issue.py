from ..base_node import BaseNode, NodeConfig
from .github_node import GithubNode
from .github_model import (
    GetIssueInput,
    CreateIssueCommentInput,
    CreateIssueInput,
    CreateIssueWithBodyInput,
    CreateIssueWithLabelsInput,
    CreateIssueWithAssigneeInput,
    CreateIssueWithMilestoneInput,
    CloseAllIssuesInput,
)

from github import Github

github_issues_node_config = {
    "name": "github_issues",
    "description": "A node for interacting with GitHub issues.",
    "functions": {
        "get_issue": "Get issue details.",
        "create_issue_comment": "Create a comment on an issue.",
        "create_issue": "Create a new issue.",
        "create_issue_with_body": "Create a new issue with a body.",
        "create_issue_with_labels": "Create a new issue with labels.",
        "create_issue_with_assignee": "Create a new issue with an assignee.",
        "create_issue_with_milestone": "Create a new issue with a milestone.",
        "close_all_issues": "Close all open issues in a repository.",
    },
}


class GithubIssuesNode(GithubNode):
    config: NodeConfig = NodeConfig(**github_issues_node_config)

    def __init__(self):
        super().__init__()  # This will call the GithubNode's __init__ method and set up the token and GitHub instance

    def get_issue(self, input: GetIssueInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            issue = repo.get_issue(number=input.issue_number)
            return issue.title, issue.body
        except Exception as e:
            return str(e)

    def create_issue_comment(self, input: CreateIssueCommentInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            issue = repo.get_issue(number=input.issue_number)
            comment = issue.create_comment(input.comment_content)
            return f"Comment created with ID: {comment.id}"
        except Exception as e:
            return str(e)

    def create_issue(self, input: CreateIssueInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            issue = repo.create_issue(title=input.title)
            return f"Issue created with title: {issue.title} and ID: {issue.id}"
        except Exception as e:
            return str(e)

    def create_issue_with_body(self, input: CreateIssueWithBodyInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            issue = repo.create_issue(title=input.title, body=input.body)
            return f"Issue created with title: {issue.title}, ID: {issue.id}, and body: {issue.body}"
        except Exception as e:
            return str(e)

    def create_issue_with_labels(self, input: CreateIssueWithLabelsInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            labels = [repo.get_label(label_name) for label_name in input.labels]
            issue = repo.create_issue(title=input.title, labels=labels)
            return f"Issue created with title: {issue.title}, ID: {issue.id}, and labels: {[label.name for label in issue.labels]}"
        except Exception as e:
            return str(e)

    def create_issue_with_assignee(self, input: CreateIssueWithAssigneeInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            issue = repo.create_issue(title=input.title, assignee=input.assignee)
            return f"Issue '{issue.title}' created with assignee '{input.assignee}' successfully."
        except Exception as e:
            return str(e)

    def create_issue_with_milestone(self, input: CreateIssueWithMilestoneInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            # Retrieve the milestone by its number
            milestone = repo.get_milestone(number=input.milestone_number)
            # Create an issue with the milestone
            issue = repo.create_issue(
                title=input.title, body=input.body, milestone=milestone
            )
            return {
                "status": "Issue created successfully with milestone.",
                "issue_number": issue.number,
            }
        except Exception as e:
            return str(e)

    def close_all_issues(self, input: CloseAllIssuesInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            open_issues = repo.get_issues(state="open")
            for issue in open_issues:
                issue.edit(state="closed")
            return "All open issues closed successfully."
        except Exception as e:
            return str(e)
