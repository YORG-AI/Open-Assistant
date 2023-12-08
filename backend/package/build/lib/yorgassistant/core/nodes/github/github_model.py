from pydantic import BaseModel

# Base input for most repository-related functions
class RepositoryInput(BaseModel):
    owner: str
    repo_name: str

# Specific file content
class GetSpecificContentFileInput(RepositoryInput):
    path: str

# Create a new file
class CreateFileInput(RepositoryInput):
    path: str
    message: str
    content: str  # Content should be base64 encoded.

# Edit a file
class EditFileInput(CreateFileInput):
    sha: str

# Delete a file
class DeleteFileInput(RepositoryInput):
    path: str
    message: str
    sha: str

# Base input for getting an issue
class GetIssueInput(BaseModel):
    owner: str
    repo_name: str
    issue_number: int

# Create comment on an issue
class CreateIssueCommentInput(BaseModel):
    owner: str
    repo_name: str
    issue_number: int
    comment_content: str

# Base input for creating an issue
class CreateIssueInput(BaseModel):
    owner: str
    repo_name: str
    title: str

# Create an issue with body
class CreateIssueWithBodyInput(CreateIssueInput):
    body: str

# Create an issue with labels
class CreateIssueWithLabelsInput(CreateIssueInput):
    labels: list[str]

# Create an issue with assignee
class CreateIssueWithAssigneeInput(CreateIssueInput):
    assignee: str

# Create an issue with milestone
class CreateIssueWithMilestoneInput(CreateIssueInput):
    milestone_number: int  # Milestone number

class CloseAllIssuesInput(BaseModel):
    owner: str
    repo_name: str

# Input for creating a commit status check
class CreateCommitStatusCheckInput(BaseModel):
    owner: str
    repo_name: str
    sha: str
    state: str  # error, failure, pending, or success
    target_url: str
    description: str
    context: str

# Input for getting the commit date
class GetCommitDateInput(BaseModel):
    owner: str
    repo_name: str
    sha: str

# Base input for most branch-related functions
class RepositoryInput(BaseModel):
    owner: str
    repo_name: str

# Input for getting a specific branch
class GetBranchInput(RepositoryInput):
    branch_name: str

# Input for getting the HEAD commit of a branch
class GetBranchHeadCommitInput(GetBranchInput):
    pass

# Input for getting the protection status of a branch
class GetBranchProtectionStatusInput(GetBranchInput):
    pass

# Input for seeing the required status checks of a branch
class GetBranchRequiredStatusChecksInput(GetBranchInput):
    pass   


# Base input for most pull request-related functions
class RepositoryInput(BaseModel):
    owner: str
    repo_name: str

# Input for creating a new pull request
class CreatePullRequestInput(RepositoryInput):
    title: str
    body: str
    head: str  # The name of the branch where your changes are implemented
    base: str  # The name of the branch you want the changes pulled into

# Input for getting a pull request by number
class GetPullRequestByNumberInput(RepositoryInput):
    pr_number: int

# Input for getting pull requests by query
class GetPullRequestsByQueryInput(RepositoryInput):
    query: str

# Input for adding and modifying a pull request comment
class ModifyPRCommentInput(RepositoryInput):
    pr_number: int
    comment_id: int
    body: str

# Base input for most milestone-related functions
class RepositoryInput(BaseModel):
    owner: str
    repo_name: str

# Input for getting a specific milestone
class GetMilestoneInput(RepositoryInput):
    milestone_number: int

# Input for creating a milestone
class CreateMilestoneInput(RepositoryInput):
    title: str

# Input for creating a milestone with state and description
class CreateMilestoneWithDetailsInput(CreateMilestoneInput):
    state: str  # Either "open", "closed", or "all"
    description: str

# Base input for getting repositories of a user
class GetUserRepositoriesInput(BaseModel):
    username: str

# Input for inviting a user to an organization
class InviteUserToOrgInput(BaseModel):
    org_name: str
    username: str

# Base input for all search operations
class BaseSearchInput(BaseModel):
    query: str

# Extended search models for specific search types
class SearchCodeInput(BaseSearchInput):
    sort: str = None
    order: str = None

class SearchCommitsInput(BaseSearchInput):
    sort: str = None
    order: str = None

class SearchIssuesAndPRsInput(BaseSearchInput):
    sort: str = None
    order: str = None

class SearchLabelsInput(BaseSearchInput):
    repository_id: int
    sort: str = None
    order: str = None

class SearchRepositoriesInput(BaseSearchInput):
    sort: str = None
    order: str = None

class SearchTopicsInput(BaseSearchInput):
    sort: str = None
    order: str = None

class SearchUsersInput(BaseSearchInput):
    sort: str = None
    order: str = None