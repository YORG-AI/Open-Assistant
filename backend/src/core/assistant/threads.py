import uuid
from typing import List, Optional
from pydantic import BaseModel, Field
from src.core.assistant.assistant import Assistants
from src.core.nodes.openai.openai import OpenAINode
from src.core.nodes.openai.openai_model import *
from src.core.assistant.tools import Tools
import time
import yaml
import os
import re

def extract_bracket_content(s: str) -> list:
    content = re.findall(r'\[(.*?)\]', s)
    return [c.replace("'", "") for c in content]

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
    def __init__(self, config: ThreadsConfig):
        self._config = config

    @property
    def config(self):
        return self._config
    
    def save_to_yaml(self):
        import os

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

    def run(self, assistant_id: str, input_text: str):
       # 使用 from_id 方法获取助手
        assistant = Assistants.from_id(assistant_id)
        tools_list = assistant.get_tools_type_list()
        # 初始化 Tools 对象
        tools = Tools()
        # 获取 tools 的 summary
        tools_summary = tools.get_tools_list_summary(tools_list)
        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 获取 prompt 文件夹下的 few_shot_tools_choose_prompt.txt 文件的路径
        few_shot_tools_choose_prompt = os.path.join(current_dir, 'prompt', 'few_shot_tools_choose_prompt.txt')

        # 读取文件内容
        with open(few_shot_tools_choose_prompt, 'r') as file:
            prompt_text = file.read()
        tools_choose_prompt = prompt_text+f"""
Input:
tools_summary: {tools_summary}
input_text: {input_text}
"""     

        
        # 创建一个 OpenAINode 对象
        tools_node = OpenAINode()
        message_config = Message(
            role = 'user',
            content = tools_choose_prompt
        )
        # 创建一个 ChatInput 对象
        chat_config = ChatWithMessageInput(
            message=message_config,
            model="gpt-4",
            append_history=False,
            use_streaming=False
        )

        # 使用 chat_with_prompt_template 方法进行聊天
        response = tools_node.chat_with_message(chat_config).message.content
        response = extract_bracket_content(response)

        # todo：已经选好tool了，接下来写prompt去生成对应tools参数的text，然后给tools运行，之后在结合tools运行结果，再生成一份回答，然后就给用户。

        return response
