import os
import requests
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.utils.router_generator import generate_node_end_points
from src.core.nodes.youtube.youtube_model import RetrievePlaylistInput
from src.core.nodes.youtube.youtube_model import RetrieveChannelInput

youtube_playlist_config = {
    "name": "youtube_playlist",
    "description": "Node related to YouTube Playlist operations.",
    "functions": {
        "retrieve_playlist": "Retrieve a specific YouTube Playlist.",
    },
}


@generate_node_end_points
class YouTubePlaylistNode(BaseNode):
    config: NodeConfig = NodeConfig(**youtube_playlist_config)

    def __init__(self):
        super().__init__()
        self.YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"
        self.API_KEY = os.getenv("YOUTUBE_API_KEY")

    def retrieve_playlist(self, input: RetrievePlaylistInput):
        url = f"{self.YOUTUBE_API_ENDPOINT}/playlists?part=snippet&id={input.playlist_id}&key={self.API_KEY}"
        response = requests.get(url)
        data = response.json()

        # Check if there's an error in the response
        if "error" in data:
            return {"error": data["error"]["message"], "details": data}

        if "items" in data and len(data["items"]) > 0:
            return data["items"][0]
        else:
            return {"error": "Playlist not found."}
