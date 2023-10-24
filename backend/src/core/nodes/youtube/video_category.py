import os
import requests
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.utils.router_generator import generate_node_end_points
from src.core.nodes.youtube.youtube_model import RetrieveVideoCategoriesInput

youtube_video_category_config = {
    "name": "youtube_video_category",
    "description": "Node related to YouTube Video Category operations.",
    "functions": {
        "retrieve_video_categories": "Retrieve video categories for a given region."
    },
}


@generate_node_end_points
class YouTubeVideoCategoryNode(BaseNode):
    config: NodeConfig = NodeConfig(**youtube_video_category_config)

    def __init__(self):
        super().__init__()
        self.YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"
        self.API_KEY = os.getenv("YOUTUBE_API_KEY")

    def retrieve_video_categories(self, input: RetrieveVideoCategoriesInput):
        url = f"{self.YOUTUBE_API_ENDPOINT}/videoCategories?part=snippet&regionCode={input.region_code}&key={self.API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check if there's an error in the response
        if "error" in data:
            return {"error": data["error"]["message"], "details": data}

        if "items" in data and len(data["items"]) > 0:
            return data["items"]
        else:
            return {"error": "No video categories found for the given region."}
