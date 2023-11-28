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
from src.core.agents.software_engineer.software_engineer import SoftwareEngineerAgent
# 使用装饰器
@register_stateful_tool
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
        return {"type": "success", "content": {"result": "stage3 done","plans":plans}}

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
        return {"type": "success", "content": {"result": "stage4 done","plans":plans}}

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
            selftask.set_finish_file_actions(finish_file_actions)
            del file_actions[action_idx]
            selftask.set_file_actions(file_actions)
        elif action == REVISE:
            new_action = task.agent._revise_code(f"{task.previous_action[action_idx]}", revise_comments, action_idx)
            self.previous_action.append(new_action)
            return {"type": "success", "content": {"result": "stage6 done","actions":self.previous_action}}
        return {"type": "success", "content": {"result": "stage6 done"}}
    
    def _finish(self):
        return {"type": "success", "content": {"message": "stateful tool is finished"}}
# def test_threads_run():
#     # 创建一个 Threads 对象  
#     threads = Threads.create('tools.yaml')
#     # 创建一个助手并保存到 assistants.yaml 文件
#     assistant = Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="run code", tools=[{'type':'code_test'}])
#     # 运行 Threads 对象
#     result = threads.run(assistant.id, "tell me python code print('Hello, World!') result")
#     print(result)
#     # 运行 Threads 对象
#     result = threads.run(assistant.id, "Tell me the answer of 17th fibonacci number plus 20th prime.")
#     print(result)

#     print(threads.config.message_history)
@pytest.mark.asyncio
async def test_threads_run_stateful_tool():
    # 创建一个 Threads 对象  
    threads = AsyncThreads.create('tools.yaml')
    # 创建一个助手并保存到 assistants.yaml 文件
    assistant = Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="Use swe tool auto fix code files", tools=[{'type':'SWEToolEntity'}])
    print(assistant.id)
    # 运行 Threads 对象
    result =await threads.run(assistant.id, "Use SoftWare Engineer Agent swe tool auto fix code files.")
    print(result)

    result =await threads.run(assistant.id, "the repo url is https://github.com/YORG-AI/Open-Assistant",goto="stage_1")
    print(result)

    result =await threads.run(assistant.id, "add helloworld feature to readme",  goto="stage_2")
    print(result)

    result =await threads.run(assistant.id, "focus_files_name_list = [README.md]", goto="stage_3")
    print(result)

    result =await threads.run(assistant.id, "action=3", goto="stage_4")
    print(result)

    result =await threads.run(assistant.id, "", goto="stage_5")
    print(result)

    result =await threads.run(assistant.id, "action=0,action_idx=0", goto="stage_6")
    print(result)

    result =await threads.run(assistant.id, "", goto="finish")
    print(result)

# def test_threads_run_stateful_tool():
#     # 创建一个 Threads 对象  
#     threads = Threads.create('tools.yaml')
#     # 创建一个助手并保存到 assistants.yaml 文件
#     assistant = Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="Use swe tool auto fix code files", tools=[{'type':'swe_tool'}])
#     print(assistant.id)
#     # 运行 Threads 对象
#     result = threads.run(assistant.id, "Use SoftWare Engineer Agent swe tool auto fix code files.")
#     print(result)

#     result = threads.run(assistant.id, "the repo url is https://github.com/YORG-AI/Open-Assistant",goto="stage_1")
#     print(result)

#     result = threads.run(assistant.id, "add helloworld feature to readme",  goto="stage_2")
#     print(result)

#     result = threads.run(assistant.id, "focus_files_name_list = [README.md]", goto="stage_3")
#     print(result)

#     result = threads.run(assistant.id, "action=3", goto="stage_4")
#     print(result)

#     result = threads.run(assistant.id, "", goto="stage_5")
#     print(result)

#     result = threads.run(assistant.id, "action=0,action_idx=0", goto="stage_6")
#     print(result)

#     result = threads.run(assistant.id, "", goto="finish")
#     print(result)
     
