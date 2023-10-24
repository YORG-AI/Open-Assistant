import os
import requests
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.utils.router_generator import generate_node_end_points
from src.core.nodes.youtube.youtube_model import RetrieveVideoInput, RateVideoInput

youtube_video_config = {
    "name": "youtube_video",
    "description": "Node related to YouTube Video operations.",
    "functions": {
        "retrieve_video": "Retrieve details of a specific YouTube Video.",
        # "rate_video": "Rate a specific YouTube Video."
    },
}


@generate_node_end_points
class YouTubeVideoNode(BaseNode):
    config: NodeConfig = NodeConfig(**youtube_video_config)

    def __init__(self):
        super().__init__()
        self.YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"
        self.API_KEY = os.getenv("YOUTUBE_API_KEY")

    def retrieve_video(self, input: RetrieveVideoInput):
        url = f"{self.YOUTUBE_API_ENDPOINT}/videos?part=snippet&id={input.video_id}&key={self.API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check if there's an error in the response
        if "error" in data:
            return {"error": data["error"]["message"], "details": data}

        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]
        else:
            return {"error": "Video not found."}

    # Note: API keys are not supported by this API. Expected OAuth2 access token or other authentication credentials that assert a principal

    # def rate_video(self, input: RateVideoInput):
    #     url = f"{self.YOUTUBE_API_ENDPOINT}/videos/rate?id={input.video_id}&rating={input.rating}&key={self.API_KEY}"
    #     response = requests.post(url)
    #     if response.status_code == 204:
    #         return {"message": f"Video successfully rated with {input.rating}"}
    #     else:
    #         return {
    #             "error": "Failed to rate the video.",
    #             "details": response.text
    #         }
