import logging
from typing import List, Optional
from .stateful_tool_entity import *
from src.core.assignments.understand_codebase.understand_code_base_assignment import CodeBaseAssignment
    
class UnderstandToolEntity(StatefulToolEntity):
    def __init__(self):
        super().__init__("understand_tool.yaml")
        self.tmp_dict = {}
        self.task = CodeBaseAssignment()

    async def _call(self, **kwargs):
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
                return self._stage2(kwargs["repo_url"])
            case "stage_3":
                return await self._stage3(kwargs["user_feature"],kwargs["query_related_code"],kwargs["query_related_content"])
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
        return {"type": "success", "content": {"message": "stage1 done, get repo_url"}}

    def _stage2(self, repo_url:str):
        self.repo_url = repo_url
        self.task.generate_code_dependencies()
        self.task.generate_code_classes()
        return {"type": "success", "content": {"message": "stage2 done,get ast structure"}}

    async def _stage3(self,user_feature, query_related_code, query_related_content):
        #设定查询内容
        self.task.set_code_base_query(user_feature=user_feature, query_related_code= query_related_code, query_related_content=query_related_content)
        await self.task.set_possiblly_related_file()
        await self.task.understand_codebase()
        understanding = self.task.get_understanding()[0]
        return {"type": "success", "content": {"result": "stage3 done","understanding":understanding}}

    
    def _finish(self):
        return {"type": "success", "content": {"message": "stateful tool is finished"}}