from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.hello.hello_model import HelloWorldInput, HelloWithNameInput
from src.utils.router_generator import generate_node_end_points
from src.service.redis import Redis

hello_node_config = {
    "name": "hello",
    "description": "A simple node that is capable of saying hello.",
    "functions": {
        "hello_world": "Say hello to the world.",
        "hello_with_name": "Say hello to someone with a name.",
        "test": "Test.",
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
        return f"Hello, {input.name}."

    def test(self, input: HelloWithNameInput):
        redis = Redis()
        redis.set("jyx", "hello")
        return redis.get("jyx")
