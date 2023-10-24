from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.deepl.deepl_model import TranslateInput
from src.utils.router_generator import generate_node_end_points
from decouple import config
import requests

DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = config('DEEPL_API_KEY')

deepl_node_config = {
    "name": "deepl",
    "description": "A node that uses DeepL for translation.",
    "functions": {
        "translate": "Translate text using DeepL."
    },
}

@generate_node_end_points
class DeepLNode(BaseNode):
    config: NodeConfig = NodeConfig(**deepl_node_config)

    def __init__(self):
        super().__init__()

    def translate(self, input: TranslateInput):
        payload = {
            "auth_key": DEEPL_API_KEY,
            "text": input.text,
            "target_lang": input.target_language
        }
        if input.source_language:
            payload["source_lang"] = input.source_language

        try:
            response = requests.post(DEEPL_API_URL, data=payload)
            response.raise_for_status()
            data = response.json()
            return data['translations'][0]['text']
        except requests.RequestException as e:
            return f"Error: {e}"
