# from serpapi import GoogleSearch
# from src.core.nodes.base_node import BaseNode, NodeConfig
from pydantic import BaseModel

class GoogleSearchInput(BaseModel):
    q:str
    location: str = "United States"
    hl:str = "en"
    gl: str =  "us"
    google_domain: str = "google.com"


class BaiduSearchInput(BaseModel):
    engine:str = "baidu"
    q: str

class BingSearchInput(BaseModel):
    engine: str = "bing"
    q:str
    cc: str = "US"

class GoogleImageSearchInput(BaseModel):
    engine:str = "google_images"
    q:str
    location: str = "United States"

class GoogleReverseImageSearchInput(BaseModel):
    engine: str = "google_reverse_image"
    image_url: str
    
class GoogleScholarSearchInput(BaseModel):
    engine: str = "google_scholar"
    q: str

class YoutubeSearchInput(BaseModel):
    engine: str = "youtube"
    search_query: str



