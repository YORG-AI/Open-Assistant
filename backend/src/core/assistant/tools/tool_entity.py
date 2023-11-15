from abc import ABC, abstractmethod
from enum import Enum
from pydantic import BaseModel, Field

import os
import yaml

class State(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    DONE = "done"

class BaseToolEntity(ABC):
    @abstractmethod
    def current_state(self):
        pass
    
    @abstractmethod
    def call(self, **kwargs):
        pass

    @abstractmethod
    def need_llm_generate_parameters(self) -> bool:
        pass

    @abstractmethod
    def need_llm_generate_response(self) -> bool:
        pass

    @abstractmethod
    def is_stateful(self) -> bool:
        pass

class FunctionToolEntity(BaseToolEntity):
    parameters: dict[str, any]
    func: callable

    def __init__(self, func: callable):
        self.func = func
        
        self.state = State.IDLE
        self.parameters = {}

    def current_state(self):
        return self.state
    
    def need_llm_generate_parameters(self) -> bool:
        return True

    def need_llm_generate_response(self) -> bool:
        return True

    def is_stateful(self) -> bool:
        return False

    def call(self, **kwargs):
        if self.state == State.IDLE:
            self.state = State.RUNNING
            res = self.func(**kwargs)
            self.state = State.DONE
            return res
        else:
            raise Exception(f"FunctionTool is in state {self.state}, not {State.IDLE}")





