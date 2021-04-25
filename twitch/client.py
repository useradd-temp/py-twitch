import json
import requests

from collections import defaultdict
from typing import Dict, TypeVar, Callable, Union
from urllib.parse import urljoin
from dacite import from_dict
from ast import literal_eval

from .models import *
from .params import BaseParam
from .exception import APIError, ValidationError, NotProvideError

T = TypeVar("T")


def api_call(model: T = None, oauth=False, **config) -> Callable[..., T]:
    class APIMethod(object):

        path = config["path"]
        method = config.get("method", "get")
        params = dict()

        def __init__(self, client, **kwargs):

            if oauth:
                raise NotProvideError(
                    message=f"py-twitch does not support '{self.path}' yet"
                )

            self.model = model if model else config.get("model")
            self.client = client
            self.header = {
                "client-id": self.client._client_id,
                "Authorization": f"Bearer {self.client._bearer_token}",
            }
            self.params_restrict = dict()

            for _, item in config.items():
                if isinstance(item, BaseParam):
                    self.params_restrict[item.name] = item

            for key in kwargs.keys():
                self.params[key] = kwargs[key]
            self.url = urljoin(client._uri, self.path)

        def set_validate(self):
            required_sets = defaultdict(list)

            for key, restrict in self.params_restrict.items():
                required_sets[restrict.required_set].append(key in self.params.keys())

            for key, item in required_sets.items():
                if not any(item):
                    raise ValidationError(message=f"Some fields is required ({key})")

        def validate(self):
            query_params = set(self.params.keys()) - set(self.params_restrict.keys())
            if len(query_params) != 0:
                raise ValidationError(
                    message=f"{list(query_params)} is not API query parameter.",
                )

            for key, item in self.params_restrict.items():
                item.validate(self.params.get(item.name))

        def _request(self, url, params, header):
            request = getattr(self.client._session, self.method.lower())
            response = request(url=url, headers=self.header, params=self.params)

            if response.status_code // 100 != 2:
                raise APIError(message=response.text)
            return response

        def execute(self):
            self.set_validate()
            self.validate()
            response = self._request(self.url, self.params, self.header)
            if self.model == dict:

                return literal_eval(response.text)
            elif self.model:
                try:
                    return from_dict(self.model, response.json())
                except Exception:
                    raise APIError(message=response.text)
            else:
                return response.json()

    def _call(client, **kwargs):
        api = APIMethod(client, **kwargs)
        return api.execute()

    return _call


