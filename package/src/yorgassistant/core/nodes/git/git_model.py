from pydantic import BaseModel
from pathlib import Path

# Base input for most repository-related functions
class GitRepositoryInput(BaseModel):
    path: str


class GitRemoteRepositoryInput(BaseModel):
    url: str
    path: Path


class GitConfigInput(GitRepositoryInput):
    config: dict[str, str]  # key-value pair of config strings


# key shape: section.key
# value shape: value
# use this config as if you're running the command git config section.key "value"


class GitConfigReaderInput(GitRepositoryInput):
    keys: list[str]


class GitFileInput(BaseModel):
    path: str


class GitAddFileInput(GitRepositoryInput):
    paths: list[str]


class GitCommitInput(GitRepositoryInput):
    message: str
    author: str


class GitResetInput(GitRepositoryInput):
    paths: list[str]


class GitBranchInput(GitRepositoryInput):
    branch_name: str


class GitLogInput(GitRepositoryInput):
    format_options: list[str]

class GitPullInput(GitRepositoryInput):
    remote: str

class GitPushInput(GitRepositoryInput):
    remote: str
