from src.core.assistant.base_assistant import BaseAssistant,AssistantConfig
import uuid
import time
import yaml

class Assistants(BaseAssistant):
    def __init__(self, config):
        super().__init__(config)
    
    def save_to_yaml(self):
        import os

        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建 assistants.yaml 文件的绝对路径
        assistants_yaml_path = os.path.join(current_dir, 'assistants.yaml')

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
        with open('assistant.yaml', 'w') as file:
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

    @staticmethod
    def create(name: str, instructions: str, tools: list[dict], model: str) -> 'Assistants':
        # 创建配置和 Assistants 对象
        config = AssistantConfig(
            id=str(uuid.uuid4()),
            created_at=int(time.time()),
            name=name,
            instructions=instructions,
            tools=tools,
            model=model,
        )
        assistant = Assistants(config)
        assistant.save_to_yaml()  # 保存到 YAML 文件
        return assistant
    @classmethod
    def from_id(cls, id: str) -> 'Assistants':
        import os

        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建 assistants.yaml 文件的绝对路径
        assistants_yaml_path = os.path.join(current_dir, 'assistants.yaml')

        # 使用绝对路径打开 assistants.yaml 文件
        with open(assistants_yaml_path, 'r') as file:
            data = yaml.safe_load(file) or []
        # 查找具有相同 id 的配置
        for d in data:
            if d['id'] == id:
                # 如果找到了，就用这个配置创建一个新的 Assistants 对象
                config = AssistantConfig(**d)
                return cls(config)
        # 如果没有找到，就抛出一个异常
        raise ValueError(f'No assistant with id {id} found in YAML file.')