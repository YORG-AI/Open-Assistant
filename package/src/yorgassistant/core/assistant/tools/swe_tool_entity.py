import logging
from typing import List, Optional
from .stateful_tool_entity import *
from ...agents.software_engineer.software_engineer import SoftwareEngineerAgent
    
class SWEToolEntity(StatefulToolEntity):
    def __init__(self):
        super().__init__("swe_tool.yaml")
        self.tmp_dict = {}
        self.task = SoftwareEngineerAgent()
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
                return self._stage1(kwargs["repo_url"])
            case "stage_2":
                return self._stage2(kwargs["feature"])
            case "stage_3":
                return self._stage3(kwargs["focus_files_name_list"])
            case "stage_4":
                return self._stage4(kwargs["action"],kwargs["plan_idx"],kwargs["focus_file_name"],kwargs["description"])
            case "stage_5":
                return self._stage5()
            case "stage_6":
                return self._stage6(kwargs["action"],kwargs["action_idx"],kwargs["revise_comments"])
            case self.config.finish_stage:
                return self._finish()
            case _:
                return {
                    "type": "error",
                    "content": {"message": f"stage {self.current_stage.name} not found"},
                }

    def _stage1(self, repo_url:str):
        self.repo_url = repo_url
        #本地处理repo
        if repo_url.startswith("http"):
            self.task.set_repo_url(repo_url)
        else:
            self.task.set_local_repo(repo_url)
        return {"type": "success", "content": {"message": "stage1 done,get repo_url"}}

    def _stage2(self, feature: str):
        self.feature = feature
        #添加功能说明
        self.task.set_feature_description(feature)
        return {"type": "success", "content": {"message": "stage2 done,get feature"}}

    def _stage3(self,focus_files_name_list: List[str]):
        #锁定文件
        self.task.set_focus_files()
        #选择修改文件
        for focus_files_name in focus_files_name_list:
            self.task.add_focus_file(focus_files_name)
        #plan
        self.task.design_plan()
        plans = self.task.get_plan()
        return {"type": "success", "content": {"result": "stage3 done","plans":str(plans)}}

    def _stage4(self,action:int,plan_idx:int,focus_file_name:str,description:str):
        ADD_PLAN = 0
        REMOVE_PLAN = 1
        MODIFY_PLAN = 2
        
        plans = self.task.get_plan()
        if action == ADD_PLAN:
            plans.append(Plan(action="add", file_path=focus_file_name, description=description))
        elif action == REMOVE_PLAN:
            print("the deleting plan is: ")
            print(plans[plan_idx])
            # plans.pop(plan_idx)
            del plans[plan_idx]
        elif action == MODIFY_PLAN:
            plans[plan_idx].file_path = focus_file_name
            plans[plan_idx].description = description
            plans[plan_idx].action = 'modify'
        self.task.set_plans(plans)
        return {"type": "success", "content": {"result": "stage4 done","plans":str(plans)}}

    def _stage5(self):
        actions = []
        for action in self.task.implement():
            actions.append(action.content)
            self.previous_action.append(action)
        return {"type": "success", "content": {"result": "stage5 done","actions":self.previous_action}}

    #差最后一个步骤，apply还是不apply还是revise
    def _stage6(self,action:int,action_idx:int,revise_comments:str):
        APPLY = 0
        NOT_APPLY = 1
        REVISE = 2
        if action == APPLY:
            file_actions = self.task.get_file_actions()
            self.task.apply_one_file_action(action_idx)
            finish_file_actions = self.task.get_finish_file_actions()
            finish_file_actions.append(file_actions[action_idx])
            self.task.set_finish_file_actions(finish_file_actions)
            del file_actions[action_idx]
            self.task.set_file_actions(file_actions)
        elif action == NOT_APPLY:
            file_actions = self.task.get_file_actions()
            finish_file_actions = self.task.get_finish_file_actions()
            finish_file_actions.append(file_actions[action_idx])
            self.task.set_finish_file_actions(finish_file_actions)
            del file_actions[action_idx]
            self.task.set_file_actions(file_actions)
        elif action == REVISE:
            new_action = self.task.agent._revise_code(f"{self.task.previous_action[action_idx]}", revise_comments, action_idx)
            self.previous_action.append(new_action)
            return {"type": "success", "content": {"result": "stage6 done","actions":self.previous_action}}
        return {"type": "success", "content": {"result": "stage6 done"}}
    
    def _finish(self):
        return {"type": "success", "content": {"message": "stateful tool is finished"}}