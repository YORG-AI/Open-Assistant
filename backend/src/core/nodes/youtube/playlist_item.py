import os
import requests
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.utils.router_generator import generate_node_end_points
from src.core.nodes.youtube.youtube_model import RetrievePlaylistItemsInput
from src.core.nodes.youtube.youtube_model import RetrieveChannelInput


youtube_playlist_item_config = {
    "name": "youtube_playlist_item",
    "description": "Node related to YouTube Playlist Item operations.",
    "functions": {
        "retrieve_playlist_items": "Retrieve items from a specific YouTube Playlist.",
    },
}


@generate_node_end_points
class YouTubePlaylistItemNode(BaseNode):
    config: NodeConfig = NodeConfig(**youtube_playlist_item_config)

    def __init__(self):
        super().__init__()
        self.YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"
        self.API_KEY = os.getenv("YOUTUBE_API_KEY")

    def retrieve_playlist_items(self, input: RetrievePlaylistItemsInput):
        url = f"{self.YOUTUBE_API_ENDPOINT}/playlistItems?part=snippet&playlistId={input.playlist_id}&maxResults={input.max_results}&key={self.API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check if there's an error in the response
        if "error" in data:
            return {"error": data["error"]["message"], "details": data}

        if "items" in data:
            return data["items"]
        else:
            return {"error": "No items found in the playlist."}
