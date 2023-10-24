from markdown import markdown
from ipykernel.kernelbase import Kernel

from .handler import Handler, HandlerInput


class DisplayHandler(Handler):
    def __init__(self, kernel: Kernel):
        super().__init__(kernel)

    def handle(
        self,
        input: HandlerInput,
        silent: bool,
        store_history: bool,
        user_expressions: any,
        allow_stdin: bool,
    ):
        html_content = markdown(
            """
# Heading
## Sub-heading

Paragraphs are separated
by a blank line.

Text attributes *italic*, **bold**,
`monospace`, ~~strikethrough~~.

A [link](http://example.com).

```python
#### hello world

print("hello world")
def add(a, b):
    return a + b

# hello
```
""",
            extensions=["fenced_code", "codehilite"],
            extension_configs={
                "codehilite": {
                    "use_pygments": True,
                    "css_class": "highlight",
                    "pygments_style": "solarized-light",
                    "guess_lang": False,
                },
            },
        )
        self.kernel.send_response(
            self.kernel.iopub_socket,
            "display_data",
            {
                "data": {
                    "text/html": html_content,
                }
            },
        )
        self.kernel.send_response(
            self.kernel.iopub_socket,
            "display_data",
            {
                "data": {
                    "text/plain": html_content,
                }
            },
        )

    def do_shutdown(self, restart: bool):
        pass
