from enum import Enum
import time
from typing import Dict, List

from pydantic import BaseModel, Field

# from .agenda import Agenda


# class InterventionType(str, Enum):
#     AUTO = "AUTO"
#     SEMI_AUTO = "SEMI_AUTO"
#     MANUAL = "MANUAL"


# class OrgSelection(str, Enum):
#     PREBUILT = "PREBUILT"
#     PUBLIC = "PUBLIC"
#     LLM = "LLM"
#     CUSTOM = "CUSTOM"


# class WebAccess(str, Enum):
#     BLOCK = "BLOCK"
#     FULL = "FULL"
#     READ_ONLY = "READ_ONLY"


# class UserInput(BaseModel):
#     user_id: str = Field(default="admin", description="用户的编号")
#     session_id: str = Field(default="1", description="当前session的编号")
#     creation_time: int = Field(default=int(time.time()), description="创建时间")
#     intervention_type: InterventionType = Field(
#         default=InterventionType.AUTO, description="人工干预的程度"
#     )
#     reiteration_cycle: int = Field(
#         default=3, description="多少次失败会trigger人工干预（适用于semi-auto）"
#     )
#     token_budget: int = Field(default=4096, description="上限消耗")
#     org_selection: OrgSelection = Field(
#         default=OrgSelection.PREBUILT, description="如何组建团队"
#     )
#     web_access: WebAccess = Field(
#         default=WebAccess.BLOCK, description="是否允许agents联网（读+写/只读/不许联网）"
#     )
#     memory_access: bool = Field(default=False, description="是否访问Agents以往的记忆")
#     agenda: Agenda = Field(default_factory=Agenda, description="用户想完成什么目标")

#     def start_project(self, user_id: str, session_id: str, requirement: str):
#         self.user_id = user_id
#         self.session_id = session_id
#         self.creation_time = int(time.time())

#         self.agenda.requirement = requirement
#         self.agenda.status_summary = "STARTED"
