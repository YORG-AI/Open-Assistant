from abc import ABC, abstractmethod
from enum import Enum

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

    def call(self, **kwargs):
        if self.state == State.IDLE:
            self.state = State.RUNNING
            res = self.func(**kwargs)
            self.state = State.DONE
            return res
        else:
            raise Exception(f"FunctionTool is in state {self.state}, not {State.IDLE}")


class ExampleStage(str, Enum):
    INIT = "init"
    STAGE1 = "stage1"
    STAGE2 = "stage2"
    STAGE3 = "stage3"
    DONE = "done"

class ExampleStatefulToolEntity(BaseToolEntity):
    stage: ExampleStage

    def __init__(self):
        self.stage = ExampleStage.INIT
        self.parameters = {}

    def current_state(self):
        match self.stage:
            case ExampleStage.INIT:
                return State.IDLE
            case ExampleStage.DONE:
                return State.DONE
            case _:
                return State.RUNNING
    
    def call(self, **kwargs):
        match self.stage:
            case ExampleStage.INIT:
                self.stage = ExampleStage.STAGE1
                return ...
            case ExampleStage.STAGE1:
                self.stage = ExampleStage.STAGE2
                return ...
            case ExampleStage.STAGE2:
                self.stage = ExampleStage.STAGE3
                return ...
            case ExampleStage.STAGE3:
                self.stage = ExampleStage.DONE
                return ...

