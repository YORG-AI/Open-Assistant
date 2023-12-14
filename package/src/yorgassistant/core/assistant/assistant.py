import uuid
import time
import os
import yaml
from typing import Optional

import inspect
from .config import *
from typing import Dict,Any
class Assistants():
    def __init__(self, config,yaml_path:Optional[str] = None):
        self.config = config
        YamlPathConfig.assistants_yaml_path = yaml_path if yaml_path else 'assistants.yaml'
    
    def set_assistants_yaml_path(yaml_path: str):
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
        # 设置 assistants_yaml_path
        YamlPathConfig.assistants_yaml_path = full_yaml_path

    def save_to_yaml(self):
        # 构建 assistants.yaml 文件的绝对路径
        assistants_yaml_path = YamlPathConfig.assistants_yaml_path
        # 检查文件是否存在，如果不存在，则创建一个空的yaml文件
        if not os.path.exists(assistants_yaml_path):
            with open(assistants_yaml_path, 'w') as file:
                file.write('')  # 创建一个空文件
        # 使用绝对路径打开 assistants.yaml 文件
        with open(assistants_yaml_path, 'r') as file:
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
        with open(assistants_yaml_path, 'w') as file:
            yaml.dump(data, file)

    @property
    def id(self):
        return self.config.id

    @property
    def name(self):
        return self.config.name

    @name.setter
    def name(self, value):
        self.config.name = value
        self.save_to_yaml()  # 更新 YAML 文件

    @property
    def instructions(self):
        return self.config.instructions

    @instructions.setter
    def instructions(self, value):
        self.config.instructions = value

    @property
    def description(self):
        return self.config.description

    @description.setter
    def description(self, value):
        self.config.description = value

    @property
    def tools(self):
        return self.config.tools

    @tools.setter
    def tools(self, value):
        self.config.tools = value
        self.save_to_yaml()  # 更新 YAML 文件

    @property
    def model(self):
        return self.config.model

    @model.setter
    def model(self, value):
        self.config.model = value
        self.save_to_yaml()  # 更新 YAML 文件

    def get_tools_type_list(self):
        return [tool['type'] for tool in self.config.tools]

    @staticmethod
    def create(name: str = None, instructions: str = None, tools: list[dict] = [{'type':''}], model: str = 'gpt-4', description: str = None, file_ids: list = None) -> 'Assistants':
        # 创建配置和 Assistants 对象
        config = AssistantConfig(
            id=str(uuid.uuid4()),
            created_at=int(time.time()),
            name=name,
            description=description,
            instructions=instructions,
            tools=tools,
            model=model,
            file_ids=file_ids if file_ids is not None else [],
        )
        assistant = Assistants(config,YamlPathConfig.assistants_yaml_path)
        assistant.save_to_yaml()  # 保存到 YAML 文件
        return assistant
    
    @staticmethod
    def get_all_assistants() -> List[Dict[str, Any]]:
        """
        读取 YAML 文件并返回所有 assistants 的信息列表。
        """
        # 确保 YAML 文件路径已经被设置
        if not YamlPathConfig.assistants_yaml_path or not os.path.isfile(YamlPathConfig.assistants_yaml_path):
            raise FileNotFoundError("The assistants YAML file path is not set or the file does not exist.")

        # 读取 YAML 文件
        with open(YamlPathConfig.assistants_yaml_path, 'r') as file:
            assistants_data = yaml.safe_load(file) or []
        # 使用 from_dict 方法将每个字典转换为 AssistantConfig 实例
        assistants_list = []
        for item in assistants_data:
            config = AssistantConfig(**item)
            assistants_list.append(config)
        return assistants_list
    @classmethod
    def from_id(cls, id: str) -> 'Assistants':
        # 使用传入的 yaml_path 参数打开 YAML 文件
        with open(YamlPathConfig.assistants_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or []
        # 查找具有相同 id 的配置
        for d in data:
            if d['id'] == id:
                # 如果找到了，就用这个配置创建一个新的 Assistants 对象
                config = AssistantConfig(**d)
                return cls(config, YamlPathConfig.assistants_yaml_path)  # 使用传入的 yaml_path 创建 Assistants 实例
        # 如果没有找到，就抛出一个异常
        raise ValueError(f'No assistant with id {id} found in YAML file.')
    
    @classmethod
    def delete_by_id(cls, id: str):

        # 使用绝对路径打开 assistants.yaml 文件
        with open(YamlPathConfig.assistants_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or []

        # 查找具有相同 id 的 assistant
        for i, d in enumerate(data):
            if d['id'] == id:
                # 如果找到了，就删除它
                del data[i]
                break
        else:
            # 如果没有找到，就抛出一个异常
            raise ValueError(f'No assistant with id {id} found in YAML file.')

        # 写回 YAML 文件
        with open(YamlPathConfig.assistants_yaml_path, 'w') as file:
            yaml.dump(data, file)