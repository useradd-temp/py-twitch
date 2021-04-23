from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Pagination:
    cursor: Optional[str]


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


@dataclass
class GameData:
    id: str
    name: str
    box_art_url: str = ""


@dataclass
class GamesModel:
    data: List[GameData]


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


@dataclass
class UsersData:
    id: str
    login: str
    display_name: str
    type: str
    broadcaster_type: str
    description: str
    profile_image_url: str
    offline_image_url: str
    view_count: int
    email: Optional[str]
    created_at: str


@dataclass
class UsersModel:
    data: List[UsersData]


@dataclass
class UsersFollowsData:
    from_id: str
    from_login: str
    from_name: str
    to_id: str
    to_login: str
    to_name: str
    followed_at: str


@dataclass
class UsersFollowsModel:
    total: int
    pagination: Pagination
    data: List[UsersFollowsData]
