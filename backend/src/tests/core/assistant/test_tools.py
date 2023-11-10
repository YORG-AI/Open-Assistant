import pytest
from src.core.assistant.tools import Tools

def test_tools():
    # 创建一个 Tools 对象
    tools = Tools()

    # 测试 call 方法
    result = tools.call('code_interpreter', {'text': "print('Hello, world!')"})
    assert result == {'type':'success','context':'test success'}

    # 测试当工具名称不存在时，call 方法应该抛出一个异常
    with pytest.raises(ValueError):
        tools.call('nonexistent_tool', {})