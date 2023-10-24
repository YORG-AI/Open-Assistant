from typing import Dict, List
from pydantic import BaseModel, Field
from enum import Enum
import time


class Org(BaseModel):
    id: str = Field(default="org1")
    creation_time: int = Field(default=int(time.time()))
    name: str = Field(default="org")
    description: str = Field(default="this is an org")


class Event(BaseModel):
    pass
