from github import Github
from ..base_node import BaseNode
import os

class GithubNode(BaseNode):
    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN")  # Retrieving the token from the environment
        if not self.token:
            raise ValueError("GITHUB_TOKEN is not set in the environment.")
        self.g = Github(self.token)  # Initializing the GitHub instance with the token
        super().__init__()
