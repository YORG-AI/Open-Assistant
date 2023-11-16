from .model import *
from .tool_entity import *
from src.core.nodes.openai.openai import OpenAINode
from src.core.nodes.openai.openai_model import *
from src.core.assistant.prompt.few_shot_extract_parametes_from_input import *
import json
class StatefulToolEntityConfig(BaseModel):
    start_stage: str = Field(description="The start stage of the tool entity.")
    finish_stage: str = Field(description="The finish stage of the tool entity.")
    all_stages: dict[str, Stage] = Field(description="All stages of the tool entity.")


class StatefulToolEntity(BaseToolEntity, ABC):
    config: StatefulToolEntityConfig
    current_stage: Stage

    def __init__(self, config_file_name: str):
        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 构建 example_stateful_tool.yaml 文件的绝对路径
        config_path = os.path.join(current_dir, config_file_name)

        # 使用绝对路径打开 assistants.yaml 文件
        with open(config_path, "r") as file:
            data = yaml.safe_load(file) or []

        self.config = StatefulToolEntityConfig(**data)
        self.current_stage = self.config.all_stages[self.config.start_stage]

    def is_stateful(self) -> bool:
        return True

    def current_state(self):
        if self.current_stage.name == self.config.finish_stage:
            return State.DONE
        elif self.current_stage.name == self.config.start_stage:
            return State.IDLE
        else:
            return State.RUNNING

    def need_llm_generate_parameters(self) -> bool:
        return self.current_stage.need_llm_generate_parameters

    def need_llm_generate_response(self) -> bool:
        return self.current_stage.need_llm_generate_response
    
    def _get_next_stages_info(self) -> dict[str, list[dict]]:
        return self.current_stage.dict()["next_stage_entry"]

    def call(self, **kwargs):
        if "goto" in kwargs:
            cur_stage_entry = self._get_next_stages_info()
            parameter_info = cur_stage_entry[next(iter(cur_stage_entry))]
            input_text = kwargs['input_text']
            if len(parameter_info)>0:
                print(f"kwargs['input_text']:{input_text},parameter_info:{parameter_info}")
                #通过input_text和parameter_info去判断是否有值，如果没有则return error 让他重新输入
                parametes = self._extract_parametes(input_text,parameter_info)
                if len(parametes)==0:
                    return{
                        "type": "error",
                        "assistant": {"message": "Please enter the corresponding parameter value correctly"},
                    }
                else:
                    kwargs.update(parametes)
        
        print(f'kwargs:{kwargs}')
        res = self._call(**kwargs)
        # 正常的应该是我这里处理还是上层处理assistant对话
        return {
            **res,
            "next_stages_info": self._get_next_stages_info(),
        }

    def _extract_parametes(self,input_text:str,parameter_info:list):
        # 创建一个 OpenAINode 对象
        parametes_node = OpenAINode()
        parametes_node.add_system_message(EXTRACT_PARAMETES_PROMPT+EXTRACT_PARAMETES_EXAMPLE_PROMPT+EXTRACT_PARAMETES_HINT)
        prompt = f"""\nTextual content (input_text):{input_text}\nParameter information (parameter_info):{parameter_info}\nGenerated parameter reference dictionary:\n"""
        message_config = Message(role="user", content=prompt)


        # 创建一个 ChatInput 对象
        chat_config = ChatWithMessageInput(
            message=message_config,
            model="gpt-4-1106-preview",
            append_history=False,
            use_streaming=False,
        )
        
        # response = parametes_node.chat_with_message(chat_config).message.content
        # parametes = json.loads(response)
        
        while True:
            try:
                response = parametes_node.chat_with_message(chat_config).message.content
                parametes = json.loads(response)
                break
            except json.JSONDecodeError:
                continue

        return parametes

        
    @abstractmethod
    def _call(self, **kwargs):
        pass
        