class TwitchAPIClient:

    _uri = "https://api.twitch.tv/helix/"
    _auth_url = "https://id.twitch.tv/oauth2/token"

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret
        self._session = requests.Session()
        self._bearer_token = self._bearer_generator()

    def _bearer_generator(self):
        auth_response = self._session.post(
            self._auth_url,
            params={
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "grant_type": "client_credentials",
            },
        ).json()

        if "access_token" not in auth_response:
            raise Exception("Wrong Client Key")
        return auth_response.get("access_token")

    # Method Block

    # https://dev.twitch.tv/docs/api/reference#start-commercial
    post_channels_commercial = api_call(
        path="channels/commercial",
        method="POST",
        oauth=True,
        model=None,
        broadcaster_id=BaseParam(name="broadcaster_id", required=True, types=str),
        length=BaseParam(name="length", required=True, types=int),
    )

    # https://dev.twitch.tv/docs/api/reference#get-extension-analytics
    get_analytics_extensions = api_call(
        path="analytics/extensions",
        method="GET",
        oauth=True,
        after=BaseParam(name="after", types=str),
        ended_at=BaseParam(name="ended_at", types=str),
        extension_id=BaseParam(name="extension_id", types=str),
        first=BaseParam(name="first", types=int, maximum=200),
        started_at=BaseParam(name="started_at", types=str),
        type=BaseParam(name="type", types=str),
    )

    # https://dev.twitch.tv/docs/api/reference#get-game-analytics
    get_analytics_games = api_call(
        path="analytics/games",
        method="GET",
        oauth=True,
    )

    # https://dev.twitch.tv/docs/api/reference#get-bits-leaderboard
    get_bits_leaderboard = api_call(
        path="bits/leaderboard",
        method="GET",
        oauth=True,
    )

    # https://dev.twitch.tv/docs/api/reference#get-cheermotes
    get_bits_cheermotes = api_call(
        path="bits/cheermotes",
        method="GET",
        model=BitsCheermotesModel,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str),
    )

    # https://dev.twitch.tv/docs/api/reference#get-extension-transactions
    get_extensions_transactions = api_call(
        path="extensions/transactions",
        method="GET",
        model=ExtensionTransactionsModel,
        extension_id=BaseParam(name="extension_id", types=str, required=True),
        id=BaseParam(name="extension_id", types=Union[List, str]),
        after=BaseParam(name="extension_id", types=str),
        first=BaseParam(name="extension_id", types=int, maximum=100),
    )

    # https://dev.twitch.tv/docs/api/reference#get-channel-information
    get_helix_channels = api_call(
        path="helix/channels",
        method="GET",
        model=ChannelModel,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str),
    )

    # https://dev.twitch.tv/docs/api/reference#modify-channel-information
    get_channels = api_call(path="channels", method="GET", model=None, oauth=True)

    # https://dev.twitch.tv/docs/api/reference#get-channel-editors
    get_channels_editors = api_call(
        path="channels/editors", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#create-custom-rewards
    get_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#delete-custom-reward
    post_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="POST", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-custom-reward
    delete_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="DELETE", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#update-custom-reward
    patch_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="PATCH", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-custom-reward-redemption
    get_channel_points_custom_rewards_redemptions = api_call(
        path="channel_points/custom_rewards/redemptions",
        method="GET",
        model=None,
        oauth=True,
    )

    # https://dev.twitch.tv/docs/api/reference#update-redemption-status
    patch_channel_points_custom_rewards_redemptions = api_call(
        path="channel_points/custom_rewards/redemptions",
        method="PATCH",
        model=None,
        oauth=True,
    )

    # https://dev.twitch.tv/docs/api/reference#get-clips
    get_clips = api_call(
        path="clips",
        method="GET",
        model=ClipModel,
        broadcaster_id=BaseParam(
            name="broadcaster_id", types=str, required=True, required_set="info"
        ),
        game_id=BaseParam(
            name="game_id", types=str, required=True, required_set="info"
        ),
        id=BaseParam(name="id", types=str, required=True, required_set="info"),
        after=BaseParam(name="after", types=str),
        before=BaseParam(name="before", types=str),
        ended_at=BaseParam(name="ended_at", types=str),
        first=BaseParam(name="first", types=int, maximum=100),
        started_at=BaseParam(name="started_at", types=str),  # RFC3339 format
    )

    # https://dev.twitch.tv/docs/api/reference#create-clip
    post_clips = api_call(path="clips", method="POST", model=None, oauth=True)

    # https://dev.twitch.tv/docs/api/reference#get-clips
    get_entitlements_codes = api_call(
        path="entitlements/codes",
        method="GET",
        model=CodesModel,
        code=BaseParam(name="code", types=Union[list, str]),
        user_id=BaseParam(name="user_id", types=int),
    )

    # https://dev.twitch.tv/docs/api/reference#get-clips
    get_entitlements_drops = api_call(
        path="entitlements/drops", method="GET", model=None, oauth=True
    )

    # TODO!!! ???
    post_entitlements_codes = api_call(
        path="entitlements/codes",
        method="POST",
        model=None,
        code=BaseParam(name="code", types=str),
        user_id=BaseParam(name="user_id", types=int),
    )

    # https://dev.twitch.tv/docs/api/reference#create-eventsub-subscription
    post_eventsub_subscriptions = api_call(
        path="eventsub/subscriptions",
        method="POST",
        model=EventsubSubscriptionsModel,
        type=BaseParam(name="type", types=str, required=True),
        version=BaseParam(name="version", types=str, required=True),
        condition=BaseParam(name="condition", types=dict, required=True),
        transport=BaseParam(name="transport", types=dict, required=True),
    )

    # https://dev.twitch.tv/docs/api/reference#delete-eventsub-subscription
    delete_eventsub_subscriptions = api_call(
        path="eventsub/subscriptions",
        method="DELETE",
        model=None,
        id=BaseParam(name="id", types=str, required=True),
    )

    # https://dev.twitch.tv/docs/api/reference#get-eventsub-subscriptions
    get_eventsub_subscriptions = api_call(
        path="eventsub/subscriptions",
        method="GET",
        model=EventsubSubscriptionsModel,
        status=BaseParam(name="status", types=str),
        type=BaseParam(name="type", types=str),
    )

    # https://dev.twitch.tv/docs/api/reference#get-top-games
    get_games_top = api_call(
        path="games/top",
        method="GET",
        model=GamesModel,
        after=BaseParam(name="after", types=str),
        before=BaseParam(name="before", types=str),
        first=BaseParam(name="first", types=int, maximum=100),
    )

    # https://dev.twitch.tv/docs/api/reference#get-games
    get_games = api_call(
        path="games",
        method="GET",
        model=GamesModel,
        id=BaseParam(
            name="id", types=Union[List, str], required=True, required_set="info"
        ),
        name=BaseParam(
            name="name", types=Union[List, str], required=True, required_set="info"
        ),
    )

    # https://dev.twitch.tv/docs/api/reference#get-hype-train-events
    get_hypetrain_events = api_call(
        path="hypetrain/events", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#check-automod-status
    post_moderation_enforcements_status = api_call(
        path="moderation/enforcements/status", method="POST", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-banned-events
    get_moderation_banned_events = api_call(
        path="moderation/banned/events", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-banned-users
    get_moderation_banned = api_call(
        path="moderation/banned", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-moderators
    get_moderation_moderators = api_call(
        path="moderation/moderators", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-moderator-events
    get_moderation_moderators_events = api_call(
        path="moderation/moderators/events", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#search-categories
    get_search_categories = api_call(
        path="search/categories",
        method="GET",
        model=CategoriesModel,
        query=BaseParam(name="query", types=str, required=True),
    )

    # https://dev.twitch.tv/docs/api/reference#search-channels
    get_search_channels = api_call(
        path="search/channels",
        method="GET",
        model=SearchChannelModel,
        query=BaseParam(name="query", types=str, required=True),
    )

    # https://dev.twitch.tv/docs/api/reference#get-stream-key
    get_streams_key = api_call(path="streams/key", method="GET", model=None, oauth=True)

    # https://dev.twitch.tv/docs/api/reference#get-streams
    get_streams = api_call(
        path="streams",
        method="GET",
        model=StreamsModel,
        after=BaseParam(name="after", types=str),
        before=BaseParam(name="before", types=str),
        first=BaseParam(name="first", types=int, maximum=100),
        game_id=BaseParam(name="game_id", types=Union[List, str]),
        language=BaseParam(name="language", types=str),
        user_id=BaseParam(name="user_id", types=Union[List, str]),
        user_login=BaseParam(name="user_login", types=Union[List, str]),
    )

    # https://dev.twitch.tv/docs/api/reference#get-followed-streams
    get_streams_followed = api_call(
        path="streams/followed", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#create-stream-marker
    post_streams_markers = api_call(
        path="streams/markers", method="POST", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-stream-markers
    get_streams_markers = api_call(
        path="streams/markers", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-broadcaster-subscriptions
    get_subscriptions = api_call(
        path="subscriptions", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#check-user-subscription
    get_subscriptions_user = api_call(
        path="subscriptions/user", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-all-stream-tags
    get_tags_streams = api_call(
        path="tags/streams",
        method="GET",
        model=TagsModel,
        after=BaseParam(name="after", types=str),
        first=BaseParam(name="first", types=int, maximum=100),
        tag_id=BaseParam(name="tag_id", types=Union[list, str]),
    )

    # https://dev.twitch.tv/docs/api/reference#get-stream-tags
    get_streams_tags = api_call(
        path="streams/tags",
        method="GET",
        model=TagsModel,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str, required=True),
    )

    # https://dev.twitch.tv/docs/api/reference#replace-stream-tags
    put_streams_tags = api_call(
        path="streams/tags", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-channel-teams
    get_teams_channel = api_call(
        path="teams/channel",
        method="GET",
        model=TeamsChannelModel,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str, required=True),
    )

    # https://dev.twitch.tv/docs/api/reference#get-teams
    get_teams = api_call(
        path="teams",
        method="GET",
        model=TeamsModel,
        name=BaseParam(name="name", types=str),
        id=BaseParam(name="id", types=str),
    )

    # https://dev.twitch.tv/docs/api/reference#get-users
    get_users = api_call(
        path="users",
        method="GET",
        model=UsersModel,
        id=BaseParam(name="id", types=Union[List, str], required_set="user"),
        login=BaseParam(name="login", types=Union[List, str], required_set="user"),
    )

    # https://dev.twitch.tv/docs/api/reference#update-user
    put_users = api_call(path="users", method="PUT", model=None, oauth=True)

    # https://dev.twitch.tv/docs/api/reference#get-users-follows
    get_users_follows = api_call(
        path="users/follows",
        method="GET",
        model=UsersFollowsModel,
        after=BaseParam(name="after", types=str),
        first=BaseParam(name="first", types=int, maximum=100),
        from_id=BaseParam(name="from_id", types=str),
        to_id=BaseParam(name="to_id", types=str),
    )

    # https://dev.twitch.tv/docs/api/reference#create-user-follows
    post_users_follows = api_call(
        path="users/follows", method="POST", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#delete-user-follows
    delete_users_follows = api_call(
        path="users/follows", method="DELETE", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-user-block-list
    get_users_blocks = api_call(
        path="users/blocks", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#block-user
    put_users_blocks = api_call(
        path="users/blocks", method="PUT", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#unblock-user
    delete_users_blocks = api_call(
        path="users/blocks", method="DELETE", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-user-extensions
    get_users_extensions_list = api_call(
        path="users/extensions/list", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-user-active-extensions
    get_users_extensions = api_call(
        path="users/extensions", method="GET", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#update-user-extensions
    put_users_extensions = api_call(
        path="users/extensions", method="PUT", model=None, oauth=True
    )

    # https://dev.twitch.tv/docs/api/reference#get-videos
    get_videos = api_call(
        path="videos",
        method="GET",
        model=VideosModel,
        id=BaseParam(name="id", types=Union[List, str], required_set="info"),
        user_id=BaseParam(name="user_id", types=str, required_set="info"),
        game_id=BaseParam(name="game_id", types=str, required_set="info"),
        after=BaseParam(name="after", types=str),
        before=BaseParam(name="before", types=str),
        first=BaseParam(name="first", types=int, maximum=100),
        language=BaseParam(name="language", types=str),
        period=BaseParam(name="period", types=str),
        sort=BaseParam(name="sort", types=str),
        type=BaseParam(name="type", types=str),
    )

    # https://dev.twitch.tv/docs/api/reference#delete-videos
    delete_videos = api_call(path="videos", method="DELETE", model=None, oauth=True)

    # https://dev.twitch.tv/docs/api/reference#get-webhook-subscriptions
    get_webhooks_subscriptions = api_call(
        path="webhooks/subscriptions", method="GET", model=WebhooksSubscriptionsModel
    )
