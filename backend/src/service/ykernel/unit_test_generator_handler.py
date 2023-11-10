from typing import Optional
from enum import Enum
from markdown import markdown
from ipykernel.kernelbase import Kernel
from ipykernel.comm import Comm
from ipywidgets import widgets
import logging
from .handler import Handler, HandlerInput
import re

from src.service.ykernel.swe_agent_handler import _auto_retry

from src.core.agents.unit_test.unit_test import (
    UnitTestAgent,
)


class Stage(str, Enum):
    INIT = "init"
    CHECK = 'check'
    REGENERATE = 'regenerate'
    ACCEPT = 'accept'
    GENERATE = 'generate'
    # DONE = "done"

class StatefulUnitTestAgent:
    def __init__(self, agent: UnitTestAgent, handler: Handler):
        self.agent = agent
        self.current_stage = Stage.INIT
        self.handler = handler
        self.resp = ''
        self.previous_unit_test = []
        self.input_content = []
        self.unit_test_res = []

    def _next(self):
        match self.current_stage:
            case Stage.INIT:
                self._on_init()
            case Stage.CHECK:
                self._on_check()
            case Stage.GENERATE:
                self._on_generate()
            case Stage.REGENERATE:
                self._on_regenerate()
            case Stage.ACCEPT:
                self._send_markdown("Task done.")

    @_auto_retry(Stage.INIT)
    def _on_init(self):
        self._send_markdown(
            "Please provide the code that you want to generate unit test."
        )

        input_code = widgets.Textarea(
            value="",
            placeholder="Type something",
            description='Input code:',
            disabled=False,
        )
        confirm_button = widgets.Button(
            Value=False,
            description="Confirm",
            disabled=False,
            button_style="",
            tooltip="Description",
            icon="check",
        )

        # confirm之后，接收用户发送的code，转接到ChatGPT获得unit test代码
        def confirm_button_clicked(b):

            self.input_content.append(input_code.value)
            self.agent.set_input_code(input_code.value)
            self._send_markdown(
                "User Code: \n ``` \n" + input_code.value + "\n```"
            )

            self._send_markdown(
                "\nAgent is generating the answer... \n"
            )
            self.resp = self.agent._generate_unit_test()
            self._send_markdown(self.resp)
            self.current_stage = Stage.GENERATE
            self._on_generate()



        vbox = widgets.VBox([input_code, confirm_button])
        confirm_button.on_click(confirm_button_clicked)
        self._send_widget(vbox)

    @_auto_retry(Stage.GENERATE)
    def _on_generate(self):
        python_code = extract_python_code(self.resp)

        self.handler._send_comm_obj(
            "custom_insert_cell",
            {"type": "generate_unit_test", "code": python_code}
        )


    @_auto_retry(Stage.REGENERATE)
    def _on_regenerate(self):
        resp = self.agent._generate_unit_test()
        self._send_markdown(resp)
        python_code = extract_python_code(resp)

        self.handler._send_comm_obj(
            "custom_insert_cell",
            {"type": "regenerate_unit_test", "code": python_code}
        )

    @_auto_retry(Stage.CHECK)
    def _on_check(self):
        accept_button = widgets.Button(
            value=False,
            description="Accept",
            disabled=False,
            button_style="",
            tooltip="Description",
            icon="check",
        )

        regenerate_button = widgets.Button(
            value=False,
            description="Regenerate",
            disabled=False,
            button_style="",
            tooltip="Description",
            icon="check",
        )

        def accept_button_clicked(b):
            self.current_stage = Stage.ACCEPT
            # disable all button
            regenerate_button.disabled = True
            self._next()

        def regenerate_button_clicked(b):
            self.current_stage = Stage.REGENERATE
            self._on_regenerate()
            accept_button.disabled = True
            # self._next()

        hbox = widgets.HBox([accept_button, regenerate_button])

        accept_button.on_click(accept_button_clicked)
        regenerate_button.on_click(regenerate_button_clicked)
        self._send_widget(hbox)

    def _send_widget(self, widget: widgets.Widget):
        self.handler._send_widget(widget)

    def _send_markdown(self, content: str):
        self.handler._send_markdown(content)


class UnitTestAgentHandler(Handler):
    def __init__(self, kernel: Kernel):
        super().__init__(kernel)

        self.agents = StatefulUnitTestAgent(
                UnitTestAgent(), self
            )
        self.unit_test_code_cell = []


    def handle(
        self,
        input: HandlerInput,
        silent: bool,
        store_history: bool,
        user_expressions: any,
        allow_stdin: bool,
    ):
        if input.cell_id is None:
            raise Exception("cell_id is None")

        match input.cell_type:
            case "unit_test":
                # print('unit_test cell: ')
                self.agents.current_stage = Stage.INIT
                self.agents._next()

            case "generate_unit_test":
                # if input.cell_id not in self.unit_test_code_cell:
                #     self.unit_test_code_cell.append(input.cell_id)
                #     self.agents.input_content.append(input.code)
                self.agents.current_stage = Stage.CHECK
                self.agents._next()
                # self.agents._next()
            case "regenerate_unit_test":
                self.agents.current_stage = Stage.CHECK
                self.agents._next()


    def get_unit_test_code(self):
        return self.unit_test_code_cell

    def do_shutdown(self, restart: bool):
        pass

def extract_python_code(code: str):
    pattent1 = re.compile("```Python([\s\S]*)```")
    pattent2 = re.compile("```python([\s\S]*)```")
    result = pattent1.findall(code) if pattent1.findall(code) else pattent2.findall(code)
    return ''.join(result)
