from .stateful_tool_entity import *


class ExampleStatefulToolEntity(StatefulToolEntity):
    """
    This example tool entity is stateful, and it has 3 inner stages.

    stage1: take integer x as input
    stage2: take integer y as input
    stage3: no input, return x + y
    """

    def __init__(self):
        super().__init__("example_stateful_tool.yaml")

    def _call(self, **kwargs):
        request_next_stage = kwargs["request_next_stage"]
        if request_next_stage in self.current_stage.next_stage_entry:
            self.current_stage = self.config.all_stages[request_next_stage]

        match self.current_stage.name:
            case "stage1":
                return self._stage1(kwargs["x"])
            case "stage2":
                return self._stage2(kwargs["y"])
            case "stage3":
                return self._stage3()
            case _:
                raise Exception(f"Stage {self.current_stage} not found.")

    def _stage1(self, x: int):
        self.x = x
        return {"type": "success", "content": {"message": "stage1 done"}}

    def _stage2(self, y: int):
        self.y = y
        return {"type": "success", "content": {"message": "stage2 done"}}

    def _stage3(self):
        return {"type": "success", "content": {"result": self.x + self.y}}
    
