import pytest
from src.core.assistant.threads import Threads
from src.core.assistant.async_threads import AsyncThreads
from src.core.assistant.assistant import Assistants
from src.core.assistant.tools.tools import register_function_tool,register_stateful_tool
import asyncio
# def test_threads_create():
#     # 创建一个 Threads 对象
#     threads = Threads.create()

#     # 检查 id 是否被正确设置
#     assert threads.config.id is not None
#     assert isinstance(threads.config.id, str)

#     # 检查其他属性的默认值
#     assert threads.config.object == "thread"
#     assert threads.config.assistant_id is None
#     assert threads.config.metadata == {}
@register_function_tool
def code_test(code:str):
    return {
        "type": "success",
        "content": {
            "result": "Hello, World!",
        },
    }

import logging
from typing import List, Optional
from src.core.assistant.tools.stateful_tool_entity import *
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
    
@pytest.mark.asyncio
async def test_threads_run_stateful_tool():
    # 创建一个 Threads 对象  
    threads = AsyncThreads.create('tools.yaml')
    # 创建一个助手并保存到 assistants.yaml 文件
    assistant = Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="Use understand codebase tool to get insight of the code", tools=[{'type':'understand_tool'}])
    print(assistant.id)
    # 运行 Threads 对象
    result =await threads.run(assistant.id, "Use SoftWare Engineer Agent swe tool auto fix code files.")
    print(result)

    result =await threads.run(assistant.id, "the repo url is https://github.com/YORG-AI/Open-Assistant",goto="stage_1")
    print(result)

    result =await threads.run(assistant.id, "the repo url is https://github.com/YORG-AI/Open-Assistant",goto="stage_2")
    print(result)

    result =await threads.run(assistant.id, "user_feature=what is swe agent usage,query_related_code='',query_related_content=''", goto="stage_3")
    print(result)

    result =await threads.run(assistant.id, "", goto="finish")
    print(result)