from google.cloud import translate_v2 as translate
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.core.nodes.google.google_translate.google_translate_model import TranslateInput
from src.utils.router_generator import generate_node_end_points

google_translate_node_config = {
    "name": "google_translate",
    "description": "A node that interacts with Google's Translation services.",
    "functions": {
        "translate": "Translate text using Google's Translation services.",
    },
}

@generate_node_end_points
class GoogleTranslateNode(BaseNode):
    config: NodeConfig = NodeConfig(**google_translate_node_config)

    def __init__(self):
        super().__init__()
        self.client = translate.Client()

    def translate(self, input: TranslateInput):
        if input.source_language:
            result = self.client.translate(input.text, target_language=input.target_language, source_language=input.source_language)
        else:
            result = self.client.translate(input.text, target_language=input.target_language)
        return result['translatedText']
