from src.core.nodes.base_node import BaseNode, NodeConfig
from .github_node import GithubNode
from .github_model import (
    RepositoryInput,
    GetMilestoneInput,
    CreateMilestoneInput,
    CreateMilestoneWithDetailsInput,
)

github_milestone_node_config = {
    "name": "github_milestone",
    "description": "A node for interacting with GitHub milestones.",
    "functions": {
        "get_milestone_list": "Get list of milestones.",
        "get_milestone": "Get a specific milestone.",
        "create_milestone": "Create a new milestone.",
        "create_milestone_with_details": "Create a milestone with state and description.",
    },
}


class GithubMilestoneNode(GithubNode):
    config: NodeConfig = NodeConfig(**github_milestone_node_config)

    def __init__(self):
        super().__init__()

    def get_milestone_list(self, input: RepositoryInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            milestones = repo.get_milestones()
            return [{"number": m.number, "title": m.title} for m in milestones]
        except Exception as e:
            return str(e)

    def get_milestone(self, input: GetMilestoneInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            milestone = repo.get_milestone(input.milestone_number)
            return {
                "number": milestone.number,
                "title": milestone.title,
                "description": milestone.description,
                "state": milestone.state,
            }
        except Exception as e:
            return str(e)

    def create_milestone(self, input: CreateMilestoneInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            milestone = repo.create_milestone(title=input.title)
            return milestone.number
        except Exception as e:
            return str(e)

    def create_milestone_with_details(self, input: CreateMilestoneWithDetailsInput):
        try:
            repo = self.g.get_repo(f"{input.owner}/{input.repo_name}")
            milestone = repo.create_milestone(
                title=input.title, state=input.state, description=input.description
            )
            return milestone.number
        except Exception as e:
            return str(e)
