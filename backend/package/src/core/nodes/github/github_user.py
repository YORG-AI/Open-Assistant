from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.github.github_node import GithubNode
from src.core.nodes.github.github_model import (
    GetUserRepositoriesInput,
    InviteUserToOrgInput
)
from src.utils.router_generator import generate_node_end_points

github_user_node_config = {
    "name": "github_user",
    "description": "A node for interacting with GitHub users.",
    "functions": {
        "get_user_repositories": "Returns the repositories of a user.",
        "invite_user_to_org": "Invites a user to an organization."
    },
}

@generate_node_end_points
class GithubUserNode(GithubNode):
    config: NodeConfig = NodeConfig(**github_user_node_config)

    def __init__(self):
        super().__init__()

    def get_user_repositories(self, input: GetUserRepositoriesInput):
        try:
            user = self.g.get_user(input.username)
            repos = user.get_repos()
            return [{"id": repo.id, "name": repo.name} for repo in repos]
        except Exception as e:
            return str(e)

    def invite_user_to_org(self, input: InviteUserToOrgInput):
        try:
            org = self.g.get_organization(input.org_name)
            org.invite_user(user=input.username)
            return f"User {input.username} invited to organization {input.org_name}."
        except Exception as e:
            return str(e)
