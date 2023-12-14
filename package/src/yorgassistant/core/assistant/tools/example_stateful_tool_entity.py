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
        if "goto" not in kwargs:
            if self.current_stage.name == self.config.start_stage:
                return {
                    "type": "success",
                    "content": {"message": "stateful tool is started"},
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
                return self._stage1(kwargs["x"])
            case "stage_2":
                return self._stage2(kwargs["y"])
            case "stage_3":
                return self._stage3()
            case self.config.finish_stage:
                return self._finish()
            case _:
                return {
                    "type": "error",
                    "content": {
                        "message": f"stage {self.current_stage.name} not found"
                    },
                }

    def _stage1(self, x: int):
        self.x = x
        return {"type": "success", "content": {"message": "stage1 done"}}

    def _stage2(self, y: int):
        self.y = y
        return {"type": "success", "content": {"message": "stage2 done"}}

    def _stage3(self):
        return {"type": "success", "content": {"result": self.x + self.y}}

    def _finish(self):
        return {"type": "success", "content": {"message": "stateful tool is finished"}}
