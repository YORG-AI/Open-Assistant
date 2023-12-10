import git
from ..base_node import BaseNode


class GitBaseNode(BaseNode):
    def __init__(self):
        # if len(args) > 0:
        #     self.repo_path = args[0]
        # else:
        #     if 'path' not in kwargs:
        #         raise ValueError("Missing argument: path to git repo at GitBaseNode().")
        #     self.repo_path = kwargs.get('path', '')
        # if type(self.repo_path) is not str:
        #     raise ValueError("Type error: argument path must be str.")

        self.g = git
        self.r = git.Repo
        super().__init__()
