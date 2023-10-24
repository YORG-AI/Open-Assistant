from pydantic import BaseModel

PROMPT_TEMPLATE = """
# You are a senior software engineer at Microsoft. You are working on this AI agent project. AI agents are capable of using "nodes" to assess third-party APIs, thereby using them as tools.

## Repo Structure
-nodes/
--base_node.py
--hello/
---hello.py
---hello_model.py
##

## Base Class to be extended (nodes/base_node.py)

{base_node_code}

##

I want you to write a new "node" for me. This is for production, NOT an exercise / school quiz! 
The node will serve as a package, with which the program calls third part APIs.

## Example node and subclass 

{example_node_code}

###
##

Now, your task is to write me the "node" (based on the example above) for {node_name}. This node is able to perform these functions/operations:

{operations_list}

----------------------

Recommendation: 
1. Prioritize the use of Python SDK  (over "calling requests API") if possible.
2. Add "try catch" for error handling, if necessary. 

Output：
1. First tell me which documentation you are relying on (you should try to find the official documentation, even if it is not a Python SDK approach).
2. Required permissions and things that I, human, need to prepare (to run and test the code). Output in Python code triple quote form.
3. Then give me detailed instructions, including all the code!!! Remember to put code in different files as the example above, the model input parameters depend on the API input.

----------------------

You should highly obey the type of the example code block, otherwise it will not be able to run.
The content in brackets is just a hint, do not copy them. Don't add any extra text, just follow format.
Your code should be in the following format:

{format_example}
"""


BASE_NODE_CODE = """
from typing import Callable
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

class NodeInput(BaseModel):
    func_name: str
    func_input: BaseModel

class NodeConfig(BaseModel):
    name: str = Field(description="Node 名称")
    description: str = Field(default="", description="Node 描述")
    functions: dict[str, str] = Field(default=\{\}, description="Node 所有功能描述")

class BaseNode(ABC):
    config: NodeConfig
    func_mapping: dict[str, Callable]

    def __init__(self):
        # initialize func_mapping
        self.func_mapping = \{\}
        avail_funcs = [
            func_name for func_name in dir(self) if not func_name.startswith("_")
        ]
        for func_name in self.config.functions.keys():
            if func_name not in avail_funcs:
                raise Exception(
                    f"Node \{self.config.name\} does not contain \{func_name\} method."
                )
            else:
                self.func_mapping[func_name] = getattr(self, func_name)

     def run(self, input: NodeInput):
        if input.func_name not in self.func_mapping.keys():
            raise Exception(
                f"Node {self.config.name} does not contain {input.func_name} method."
            )
        else:
            self.func_mapping[input.func_name](input.func_input)
"""


NODE_EXAMPLE = """
### nodes/hello/hello.py

from src.core.base_node import BaseNode, NodeConfig
from src.core.nodes.hello.hello_model import HelloWorldInput, HelloWithNameInput
from src.utils.router_generator import generate_node_end_points

hello_node_config = {
    "name": "hello",
    "description": "A simple node that is capable of saying hello.",
    "functions": {
        "hello_world": "Say hello to the world.",
        "hello_with_name": "Say hello to someone with a name.",
    },
}

@generate_node_end_points
class HelloNode(BaseNode):
    config: NodeConfig = NodeConfig(**hello_node_config)

    def __init__(self):
        super().__init__()

    def hello_world(self, input: HelloWorldInput):
        return f"Hello world!"

    def hello_with_name(self, input: HelloWithNameInput):
        return f"Hello, \{input.name\}."

### nodes/hello/hello_model.py

from pydantic import BaseModel

class HelloWorldInput(BaseModel):
    pass

class HelloWithNameInput(BaseModel):
    name: str

"""


FORMAT_EXAMPLE = """
## Reference Documentation (must be a python list of links)
```python
[
    "https://docs...",
]

## Requirements (must be a python list of tuples, each tuple contains two string, first is description, second is content)
```python
[
    ("description ...", "content ..."),
]
```

## Code Content (must be a python list of tuples, each tuple contains two string, first is file path, second is file content)
```python
[
    ("path/to/file", "file_content ..."),
]
```
"""


OUTPUT_SCHEMA = {
    "Reference Documentation": (list[str], ...),
    "Requirements": (list[tuple[str, str]], ...),
    "Code Content": (list[tuple[str, str]], ...),
}


class Operations(BaseModel):
    contents: dict[str, list[str]]

    def __str__(self):
        res = ""
        for key, value in self.contents.items():
            res += f"- {key}\n"
            for item in value:
                res += f"  - {item}\n"
        return res