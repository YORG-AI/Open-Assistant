from enum import Enum

from src.core.agents.software_engineer.software_engineer import SoftwareEngineerAgent

from .tool_entity import *


class Stage(str, Enum):
    INIT = "init"
    WAIT_FOR_GIT_REPO = "wait_for_git_repo"
    SET_GIT_REPO_DONE = "set_git_repo_done"
    WAIT_FOR_FEATURE = "wait_for_feature"
    SET_FEATURE_DONE = "set_feature_done"
    MODIFY_FOCUS_FILES = "modify_focus_files"
    WAIT_FOR_MODIFY_FOCUS_FILES = "wait_for_modify_focus_files"
    MODIFY_FOCUS_FILES_DONE = "modify_focus_files_done"
    MODIFY_PLAN = "modify_plan"
    WAIT_FOR_MODIFY_PLAN = "wait_for_modify_plan"
    GENERATE_ACTION = "generate_action"
    APPLY_ACTION = "apply_action"
    WAIT_APPLY_ACTION = "wait_apply_action"
    DONE = "done"


class SWEToolEntity(BaseToolEntity):
    parameters: dict[str, any]
    swe_agent: SoftwareEngineerAgent
    stage: Stage

    def __init__(self):
        self.swe_agent = SoftwareEngineerAgent()
        self.parameters = {}
        
    def current_state(self):
        match self.stage:
            case Stage.INIT:
                return State.IDLE
            case Stage.DONE:
                return State.DONE
            case _:
                return State.RUNNING
    
    def set_parameters(self, **kwargs):
        self.parameters = kwargs

    def call(self):
        match self.stage:
            case Stage.INIT:
                self.stage = Stage.WAIT_FOR_GIT_REPO
                return ...
            case Stage.WAIT_FOR_GIT_REPO:
                ...
                return ...
            case _:
                ...

