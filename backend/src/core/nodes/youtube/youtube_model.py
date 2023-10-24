from pydantic import BaseModel


class RetrieveChannelInput(BaseModel):
    channel_id: str


class UpdateChannelInput(BaseModel):
    channel_id: str
    new_name: str


class UploadChannelBannerInput(BaseModel):
    channel_id: str
    banner_url: str


class RetrievePlaylistInput(BaseModel):
    playlist_id: str


class RetrievePlaylistItemsInput(BaseModel):
    playlist_id: str
    max_results: int = 5  # By default, retrieve 5 items. You can adjust this.


class RetrieveVideoInput(BaseModel):
    video_id: str


class RateVideoInput(BaseModel):
    video_id: str
    rating: str  # Should be one of ['like', 'dislike', 'none']


class RetrieveVideoCategoriesInput(BaseModel):
    region_code: str  # This should be a two-letter country code (e.g., "US" for the United States).
