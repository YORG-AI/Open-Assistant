import pytest
from src.core.assistant.threads import Threads
from src.core.assistant.assistant import Assistants

def test_threads_create():
    # 创建一个 Threads 对象
    threads = Threads.create()

    # 检查 id 是否被正确设置
    assert threads.config.id is not None
    assert isinstance(threads.config.id, str)

    # 检查其他属性的默认值
    assert threads.config.object == "thread"
    assert threads.config.assistant_id is None
    assert threads.config.metadata == {}

def test_threads_run():
    # 创建一个 Threads 对象  
    threads = Threads.create()
    # 创建一个助手并保存到 assistants.yaml 文件
    assistant = Assistants.create(name="Test Assistant", model="gpt-4-1106-preview", instructions="run code", tools=[{'type':'code_interpreter'}])
    # 运行 Threads 对象
    result = threads.run(assistant.id, "Tell me the answer of 12th fibonacci number plus 15th prime.")
    print(result)
    # 运行 Threads 对象
    result = threads.run(assistant.id, "Tell me the answer of 17th fibonacci number plus 20th prime.")
    print(result)

    print(threads.config.message_history)
