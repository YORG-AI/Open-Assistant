from .model import *
from .tool_entity import *


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
    
    def _get_next_stages_info(self) -> dict[str, list[Parameter]]:
        return self.current_stage.next_stage_entry 

    def call(self, **kwargs):
        res = self._call(**kwargs)
        return {
            **res,
            "next_stages_info": self._get_next_stages_info(),
        }

    @abstractmethod
    def _call(self, **kwargs):
        pass
        