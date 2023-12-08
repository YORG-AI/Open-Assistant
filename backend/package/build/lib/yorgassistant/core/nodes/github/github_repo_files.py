import requests
from github import Github
from ..base_node import BaseNode, NodeConfig
from .github_model import (
    RepositoryInput,
    GetSpecificContentFileInput,
    CreateFileInput,
    EditFileInput,
    DeleteFileInput,
)

import os
from dotenv import load_dotenv

load_dotenv()  # This will load variables from .env into the environment

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

repository_node_config = {
    "name": "repository",
    "description": "A node for interacting with GitHub repositories and files.",
    "functions": {
        "get_repository_topics": "Get repository topics.",
        "get_count_of_stars": "Get count of stars.",
        "get_specific_content_file": "Get a specific content file.",
        "create_file": "Create a new file in the repository.",
        "edit_file": "Edit a file in the repository.",
        "delete_file": "Delete a file in the repository.",
        "get_list_of_open_issues": "Get a list of open issues.",
        "get_list_of_code_scanning_alerts": "Get a list of code scanning alerts.",
        "get_all_labels_of_repository": "Get all labels of the repository.",
        "get_contents_of_root_directory": "Get contents of the root directory.",
        "get_all_contents_recursively": "Get all contents recursively.",
        "get_top_10_referrers": "Get top 10 referrers.",
        "get_top_10_popular_contents": "Get top 10 popular contents.",
        "get_clone_and_view_data": "Get clone and view data.",
        "mark_notifications_as_read": "Mark notifications as read.",
    },
}

class GithubNode(BaseNode):
    def __init__(self, token: str):
        self.token = token
        self.g = Github(self.token)  # Initializing the GitHub instance with the token
        super().__init__()

class RepositoryNode(GithubNode):
    config: NodeConfig = NodeConfig(**repository_node_config)

    def __init__(self):
        token = os.environ.get("GITHUB_TOKEN")  # Retrieving the token from the environment
        if not token:
            raise ValueError("GITHUB_TOKEN is not set in the environment.")
        super().__init__(token)

    def get_repository_topics(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            topics = repo.get_topics()
            return topics
        except Exception as e:
            return str(e)

    def get_count_of_stars(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            stars_count = repo.stargazers_count
            return stars_count
        except Exception as e:
            return str(e)

    def get_specific_content_file(self, input: GetSpecificContentFileInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            content_file = repo.get_contents(input.path)
            return content_file.decoded_content.decode()
        except Exception as e:
            return str(e)

    def create_file(self, input: CreateFileInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            repo.create_file(input.path, input.message, input.content)
            return {"status": "File created successfully."}
        except Exception as e:
            return str(e)

    def edit_file(self, input: EditFileInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            content_file = repo.get_contents(input.path)
            repo.update_file(input.path, input.message, input.content, content_file.sha)
            return {"status": "File updated successfully."}
        except Exception as e:
            return str(e)

    def delete_file(self, input: DeleteFileInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            content_file = repo.get_contents(input.path)
            repo.delete_file(input.path, input.message, content_file.sha)
            return {"status": "File deleted successfully."}
        except Exception as e:
            return str(e)

    def get_list_of_open_issues(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            issues = repo.get_issues(state='open')
            return [issue.title for issue in issues]
        except Exception as e:
            return str(e)

    # def get_list_of_code_scanning_alerts(self, input: RepositoryInput):
    #     # Note: This function might require direct API calls as it's not clearly supported in PyGithub at the moment.
    #     raise NotImplementedError("This function is not implemented yet.")

    def get_list_of_code_scanning_alerts(self, input: RepositoryInput):
        try:
            headers = {
                "Authorization": f"token {self.g.get_user().get_access_token().token}", 
                "Accept": "application/vnd.github.v3+json"
            }
            url = f"https://api.github.com/repos/{input.owner}/{input.repo_name}/code-scanning/alerts"
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Will raise an exception for 4xx and 5xx responses

            return response.json()

        except requests.RequestException as e:
            return {"error": str(e)}


    def get_all_labels_of_repository(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            labels = repo.get_labels()
            return [label.name for label in labels]
        except Exception as e:
            return str(e)

    def get_contents_of_root_directory(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            contents = repo.get_contents("")
            return [content.name for content in contents]
        except Exception as e:
            return str(e)

    def get_all_contents_recursively(self, input: RepositoryInput):
        # This will likely be a recursive method since GitHub API doesn't directly support fetching all contents recursively.
        raise NotImplementedError("This function is not implemented yet.")

    def get_top_10_referrers(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            referrers = repo.get_top_referrers()[:10]
            return [{"referrer": referrer.referrer, "count": referrer.count, "uniques": referrer.uniques} for referrer in referrers]
        except Exception as e:
            return str(e)

    def get_top_10_popular_contents(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            popular_contents = repo.get_top_paths()[:10]
            return [{"path": content.path, "count": content.count, "uniques": content.uniques} for content in popular_contents]
        except Exception as e:
            return str(e)

    def get_clone_and_view_data(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            clones = repo.get_clones_traffic()
            views = repo.get_views_traffic()
            return {"clones": clones, "views": views}
        except Exception as e:
            return str(e)

    def mark_notifications_as_read(self, input: RepositoryInput):
        try:
            notifications = self.g.get_user().get_notifications()
            for notification in notifications:
                if notification.repository.full_name == f"{input.owner}/{input.repo_name}":
                    notification.mark_as_read()
            return {"status": "Notifications marked as read."}
        except Exception as e:
            return str(e)