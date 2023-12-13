
import uuid
from typing import Any, List, Optional,Dict


from .assistant import Assistants
from ..nodes.openai.openai import OpenAINode
from ..nodes.openai.openai_model import *
from .tools.tools import Tools, Tool
from .config import *

import time
import yaml
import os
import re
import logging
import json
import inspect
# from .prompt.few_shot_tools_choose_prompt import *
from .prompt.few_shot_cot_tools_choose_prompt import *
from .prompt.parameters_generate_prompt import *
from .prompt.response_generate_prompt import *


def extract_bracket_content(s: str) -> list:
    content = re.findall(r"\[(.*?)\]", s)
    content = [c.replace("'", "") for c in content]
    content = filter(lambda x: x != "", content)
    ret = []
    for item in content:
        if "," in item:
            ret.extend(item.split(","))
        else:
            ret.append(item)
    return ret




class Threads:
    current_tool: Tool
    chat_node: OpenAINode  # Threads 全局的 OpenAI node，仅用于 chat 交互以及对 tool 执行结果的分析（选择 tool 以及生成参数不使用该 node）

    def __init__(self, config: ThreadsConfig,threads_yaml_path:Optional[str] = None):
        self._config = config
        self.current_tool = None
        YamlPathConfig.threads_yaml_path = threads_yaml_path if threads_yaml_path else "threads.yaml"

    @property
    def config(self):
        return self._config
    
    @property
    def id(self):
        return self._config.id

    def set_threads_yaml_path(yaml_path:str):
        # 检查 yaml_path 是否为绝对路径
        if not os.path.isabs(yaml_path):
            # 获取调用此方法的栈帧
            stack = inspect.stack()
            caller_frame = stack[1]
            # 获取调用者的文件路径
            caller_path = caller_frame.filename
            # 获取调用者的目录路径
            caller_dir = os.path.dirname(caller_path)
            # 构建 yaml 文件的绝对路径
            full_yaml_path = os.path.join(caller_dir, yaml_path)
        else:
            full_yaml_path = yaml_path
        # 获取 yaml 文件所在的目录
        yaml_dir = os.path.dirname(full_yaml_path)
        # 如果目录不存在，则创建它
        os.makedirs(yaml_dir, exist_ok=True)
        # 设置 yaml_path
        YamlPathConfig.threads_yaml_path = full_yaml_path


    def save_to_yaml(self):
        # 构建 threads.yaml 文件的绝对路径
        threads_yaml_path = YamlPathConfig.threads_yaml_path
        # 检查文件是否存在，如果不存在，则创建一个空的yaml文件
        if not os.path.exists(threads_yaml_path):
            with open(threads_yaml_path, 'w') as file:
                file.write('')  # 创建一个空文件
        # 使用绝对路径打开 threads.yaml 文件
        with open(threads_yaml_path, "r") as file:
            data = yaml.safe_load(file) or []
        # 查找具有相同 id 的 assistant
        for i, d in enumerate(data):
            if d["id"] == self.config.id:
                # 如果找到了，就更新它
                data[i] = self.config.to_dict()
                break
        else:
            # 如果没有找到，就添加新的 assistant 到列表中
            data.append(self.config.to_dict())
        # 写回 YAML 文件
        with open(threads_yaml_path, "w") as file:
            yaml.dump(data, file)

    @staticmethod
    def create() -> "Threads":
        # 创建 ThreadsConfig 对象
        config = ThreadsConfig(
            id=str(uuid.uuid4()),
            object="thread",
            created_at=int(time.time()),
            message_history=[],
            metadata={},
        )
       
        # 创建 Threads 对象
        threads = Threads(config,YamlPathConfig.threads_yaml_path)

        # 保存到 YAML 文件
        threads.save_to_yaml()

        return threads

    @classmethod
    def from_id(cls, id: str) -> 'Threads':
        # 使用传入的 yaml_path 参数打开 YAML 文件
        with open(YamlPathConfig.threads_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or []
        # 查找具有相同 id 的配置
        for d in data:
            if d['id'] == id:
                # 如果找到了，就用这个配置创建一个新的对象
                config = ThreadsConfig.from_dict(d)
                return cls(config, YamlPathConfig.threads_yaml_path)  # 使用传入的 yaml_path 创建  实例
        # 如果没有找到，就抛出一个异常
        raise ValueError(f'No threads with id {id} found in YAML file.')
    @staticmethod
    def get_all_threads() -> List[Dict[str, Any]]:
        """
        读取 YAML 文件并返回所有 threads 的信息列表。
        """
        # 确保 YAML 文件路径已经被设置
        if not YamlPathConfig.threads_yaml_path or not os.path.isfile(YamlPathConfig.threads_yaml_path):
            raise FileNotFoundError("The threads YAML file path is not set or the file does not exist.")

        # 读取 YAML 文件
        with open(YamlPathConfig.threads_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or []
        # 使用 from_dict 方法将每个字典转换为 ThreadsConfig 实例
        threads_list = []
        for item in data:
            config = ThreadsConfig.from_dict(item)
            threads_list.append(config)

        return threads_list
    def run(self, assistant_id: str, input_text: str, **kwargs):
        try:
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

                    self.current_tool = None
                    # 不使用 Tool, 直接 chat
                    res_message = self._chat(input_text, assistant)
                else:
                    tool_name = chosen_tools[0]

                    # 获取对应的 tool 对象
                    self.current_tool = tools.get_tool(tool_name)

            # 判断当前 tool 的执行是否需要 llm 生成参数
            if self.current_tool is not None and self.current_tool.need_llm_generate_parameters():
                # 使用 LLM 生成参数
                parameters = self._generate_parameters(self.current_tool, input_text)
            else:
                parameters = kwargs
                parameters['input_text'] = input_text

            # 执行 tool
            if self.current_tool is not None:
                res_message = self.current_tool.call(**parameters)
                tool_tmp_message = str(res_message)

            # 根据执行结果，交给 LLM 进行包装
            if self.current_tool is not None and self.current_tool.need_llm_generate_response():
                # 使用 LLM 生成 response
                res_message = self._generate_response(
                    self.current_tool, input_text, parameters, tool_tmp_message, assistant
                )

            if isinstance(res_message, dict) and 'assistant' in res_message:
                res_message['content']['tool'] = self.current_tool.config.name
                res_message['content']['tool_type'] = self.current_tool.tool_type
                res_message['content']['tool_response'] = tool_tmp_message
                if res_message['type'] =='success':
                    self._config.message_history.append(
                        [
                            {'user':input_text},
                            {'assistant':res_message},
               
                        ]
                    )
                    self._config.assistant_id = assistant_id
                    self.save_to_yaml()
                return res_message
            else:
                assistant_message_str = str(res_message)
                result_dict = {
                'type': 'success',
                'content': {'tool': self.current_tool.config.name if self.current_tool else '','tool_type':self.current_tool.tool_type if self.current_tool else '','tool_response':tool_tmp_message if self.current_tool else ''},
                'next_stages_info': {},
                'assistant': {'message': assistant_message_str}
            }
                self._config.message_history.append(
                    [
                        {'user':input_text},
                        {'assistant':result_dict},
                    ]
                )
                self._config.assistant_id = assistant_id
                self.save_to_yaml()
                return result_dict
            
        except Exception as e:
            # 异常时的返回格式
            logging.error(f"An error occurred: {e}")
            return {
                'type': 'error',
                'content': {'message': str(e)},
                'next_stages_info': {},
                'assistant': {'message': ''}
            }
        

    def _chat(
        self, prompt: str, assistant: Assistants, system_message: Optional[str] = None
    ) -> str:
        # 创建一个 OpenAINode 对象
        response_node = OpenAINode()

        # 使用 assistant 的 description 和 instructions
        description = assistant.description
        instructions = assistant.instructions
        system_prompt = f"""You're an assistant. That's your description.\n{description}\nPlease follow these instructions:\n{instructions}\n """
        response_node.add_system_message(system_prompt)
        if system_message:
            response_node.add_system_message(system_message)

        # 如果 self._config.message_history 里有数据
        if self._config.message_history:
            for record in self._config.message_history:
                user_message = record[0]
                assistant_message = record[1]
                response_node.add_content(user_message['user'])
                response_node.add_role('user')
                response_node.add_content(str(assistant_message['assistant']))
                response_node.add_role('assistant')

        message_config = Message(role="user", content=prompt)

        # 创建一个 ChatInput 对象
        chat_config = ChatWithMessageInput(
            message=message_config,
            model="gpt-4-1106-preview",
            append_history=False,
            use_streaming=False,
        )

        response = response_node.chat_with_message(chat_config).message.content
        return response

    def _choose_tools(self, tools_summary: dict, input_text: str,instruct:bool = False) -> list[str]:
        
         # 创建一个 OpenAINode 对象
        tools_node = OpenAINode()
        if instruct:
            tools_choose_prompt = TOOLS_CHOOSE_PROMPT + TOOLS_CHOOSE_EXAMPLE_PROMPT + TOOLS_CHOOSE_HINT +f"""\nInput:\ntools_summary: {tools_summary}\ninput_text: {input_text}\nDispose:"""     

            # 创建一个 ChatInput 对象
            chat_config = OldCompleteInput(
                model="gpt-3.5-turbo-instruct",
                prompt = tools_choose_prompt,
                use_streaming=False
            )

            response = tools_node.use_old_openai_with_prompt(chat_config).text

        else:
            tools_node.add_system_message(
                TOOLS_CHOOSE_PROMPT + TOOLS_CHOOSE_EXAMPLE_PROMPT + TOOLS_CHOOSE_HINT
            )

            tools_choose_prompt = f"""
    Input:
    tools_summary: {tools_summary}
    input_text: {input_text}
    Dispose:
    """

            message_config = Message(role="user", content=tools_choose_prompt)

            # 创建一个 ChatInput 对象
            chat_config = ChatWithMessageInput(
                message=message_config,
                model="gpt-4-1106-preview",
                append_history=False,
                use_streaming=False,
            )

            # 使用 chat_with_prompt_template 方法进行聊天
            response = tools_node.chat_with_message(chat_config).message.content
         # 使用正则表达式匹配字典部分
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            dict_str = match.group()
            # 使用json.loads()函数将字符串转换为字典
            response = json.loads(dict_str)
        else:
            response = json.loads(response)
        # tools_list = extract_bracket_content(response)
        # response = json.loads(response)
        tools_list = response['tool']['name']

        # print(f'tools_list:{tools_list}')
        return tools_list

    def _generate_parameters(self, target_tool: Tool, input_text: str,instruct:bool = False) -> dict:
        # 创建一个 OpenAINode 对象
        tools_node = OpenAINode()
        if instruct:
            parameters_generate_prompt = PARAMETERS_GENERATE_PROMPT + PARAMETERS_GENERATE_EXAMPLE_PROMPT + PARAMETERS_GENERATE_HINT +f"""
    Input:
    tools_name: {target_tool.config.name}
    tools_summary: {target_tool.config.summary}
    input_text: {input_text}
    tool_input_schema: {[parameter.json() for parameter in target_tool.config.parameters]}
    """

            # 创建一个 ChatInput 对象
            chat_config = OldCompleteInput(
                model="gpt-3.5-turbo-instruct",
                prompt = parameters_generate_prompt,
                use_streaming=False
            )
            
            max_attempts = 5
            attempts = 0

            while attempts < max_attempts:
                try:
                    response = tools_node.use_old_openai_with_prompt(chat_config).text
                    parameters = json.loads(response)
                    break
                except json.JSONDecodeError:
                    attempts+=1
                    continue
        else:
            tools_node.add_system_message(
                PARAMETERS_GENERATE_PROMPT
                + PARAMETERS_GENERATE_EXAMPLE_PROMPT
                + PARAMETERS_GENERATE_HINT
            )

            parameters_generate_prompt = f"""
    Input:
    tools_name: {target_tool.config.name}
    tools_summary: {target_tool.config.summary}
    input_text: {input_text}
    tool_input_schema: {[parameter.json() for parameter in target_tool.config.parameters]}
    """

            message_config = Message(role="user", content=parameters_generate_prompt)

            # 创建一个 ChatInput 对象
            chat_config = ChatWithMessageInput(
                message=message_config,
                model="gpt-4-1106-preview",
                append_history=False,
                use_streaming=False,
            )

            # 使用 chat_with_prompt_template 方法进行聊天
            max_attempts = 5
            attempts = 0

            while attempts < max_attempts:
                try:
                    response = tools_node.chat_with_message(chat_config).message.content
                    parameters = json.loads(response)
                    break
                except json.JSONDecodeError:
                    attempts += 1
                    continue
        return parameters

    def _generate_response(
        self,
        target_tool: Tool,
        input_text: str,
        tool_input: dict[str, any],
        tool_result: dict[str, any],
        assistant: Assistants,
    ) -> str:
        system_message = (
            RESPONSE_GENERATE_PROMPT
            + RESPONSE_GENERATE_EXAMPLE_PROMPT
            + RESPONSE_GENERATE_HINT
        )
        response_generate_prompt = f"""
Input:
input_text: {input_text}
chosen_tool_info: {target_tool.config.json()}
tool_input: {tool_input}
tool_result: {tool_result}
"""
        return self._chat(response_generate_prompt, assistant, system_message)