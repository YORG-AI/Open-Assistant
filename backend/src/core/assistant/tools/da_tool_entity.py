import os
from typing import List
from .stateful_tool_entity import *
from ....core.agents.data_analysis.data_analysis import DataAnalysisAgent


class DAToolEntity(StatefulToolEntity):
    def __init__(self):
        super().__init__("da_tool_entity.yaml")
        self.tmp_dict = {}
        self.task = DataAnalysisAgent()
        self.previous_action = []

    def _call(self, **kwargs):
        if "goto" not in kwargs:
            if self.current_stage.name == self.config.start_stage:
                return {
                    "type": "success",
                    "content": {"message": "swe tool is started"},
                }
            else:
                return {
                    "type": "error",
                    "content": {"message": "please provide `goto` parameter"},
                }

        request_next_stage = kwargs["goto"]
        if request_next_stage not in self.config.all_stages:
            return {
                "type": "error",
                "content": {"message": f"stage {request_next_stage} not found"},
            }
        self.current_stage = self.config.all_stages[request_next_stage]

        match self.current_stage.name:
            case "stage_1":
                return self._stage1(kwargs["project_name"])
            case "stage_2":
                return self._stage2(kwargs["file_list"])
            case "stage_3":
                return self._stage3(kwargs["project_requirement"])
            case "stage_4":
                return self._stage4()
            case "stage_5":
                return self._stage5(kwargs["project_type"])
            case "stage_6":
                return self._stage6()
            case "stage_7":
                return self._stage7()
            case self.config.finish_stage:
                return self._finish()
            case _:
                return {
                    "type": "error",
                    "content": {"message": f"stage {self.current_stage.name} not found"},
                }

    def _stage1(self, project_name: str):
        self.task.set_project_name(project_name)
        return {"type": "success", "content": {"message": "stage1 done, successfully set project_name"}}

    def _stage2(self, file_list: List[str]):
        for file_path in file_list:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.task.add_file_path(file_path)
            else:
                return {"type": "error", "content": {"message": "file at path: %s not found." % (file_path)}}
        return {"type": "success", "content": {"message": "stage2 done, add files"}}

    def _stage3(self, project_requirement: str):
        self.task.set_project_requirement(project_requirement)
        return {"type": "success", "content": {"result": "stage3 done"}}

    def _stage4(self):
        types = self.task.plan_project_type()
        return {"type": "success", "content": {"result": "stage4 done", "planned_types": types}}

    def _stage5(self, project_type: str):
        self.task.set_project_type(project_type)
        self.task.obtain_step_plan()
        plan_list = self.task.step_plan[:self.task.step_numbers]
        return {"type": "success", "content": {"result": "stage5 done", "plan_list": plan_list}}

    def _stage6(self):
        for step_idx in range(self.task.step_numbers):
            self.task.step_code_generator(step_idx)
        return {"type": "success", "content": {"result": "stage6 done", "code": self.task.step_code[:self.task.step_numbers]}}

    def _stage7(self):
        for step_idx in range(self.task.step_numbers):
            self.task.step_report_generator(step_idx)
        return {"type": "success", "content": {"result": "stage6 done", "code": self.task.step_report[:self.task.step_numbers]}}
    def _finish(self):
        return {"type": "success", "content": {"message": "stateful tool is finished"}}