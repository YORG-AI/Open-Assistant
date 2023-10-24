from serpapi import GoogleSearch,BaiduSearch
from src.core.nodes.base_node import BaseNode, NodeConfig
from src.utils.router_generator import generate_node_end_points
from src.core.nodes.serp.serp_model import (GoogleSearchInput, BaiduSearchInput, BingSearchInput, GoogleImageSearchInput, 
                                            GoogleReverseImageSearchInput, GoogleScholarSearchInput, YoutubeSearchInput)
import os
serp_node_config = {
    "name": "serp",
    "description": "A node that scrape and parse search results from Google, Baidu, Bing etc.",
    "functions": {
        "google_search": "scrape and parse search results from google",
        "baidu_search": "scrape and parse search results from baidu",
        "bing_search": "scrape and parse search results from bing",
        "google_images_search": "scrape and parse search results from google images",
        "google_reverse_images_search": "scrape and parse search results from google revsere images using image url",
        "google_scholar_search": "scrape and parse search results from google scholar",
        "youtube_search": "scrape and parse search results from youtube"
    },
}
@generate_node_end_points
class SerpNode(BaseNode):
    config: NodeConfig = NodeConfig(**serp_node_config)

    def __init__(self):
        super().__init__()
    
    def google_search(self, input:GoogleSearchInput):
        params = {
            "q": input.q, 
            "location": input.location,
            "api_key":  os.getenv("SERP_API_KEY"),
            "hl": input.hl,
            "gl": input.gl,
            "google_domain":input.google_domain
        }
        search = GoogleSearch(params)
        results = search.get_dict() 
        return results
    
    def baidu_search(self,input:BaiduSearchInput):
        params = {
            "engine": input.engine,
            "q": input.q,
            "api_key":  os.getenv("SERP_API_KEY")
        }
        search = BaiduSearch(params)
        results = search.get_dict()
        return results
    
    def bing_search(self, input:BingSearchInput):
        params = {
            "engine": input.engine,
            "q": input.q,
            "cc": input.cc,
            "api_key":  os.getenv("SERP_API_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results
    
    def google_images_search(self, input:GoogleImageSearchInput):
        params = {
            "engine": input.engine,
            "q": input.q,
            "location": input.location,
            "api_key":  os.getenv("SERP_API_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results

    def google_reverse_images_search(self, input:GoogleReverseImageSearchInput):
        params = {
            "engine": input.engine,
            "image_url": input.image_url,
            "api_key":  os.getenv("SERP_API_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results

    def google_scholar_search(self, input: GoogleScholarSearchInput):
        params = {
        "engine": input.engine,
        "q": input.q,
        "api_key": os.getenv("SERP_API_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results

    def youtube_search(self, input: YoutubeSearchInput):
        params = {
        "engine": input.engine,
        "search_query": input.search_query,
        "api_key": os.getenv("SERP_API_KEY")
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        return results