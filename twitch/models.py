from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Pagination:
    cursor: Optional[str]


@dataclass
class BitsCheermotesModel:
    @dataclass
    class Data:
        @dataclass
        class Tier:
            min_bits: Optional[int]
            id: Optional[str]
            color: Optional[str]
            images: Optional[dict]
            can_cheer: Optional[bool]
            show_in_bits_card: Optional[bool]

        prefix: Optional[str]
        tiers: List[dict]
        tiers: List[Tier]
        type: Optional[str]
        order: Optional[int]
        last_updated: Optional[str]
        is_charitable: Optional[bool]

    data: List[Data]


@dataclass
class ExtensionTransactionsModel:
    @dataclass
    class Data:
        @dataclass
        class ProductData:
            sku: Optional[str]
            cost: Optional[dict]
            displayName: Optional[str]
            inDevelopment: Optional[bool]

        id: Optional[str]
        timestamp: Optional[str]
        broadcaster_id: Optional[str]
        broadcaster_login: Optional[str]
        broadcaster_name: Optional[str]
        user_id: Optional[str]
        user_login: Optional[str]
        user_name: Optional[str]
        product_type: Optional[str]
        product_data: ProductData

    data: List[Data]
    pagination: Pagination


@dataclass
class ChannelModel:
    @dataclass
    class Data:
        broadcaster_id: Optional[str]
        broadcaster_name: Optional[str]
        game_name: Optional[str]
        game_id: Optional[str]
        broadcaster_language: Optional[str]
        title: Optional[str]

    data: List[Data]


@dataclass
class ClipModel:
    @dataclass
    class Data:
        id: Optional[str]
        url: Optional[str]
        embed_url: Optional[str]
        broadcaster_id: Optional[str]
        broadcaster_name: Optional[str]
        creator_id: Optional[str]
        creator_name: Optional[str]
        video_id: Optional[str]
        game_id: Optional[str]
        language: Optional[str]
        title: Optional[str]
        view_count: Optional[int]
        created_at: Optional[str]
        thumbnail_url: Optional[str]
        duration: float

    data: List[Data]
    pagination: Pagination


@dataclass
class CodesModel:
    @dataclass
    class Data:
        code: Optional[str]
        status: Optional[str]

    data: List[Data]


@dataclass
class EventsubSubscriptionsModel:
    @dataclass
    class Data:
        id: Optional[str]
        status: Optional[str]
        type: Optional[str]
        version: Optional[str]
        condition: Optional[dict]
        created_at: Optional[str]
        transport: Optional[dict]

    data: List[Data]
    limit: Optional[int]
    total: Optional[int]
    total_cost: Optional[int]
    max_total_cost: Optional[int]


@dataclass
class GamesModel:
    @dataclass
    class Data:
        box_art_url: Optional[str]
        id: Optional[str]
        name: Optional[str]

    data: List[Data]
    pagination: Pagination


@dataclass
class CategoriesModel:
    @dataclass
    class Data:
        box_art_url: Optional[str]
        id: Optional[str]
        name: Optional[str]

    data: List[Data]
    pagination: Pagination


@dataclass
class SearchChannelModel:
    @dataclass
    class Data:
        broadcaster_language: Optional[str]
        broadcaster_login: Optional[str]
        display_name: Optional[str]
        game_id: Optional[str]
        game_name: Optional[str]
        id: Optional[str]
        is_live: Optional[bool]
        tag_ids: Optional[List[str]]
        thumbnail_url: Optional[str]
        title: Optional[str]
        started_at: Optional[str]

    data: List[Data]
    pagination: Pagination


@dataclass
class StreamsModel:
    @dataclass
    class Data:
        id: Optional[str]
        user_id: Optional[str]
        user_login: Optional[str]
        user_name: Optional[str]
        game_id: Optional[str]
        game_name: Optional[str]
        type: Optional[str]
        title: Optional[str]
        viewer_count: Optional[int]
        started_at: Optional[str]
        language: Optional[str]
        thumbnail_url: Optional[str]
        tag_ids: Optional[List[str]]
        is_mature: Optional[bool]

    data: List[Data]
    pagination: Pagination


@dataclass
class TagsModel:
    @dataclass
    class Data:
        tag_id: Optional[str]
        is_auto: Optional[bool]
        localization_names: Optional[dict]
        localization_descriptions: Optional[dict]

    data: List[Data]
    pagination: Pagination


@dataclass
class TeamsChannelModel:
    @dataclass
    class Data:
        broadcaster_id: Optional[str]
        broadcaster_login: Optional[str]
        broadcaster_name: Optional[str]
        background_image_url: Optional[str]
        banner: Optional[str]
        created_at: Optional[str]
        updated_at: Optional[str]
        info: Optional[str]
        thumbnail_url: Optional[str]
        team_name: Optional[str]
        team_display_name: Optional[str]
        id: Optional[str]

    data: List[Data]


@dataclass
class TeamsModel:
    @dataclass
    class Data:
        @dataclass
        class Users:
            user_id: Optional[str]
            user_login: Optional[str]
            user_name: Optional[str]

        users: List[Users]
        background_image_url: Optional[str]
        banner: Optional[str]
        created_at: Optional[str]
        updated_at: Optional[str]
        info: Optional[str]
        thumbnail_url: Optional[str]
        team_name: Optional[str]
        team_display_name: Optional[str]
        id: Optional[str]

    data: List[Data]


@dataclass
class UsersModel:
    @dataclass
    class Data:
        broadcaster_type: Optional[str]
        description: Optional[str]
        display_name: Optional[str]
        id: Optional[str]
        login: Optional[str]
        offline_image_url: Optional[str]
        profile_image_url: Optional[str]
        type: Optional[str]
        view_count: Optional[int]
        email: Optional[str]
        created_at: Optional[str]

    data: List[Data]


@dataclass
class UsersFollowsModel:
    @dataclass
    class Data:
        followed_at: Optional[str]
        from_id: Optional[str]
        from_login: Optional[str]
        from_name: Optional[str]
        to_id: Optional[str]
        to_login: Optional[str]
        to_name: Optional[str]

    total: Optional[int]
    data: List[Data]
    pagination: Pagination


@dataclass
class VideosModel:
    @dataclass
    class Data:
        @dataclass
        class MutedSegments:
            duration: Optional[int]
            offset: Optional[int]

        id: Optional[str]
        stream_id: Optional[str]
        user_id: Optional[str]
        user_login: Optional[str]
        user_name: Optional[str]
        title: Optional[str]
        description: Optional[str]
        created_at: Optional[str]
        published_at: Optional[str]
        url: Optional[str]
        thumbnail_url: Optional[str]
        viewable: Optional[str]
        view_count: Optional[int]
        language: Optional[str]
        type: Optional[str]
        duration: Optional[str]
        muted_segments: List[MutedSegments]

    data: List[Data]
    pagination: Pagination


@dataclass
class WebhooksSubscriptionsModel:
    @dataclass
    class Data:
        callback: Optional[str]
        expires_at: Optional[str]
        topic: Optional[str]

    total: Optional[int]
    data: List[Data]
    pagination: Pagination
