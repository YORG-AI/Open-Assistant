# YORG Test Package

this is a test package

# test version

## how to use

- Set up test version package
``` shell
pip install  yorgassistant
```
- Set up openapikey
(If you are in China, please set up a proxy to ensure that you can connect to openai.)
```python
import os
#os.environ['http_proxy'] = 'http://127.0.0.1:10809'  # 这里设置自己的代理端口号
#os.environ['https_proxy'] = 'http://127.0.0.1:10809'  # 这里设置自己的代理端口号
os.environ['OPENAI_CHAT_API_KEY'] = 'sk-br3j7Gxxxxxxxxvt8r'
```
- set up yaml file
We have some tools built in eg.code_interpreter,swe_tool

tools.yaml
```yaml
YORG: 0.0.1
info:
  title: yorg_tools_document
  description: yorg tool define document.
  version: 'v1'
tools:
  code_interpreter:
    name: code_interpreter
    entity_name: code_interpreter
    summary: Run the code through code_interpreter and return the result of the code run. If your query is about math, computer science, or data science, you can use this tool to get the result of the code run.
    parameters:
      - name: code
        description: code text that requires code_interpreter to run
        required: true
        parameter_schema:
          type: string
    responses:
      success:
        description: OK
        content:
          result:
            type: string
            description: the result of the code run
  example_stateful_tool:
    name: example_stateful_tool
    entity_name: example_stateful_tool
    summary: This tool is an example of a stateful tool. It will get two number from user input and return the sum of the two numbers.
    parameters: []
    responses: {}  
  swe_tool:
    name: sew_tool
    entity_name: swe_tool
    summary: SoftWare Engineer Agent(swe_tool) specializes in working with code files.
    parameters: []
    responses: {}  
```
Tools are categorized into stateful tools and function tools,
Function tools can describe parameters and return values directly in tools.yaml
Functions can be registered using decorators
```python
from yorgassistant.core.assistant.tools.tools import register_function_tool
@register_function_tool
def code_test(code: str):
    return {
        "type": "success",
        "content": {
            "result": "Hello, World!",
        },
    }
```
If it's a stateful tool you need to write an additional yaml file with a stateful description

example_stateful_tool.yaml
```yaml
start_stage: "init"
finish_stage: "finish"
all_stages:
  init:
    name: "init"
    next_stage_entry: 
      stage_1:
        - name: x
          required: true
          parameter_schema:
            type: number
            description: "input value x"
    need_llm_generate_parameters: false
    need_llm_generate_response: false
  stage_1:
    name: "stage_1"
    next_stage_entry: 
      stage_2:
        - name: y 
          required: true
          parameter_schema:
            type: number
            description: "input value y"
    need_llm_generate_parameters: false 
    need_llm_generate_response: false
  stage_2:
    name: "stage_2"
    next_stage_entry: 
      stage_3: []
    need_llm_generate_parameters: false
    need_llm_generate_response: false
  stage_3:
    name: "stage_3"
    next_stage_entry: 
      finish: []
    need_llm_generate_parameters: false
    need_llm_generate_response: false
  finish:
    name: "finish"
    next_stage_entry: {}
    need_llm_generate_parameters: false
    need_llm_generate_response: false
```
Stateful tools can also be registered using decorators.
The yaml file is registered in init.
```python
from yorgassistant.core.assistant.tools.tools import register_stateful_tool
from yorgassistant.core.assistant.tools.stateful_tool_entity import StatefulToolEntity
@register_stateful_tool
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
```
- setting data
```python
import yorgassistant
yorgassistant.Threads.set_threads_yaml_path('data/threads.yaml')
yorgassistant.Assistants.set_assistants_yaml_path('data/assistants.yaml')
```
- find assistants
```python
import yorgassistant
assistants_list = yorgassistant.Assistants.get_all_assistants()
print(assistants_list)
```
- run example

```python
import yorgassistant
yorgassistant.Threads.set_threads_yaml_path('data/threads.yaml')
yorgassistant.Assistants.set_assistants_yaml_path('data/assistants.yaml')
threads = yorgassistant.Threads.create('tools.yaml')
assistant = yorgassistant.Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="Use swe tool auto fix code files", tools=[{'type':'swe_tool'}])
print(assistant.id)
# 运行 Threads 对象
result = threads.run(assistant.id, "Use SoftWare Engineer Agent swe tool auto fix code files.")
print(result)

result = threads.run(assistant.id, "the repo url is https://github.com/YORG-AI/Open-Assistant",goto="stage_1")
print(result)

result = threads.run(assistant.id, "add helloworld feature to readme",  goto="stage_2")
print(result)

result = threads.run(assistant.id, "focus_files_name_list = [README.md]", goto="stage_3")
print(result)

result = threads.run(assistant.id, "action=3", goto="stage_4")
print(result)

result = threads.run(assistant.id, "", goto="stage_5")
print(result)

result = threads.run(assistant.id, "action=0,action_idx=0", goto="stage_6")
print(result)

result = threads.run(assistant.id, "", goto="finish")
print(result)
```

