from markdown import markdown
from ipykernel.kernelbase import Kernel
from src.core.nodes import (
    OpenAINode,
    ChatInput,
)

from .handler import Handler, HandlerInput


class GPTHandler(Handler):
    def __init__(self, kernel: Kernel):
        super().__init__(kernel)

        self.openai_node = OpenAINode()
        self.selected_value = None

    def handle(
        self,
        input: HandlerInput,
        silent: bool,
        store_history: bool,
        user_expressions: any,
        allow_stdin: bool,
    ):        
        code = input.code

        resp = self.openai_node.chat(
            ChatInput(
                message_text=code,
                model="gpt-3.5-turbo",
            )
        )

        html_content = markdown(resp.message.content)
        self.kernel.send_response(
            self.kernel.iopub_socket,
            "display_data",
            {"data": {"text/html": html_content}},
        )

    def do_shutdown(self, restart: bool):
        pass
