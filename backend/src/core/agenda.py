from typing import List
from enum import Enum
from pydantic import BaseModel, Field
# from .workflow import Workflow
from .org import Org
from .event import Event
import time


# class Agenda(BaseModel):
#     id: str = Field(default="agenda1", description="用户目标的编号")
#     creation_time: int = Field(default=int(time.time()), description="创建时间")
#     title: str = Field(default="", description="用户目标的题目")
#     requirement: str = Field(default="", description="用户目标的描述")
#     org: Org = Field(default_factory=Org, description="完成目标需要的团队")
#     workflows: List[Workflow] = Field(default_factory=list, description="完成目标需要的任务&排序")
#     status_summary: str = Field(default="", description="当前的完成情况")
#     event_history: List[Event] = Field(default_factory=list, description="事件列表")
