from ..base_node import BaseNode, NodeConfig
from .git_base_node import GitBaseNode
from .git_model import (
    GitRepositoryInput,
    GitRemoteRepositoryInput,
    GitConfigInput,
    GitConfigReaderInput,
)

import os
from dotenv import load_dotenv

load_dotenv()  # This will load variables from .env into the environment

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

repository_node_config = {
    "name": "git_repo",
    "description": "A node that implements common repo-level git operations.",
    "functions": {
        "git_init": "Initialize a git repository at given dir path.",
        "git_clone": "Create a new file in the repository.",
        "git_fetch": "Delete a file in the repository.",
        "git_get_config": "Get repo config.",
        "git_config": "Set the config for repo.",
        "git_config_global": "Set global git config for repo",
        "is_dirty": "Return true if repo has untracked file or index has changed.",
    },
}


class GitRepoNode(GitBaseNode):
    config: NodeConfig = NodeConfig(**repository_node_config)

    def __init__(self):
        super().__init__()

    # setters, updaters
    def git_init(self, input: GitRepositoryInput):
        try:
            repo_path = input.path
            self.r.init(repo_path)  # raise NoSuchPathError if path doesn't exist
            return {"status": "Repo initialized successfully."}
        except Exception as e:
            return str(e)

    def git_clone(self, input: GitRemoteRepositoryInput):
        try:
            repo_url = input.url
            repo_path = input.path
            self.r.clone_from(repo_url, repo_path)
            return {"status": "Repo cloned successfully."}
        except Exception as e:
            return str(e)

    def git_fetch(self, input: GitRepositoryInput):
        try:
            repo_path = input.path
            repo = self.g.Repo(repo_path)
            for remote in repo.remotes:
                remote.fetch()
        except Exception as e:
            return str(e)

    def git_get_config(self, input: GitConfigReaderInput):
        try:
            repo_path = input.path
            repo = self.g.Repo(repo_path)
            keys = input.keys
            reader = repo.config_reader(config_level="repository")
            res = []
            for k in keys:
                kk = k.split(".")
                if len(kk) < 2:
                    raise ValueError("Git config key should have section.option format")
                section, option = k
                res.append(reader.get_value(section, option))
            return {"status": "Git local config set successfully."}
        except Exception as e:
            return str(e)

    def git_config(self, input: GitConfigInput):
        try:
            repo_path = input.path
            repo = self.g.Repo(repo_path)
            config = input.config
            writer = repo.config_writer(config_level="repository")
            for k, v in config.items():
                kk = k.split(".")
                if len(kk) < 2:
                    raise ValueError("Git config key should have section.option format")
                section, option = kk
                writer.set_value(section, option, v)
            writer.release()
            return {"status": "Git local config set successfully."}
        except Exception as e:
            return str(e)

    def git_config_global(self, input: GitConfigInput):
        try:
            repo_path = "~"
            repo = self.g.Repo(repo_path)
            config = input.config
            w = repo.config_writer(config_level="global")
            for k, v in config.items():
                kk = k.split(".")
                if len(kk) < 2:
                    raise ValueError("Git config key should have section.option format")
                section, option = kk
                w.set_value(section, option, v)
            w.release()
            return {"status": "Git local config set successfully."}
        except Exception as e:
            return str(e)

    def is_dirty(self, input: GitRepositoryInput):
        try:
            repo_path = input.path
            repo = self.g.Repo(repo_path)
            return {"dirty": repo.is_dirty(untracked_files=True)}
        except Exception as e:
            return str(e)
