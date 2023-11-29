# YORG Test Package

this is a test package

# test

```python
import yorg_test
import os
#os.environ['http_proxy'] = 'http://127.0.0.1:10809'  # 这里设置自己的代理端口号
#os.environ['https_proxy'] = 'http://127.0.0.1:10809'  # 这里设置自己的代理端口号
os.environ['OPENAI_CHAT_API_KEY'] = 'sk-br3j7Gxxxxxxxxvt8r'

threads = yorg_test.Threads.create('tools.yaml')
assistant = yorg_test.Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="Use swe tool auto fix code files", tools=[{'type':'SWEToolEntity'}])
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

pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple yorg-test==0.0.13