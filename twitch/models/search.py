from .base import *


@dataclass
class SearchChannelsData:
    broadcaster_language: str
    broadcaster_login: str
    display_name: str
    game_id: str
    id: str
    is_live: bool
    tag_ids: Optional[List[str]]
    thumbnail_url: str
    title: str
    started_at: str


@dataclass
class SearchChannelsModel:
    pagination: Pagination
    data: List[SearchChannelsData]
