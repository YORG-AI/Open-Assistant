from abc import ABC, abstractmethod
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    name: str = Field(description="Agent 名称")


class BaseAgent(ABC):
    AgentConfig: AgentConfig

