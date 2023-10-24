
from enum import Enum
from pydantic import BaseModel, Field

# from .assignment import Assignment
from .memory import Memory


# class Role(BaseModel):
#     class RoleType(str, Enum):
#         FRONTEND_DEVELOPER = "frontend developer"
#         BACKEND_DEVELOPER = "backend developer"
#         FULLSTACK_DEVELOPER = "fullstack developer"
#         REASERCHER = "researcher"
#         OTHER = "other"

#     type: RoleType = Field(default=RoleType.OTHER, description="角色类型")
#     description: str = Field(default="", description="角色信息")
#     goals: str = Field(default="", description="角色目标")

# class Agent(BaseModel):
#     name: str = Field(default="", description="Agent 名称")
#     background: str = Field(default="", description="Agent 背景信息")
#     role: list[Role] = Field(default=[], description="Agent 角色")
#     memory: list[Memory] = Field(default=[], description="Agent 能访问的记忆")

    

