from .base import *


@dataclass
class StreamData:
    id: str
    user_id: str
    user_login: str
    user_name: str
    game_id: str
    type: str
    title: str
    viewer_count: int
    started_at: str
    language: str
    thumbnail_url: str
    tag_ids: Optional[List[str]]


@dataclass
class StreamsModel:
    pagination: Pagination
    data: List[StreamData]
