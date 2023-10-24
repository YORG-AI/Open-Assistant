import os
import requests
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.utils.router_generator import generate_node_end_points
from src.core.nodes.youtube.youtube_model import (
    RetrieveChannelInput,
    UpdateChannelInput,
    UploadChannelBannerInput,
)

youtube_channel_config = {
    "name": "youtube_channel",
    "description": "Node related to YouTube Channel operations.",
    "functions": {
        "retrieve_channel": "Retrieve a specific YouTube Channel.",
        # "update_channel": "Update details of a YouTube Channel.",
        # "upload_channel_banner": "Upload a banner for a YouTube Channel."
    },
}


@generate_node_end_points
class YouTubeChannelNode(BaseNode):
    config: NodeConfig = NodeConfig(**youtube_channel_config)

    def __init__(self):
        super().__init__()
        self.YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"
        self.API_KEY = os.getenv("YOUTUBE_API_KEY")
        print("API key: " + self.API_KEY)

    def retrieve_channel(self, input: RetrieveChannelInput):
        url = f"{self.YOUTUBE_API_ENDPOINT}/channels?part=snippet&id={input.channel_id}&key={self.API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check if there's an error in the response
        if "error" in data:
            return {"error": data["error"]["message"], "details": data}

        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]
        else:
            return {"error": "Channel not found."}

    # Note: The YouTube API does not provide a direct way to update a channel's name using the API Key.

    # def update_channel(self, input: UpdateChannelInput):
    #     # Note: The YouTube API does not provide a direct way to update a channel's name using the API Key.
    #     # This is just a placeholder method.
    #     return {
    #         "error": "Updating a channel's name via API Key is not supported by YouTube API."
    #     }

    # Note: The YouTube API does not provide a direct way to upload a channel banner using the API Key.

    # def upload_channel_banner(self, input: UploadChannelBannerInput):
    #     # This is just a placeholder method.
    #     return {
    #         "error": "Uploading a channel banner via API Key is not supported by YouTube API."
    #     }
