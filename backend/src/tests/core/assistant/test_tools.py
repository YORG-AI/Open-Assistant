import pytest
from src.core.assistant.tools.tools import Tools

def test_tools():
    # 创建一个 Tools 对象
    tools = Tools()

    # 测试 call 方法
    result = tools.get_tool('code_interpreter').call(text="print('Hello, world!')")
    assert result == {'type':'success','context':'test success'}

    # 测试当工具名称不存在时，call 方法应该抛出一个异常
    with pytest.raises(ValueError):
        tools.get_tool('nonexistent_tool')