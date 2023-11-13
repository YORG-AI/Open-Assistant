import uuid
from typing import List, Optional
from pydantic import BaseModel, Field

from src.core.assistant.assistant import Assistants
from src.core.nodes.openai.openai import OpenAINode
from src.core.nodes.openai.openai_model import *
from src.core.assistant.tools import Tools, Tool

import time
import yaml
import os
import re
import logging
import json

from .prompt.few_shot_tools_choose_prompt import *
from .prompt.parameters_generate_prompt import *
from .prompt.response_generate_prompt import *

def extract_bracket_content(s: str) -> list:
    content = re.findall(r'\[(.*?)\]', s)
    content = [c.replace("'", "") for c in content]
    content = filter(lambda x: x != "", content)
    return list(content)

class MessageRecord(BaseModel):
    role: str = Field(description="角色")
    content: str = Field(description="内容")

class ThreadsConfig(BaseModel):
    id: str = Field(description="线程 ID")
    object: str = Field(default="thread", description="对象类型")
    created_at: int = Field(description="创建时间")
    assistant_id:  Optional[str] = Field(description="助手 ID")
    message_history: List[MessageRecord] = Field(description="消息")
    metadata: dict = Field(default={}, description="元数据")

class Threads:
    current_tool: Tool
    chat_node: OpenAINode # Threads 全局的 OpenAI node，仅用于 chat 交互以及对 tool 执行结果的分析（选择 tool 以及生成参数不使用该 node）


    def __init__(self, config: ThreadsConfig):
        self._config = config
        self.current_tool = None
        self.chat_node = OpenAINode()

    @property
    def config(self):
        return self._config
    
    def save_to_yaml(self):
        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建 threads.yaml 文件的绝对路径
        threads_yaml_path = os.path.join(current_dir, 'threads.yaml')

        # 使用绝对路径打开 threads.yaml 文件
        with open(threads_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or []
        # 查找具有相同 id 的 assistant
        for i, d in enumerate(data):
            if d['id'] == self.config.id:
                # 如果找到了，就更新它
                data[i] = self.config.__dict__
                break
        else:
            # 如果没有找到，就添加新的 assistant 到列表中
            data.append(self.config.__dict__)
        # 写回 YAML 文件
        with open(threads_yaml_path, 'w') as file:
            yaml.dump(data, file)

    @staticmethod
    def create() -> 'Threads':
        # 创建 ThreadsConfig 对象
        config = ThreadsConfig(
            id=str(uuid.uuid4()),
            object="thread",
            created_at=int(time.time()),
            message_history=[],
            metadata={}
        )

        # 创建 Threads 对象
        threads = Threads(config)

        # 保存到 YAML 文件
        threads.save_to_yaml()

        return threads

    def run(self, assistant_id: str, input_text: str, **kwargs):
       # 使用 from_id 方法获取助手
        assistant = Assistants.from_id(assistant_id)
        tools_list = assistant.get_tools_type_list()
        # 初始化 Tools 对象
        tools = Tools()
        # 获取 tools 的 summary
        tools_summary = tools.get_tools_list_summary(tools_list)

        # 如果第一次执行或当前的 tool 已执行完毕
        if self.current_tool is None or self.current_tool.has_done():
            # 使用 LLM 选择 tools
            chosen_tools = self._choose_tools(tools_summary, input_text)
            # TODO: 支持多个 tool 执行
            if len(chosen_tools) == 0:
                logging.warn("No tool is recommended.")
                # 不使用 Tool, 直接 chat
                res = self._chat(input_text, assistant)
            else:
                tool_name = chosen_tools[0]
                
                # 获取对应的 tool 对象
                target_tool = tools.get_tool(tool_name)
                self.current_tool = target_tool

                # 判断当前 tool 的执行是否需要 llm 生成参数
                if target_tool.need_llm_generate_parameters():
                    # 使用 LLM 生成参数
                    parameters = self._generate_parameters(target_tool, input_text)
                else:
                    parameters = kwargs
                
                # 执行 tool
                res = target_tool.call(**parameters)

                # 根据执行结果，交给 LLM 进行包装
                if target_tool.need_llm_generate_response():
                    # 使用 LLM 生成 response
                    res = self._generate_response(target_tool, input_text, parameters, res, assistant)
            
            self._config.message_history = [MessageRecord(role='user',content=input_text),MessageRecord(role='assistant',content=res)]
            return res

    def _chat(self, input_text: str, assistant: Assistants) -> str:
        # TODO: 使用全局 OpenAI Node

        # 使用 assistant 的 description 和 instructions
        description = assistant.description
        instructions = assistant.instructions
        system_prompt = f"""You're an assistant. That's your description.\n{description}\nPlease follow these instructions:\n{instructions}\n """
        self.chat_node.add_system_message(system_prompt)
        message_config = Message(
            role = 'user',
            content = input_text
        )

        # 创建一个 ChatInput 对象
        chat_config = ChatWithMessageInput(
            message=message_config,
            model="gpt-4-1106-preview",
            append_history=True,
            use_streaming=False
        )

        # 使用 chat_with_prompt_template 方法进行聊天
        response = self.chat_node.chat_with_message(chat_config).message.content

        return response

    def _choose_tools(self, tools_summary: dict, input_text: str) -> list[str]:
        # 创建一个 OpenAINode 对象
        tools_node = OpenAINode()

        tools_node.add_system_message(TOOLS_CHOOSE_PROMPT + TOOLS_CHOOSE_EXAMPLE_PROMPT + TOOLS_CHOOSE_HINT)

        tools_choose_prompt = f"""
Input:
tools_summary: {tools_summary}
input_text: {input_text}
"""     

        message_config = Message(
            role = 'user',
            content = tools_choose_prompt
        )

        # 创建一个 ChatInput 对象
        chat_config = ChatWithMessageInput(
            message=message_config,
            model="gpt-4-1106-preview",
            append_history=False,
            use_streaming=False
        )

        # 使用 chat_with_prompt_template 方法进行聊天
        response = tools_node.chat_with_message(chat_config).message.content
        tools_list = extract_bracket_content(response)

        return tools_list

    def _generate_parameters(self, target_tool: Tool, input_text: str) -> dict:
        # 创建一个 OpenAINode 对象
        tools_node = OpenAINode()

        tools_node.add_system_message(PARAMETERS_GENERATE_PROMPT + PARAMETERS_GENERATE_EXAMPLE_PROMPT + PARAMETERS_GENERATE_HINT)

        parameters_generate_prompt = f"""
Input:
tools_name: {target_tool.config.name}
tools_summary: {target_tool.config.summary}
input_text: {input_text}
tool_input_schema: {[parameter.json() for parameter in target_tool.config.parameters]}
"""
        
        message_config = Message(
            role = 'user',
            content = parameters_generate_prompt
        )

        # 创建一个 ChatInput 对象
        chat_config = ChatWithMessageInput(
            message=message_config,
            model="gpt-4-1106-preview",
            append_history=False,
            use_streaming=False
        )

       # 使用 chat_with_prompt_template 方法进行聊天
        while True:
            try:
                response = tools_node.chat_with_message(chat_config).message.content
                parameters = json.loads(response)
                break
            except json.JSONDecodeError:
                continue

        return parameters

    def _generate_response(self, target_tool: Tool, input_text: str, tool_input: dict[str, any], tool_result: dict[str, any], assistant: Assistants) -> dict:
        # 创建一个 OpenAINode 对象
        response_node = OpenAINode()
        # 使用 assistant 的 description 和 instructions
        description = assistant.description
        instructions = assistant.instructions
        system_prompt = f"""You're an assistant. That's your description.\n{description}\nPlease follow these instructions:\n{instructions}\n """
        response_node.add_system_message(system_prompt)
        response_node.add_system_message(RESPONSE_GENERATE_PROMPT + RESPONSE_GENERATE_EXAMPLE_PROMPT + RESPONSE_GENERATE_HINT)

        response_generate_prompt = f"""
Input:
input_text: {input_text}
chosen_tool_info: {target_tool.config.json()}
tool_input: {tool_input}
tool_result: {tool_result}
"""
        
        message_config = Message(
            role = 'user',
            content = response_generate_prompt
        )

        # 创建一个 ChatInput 对象
        chat_config = ChatWithMessageInput(
            message=message_config,
            model="gpt-4-1106-preview",
            append_history=False,
            use_streaming=False
        )

        response = response_node.chat_with_message(chat_config).message.content
        return response