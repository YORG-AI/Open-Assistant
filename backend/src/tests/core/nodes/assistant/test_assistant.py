import pytest
from src.core.assistant.assistant import Assistants

def test_assistant_creation():
    # 使用这个配置创建一个新的 Assistants 对象
    assistant = Assistants.create(name="test_name",instructions="test_instructions",tools=[{'type':'code_interpreter'}],model="test_model")
    # 检查新创建的 Assistants 对象的属性是否符合预期
    assert assistant.name == "test_name"
    assert assistant.instructions == "test_instructions"
    assert assistant.tools == [{'type':'code_interpreter'}]
    assert assistant.model == "test_model"

# def test_assistant_from_id():
#     # 使用一个存在的 id 创建一个新的 Assistants 对象
#     assistant = Assistants.from_id("existing_id")
#     # 检查新创建的 Assistants 对象的属性是否符合预期
#     assert assistant.id == "existing_id"
#     # 这里你可以添加更多的 assert 语句来检查其他的属性

# def test_assistant_from_id_with_non_existing_id():
#     # 使用一个不存在的 id 创建一个新的 Assistants 对象
#     # 这应该会抛出一个 ValueError 异常
#     with pytest.raises(ValueError):
#         assistant = Assistants.from_id("non_existing_id")