import requests
from typing import Dict
from urllib.parse import urljoin
from typing import TypeVar, Callable
from dacite import from_dict

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

        def validate(self, **params):
            query_params = set(params.keys()) - set(self.params_restrict.keys())
            if len(query_params) != 0:
                raise ValidationError(
                    message=f"{list(query_params)} is not API query parameter.",
                )

            for key, item in self.params_restrict.items():
                item.validate(params.get(item.name))

        def _request(self, url, params, header):
            request = getattr(self.client._session, self.method.lower())
            response = request(url=url, headers=self.header, params=self.params)

            if response.status_code // 100 != 2:
                raise APIError(message=response.text)
            return response

        def execute(self):
            self.validate(**self.params)
            response = self._request(self.url, self.params, self.header)
            if self.model:
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

    channels_commercial = api_call(
        path="channels/commercial",
        method="POST",
        oauth=True,
        model=None,
        broadcaster_id=BaseParam(name="broadcaster_id", required=True, types=str),
        length=BaseParam(name="length", required=True, types=int),
    )

    analytics_extensions = api_call(
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

    # TODO
    analytics_games = api_call(
        path="analytics/games",
        method="GET",
        oauth=True,
    )

    bits_leaderboard = api_call(
        path="bits/leaderboard",
        method="GET",
        oauth=True,
    )

    bits_cheermotes = api_call(
        path="bits/cheermotes",
        method="GET",
        model=BitsCheermotesModel,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str),
    )

    extensions_transactions = api_call(
        path="extensions/transactions",
        method="GET",
        model=None,
        extension_id=BaseParam(name="extension_id", types=str, required=True),
        id=BaseParam(name="extension_id", types=str),
        after=BaseParam(name="extension_id", types=str),
        first=BaseParam(name="extension_id", types=int, maximum=100),
    )

    helix_channels = api_call(
        path="helix/channels",
        method="GET",
        model=None,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str),
    )

    channels = api_call(path="channels", method="GET", model=None, oauth=True)

    channels_editors = api_call(
        path="channels/editors", method="GET", model=None, oauth=True
    )

    channel_points_custom_rewards_GET = api_call(
        path="channel_points/custom_rewards", method="GET", model=None, oauth=True
    )

    channel_points_custom_rewards_POST = api_call(
        path="channel_points/custom_rewards", method="POST", model=None, oauth=True
    )

    channel_points_custom_rewards_DELETE = api_call(
        path="channel_points/custom_rewards", method="DELETE", model=None, oauth=True
    )

    channel_points_custom_rewards_PATH = api_call(
        path="channel_points/custom_rewards", method="PATH", model=None, oauth=True
    )

    channel_points_custom_rewards_redemptions_GET = api_call(
        path="channel_points/custom_rewards/redemptions",
        method="GET",
        model=None,
        oauth=True,
    )

    channel_points_custom_rewards_redemptions_PATH = api_call(
        path="channel_points/custom_rewards/redemptions",
        method="PATH",
        model=None,
        oauth=True,
    )

    # TODO!!!
    clips_GET = api_call(
        path="clips",
        method="GET",
        model=None,
    )

    clips_POST = api_call(path="clips", method="POST", model=None, oauth=True)

    # TODO!!!
    entitlements_codes_GET = api_call(
        path="entitlements/codes",
        method="GET",
        model=None,
        code=BaseParam(name="code", types=str),
        user_id=BaseParam(name="user_id", types=int),
    )

    entitlements_drops = api_call(
        path="entitlements/drops", method="GET", model=None, oauth=True
    )

    # TODO!!!
    entitlements_codes_POST = api_call(
        path="entitlements/codes",
        method="POST",
        model=None,
        code=BaseParam(name="code", types=str),
        user_id=BaseParam(name="user_id", types=int),
    )

    # TODO!!!
    eventsub_subscriptions_POST = api_call(
        path="eventsub/subscriptions",
        method="POST",
        model=None,
        type=BaseParam(name="type", types=str),
        version=BaseParam(name="version", types=str),
        condition=BaseParam(name="condition", types=dict),
        transport=BaseParam(name="transport", types=dict),
    )

    # TODO!!!
    eventsub_subscriptions_DELETE = api_call(
        path="eventsub/subscriptions",
        method="DELETE",
        model=None,
        id=BaseParam(name="id", types=str),
    )

    # TODO!!!
    eventsub_subscriptions_GET = api_call(
        path="eventsub/subscriptions",
        method="GET",
        model=None,
        status=BaseParam(name="status", types=str),
        type=BaseParam(name="type", types=str),
    )

    # TODO!!!
    games_top = api_call(
        path="games/top",
        method="GET",
        model=None,
    )

    # TODO!!!
    games = api_call(path="games", method="GET", model=None)

    # TODO!!!
    hypetrain_events = api_call(path="hypetrain/events", method="GET", model=None)

    moderation_enforcements_status = api_call(
        path="moderation/enforcements/status", method="POST", model=None, oauth=True
    )

    moderation_banned_events = api_call(
        path="moderation/banned/events", method="GET", model=None, oauth=True
    )

    moderation_banned = api_call(
        path="moderation/banned", method="GET", model=None, oauth=True
    )

    # TODO!!!
    moderation_moderators = api_call(
        path="moderation/moderators",
        method="GET",
        model=None,
    )

    moderation_moderators_events = api_call(
        path="moderation/moderators/events", method="GET", model=None, oauth=True
    )

    # TODO!!!
    search_categories = api_call(
        path="search/categories",
        method="GET",
        model=None,
    )

    # TODO!!!
    search_channels = api_call(path="search/channels", method="GET", model=None)

    streams_key = api_call(path="streams/key", method="GET", model=None, oauth=True)

    # TODO!!!
    streams = api_call(
        path="streams",
        method="GET",
        model=None,
    )

    streams_followed = api_call(
        path="streams/followed", method="GET", model=None, oauth=True
    )

    streams_markers_POST = api_call(
        path="streams/markers", method="POST", model=None, oauth=True
    )

    streams_markers_GET = api_call(
        path="streams/markers", method="GET", model=None, oauth=True
    )

    subscriptions = api_call(path="subscriptions", method="GET", model=None, oauth=True)

    subscriptions_user = api_call(
        path="subscriptions/user", method="GET", model=None, oauth=True
    )

    # TODO!!!
    tags_streams = api_call(
        path="tags/streams",
        method="GET",
        model=None,
    )

    # TODO!!!
    streams_tags_GET = api_call(path="streams/tags", method="GET", model=None)

    # TODO!!!
    streams_tags_PUT = api_call(
        path="streams/tags", method="GET", model=None, oauth=True
    )

    # TODO!!!
    teams_channel = api_call(
        path="teams/channel",
        method="GET",
        model=None,
    )

    # TODO!!!
    teams = api_call(
        path="teams",
        method="GET",
        model=None,
    )

    # TODO!!!
    users_GET = api_call(
        path="users",
        method="GET",
        model=None,
        id=BaseParam(name="id", types=str),
        login=BaseParam(name="login", types=str),
    )

    users_PUT = api_call(path="users", method="PUT", model=None, oauth=True)

    # TODO!!!
    users_follows_GET = api_call(path="users/follows", method="GET", model=None)

    users_follows_POST = api_call(
        path="users/follows", method="POST", model=None, oauth=True
    )

    users_follows_DELETE = api_call(
        path="users/follows", method="DELETE", model=None, oauth=True
    )

    users_blocks_GET = api_call(
        path="users/blocks", method="GET", model=None, oauth=True
    )

    users_blocks_PUT = api_call(
        path="users/blocks", method="PUT", model=None, oauth=True
    )

    users_blocks_DELETE = api_call(
        path="users/blocks", method="DELETE", model=None, oauth=True
    )

    users_extensions_list = api_call(
        path="users/extensions/list", method="GET", model=None, oauth=True
    )

    users_extensions_GET = api_call(
        path="users/extensions", method="GET", model=None, oauth=True
    )

    users_extensions_PUT = api_call(
        path="users/extensions", method="PUT", model=None, oauth=True
    )

    videos_GET = api_call(path="videos", method="GET", model=None)

    videos_DELETE = api_call(path="videos", method="DELETE", model=None)

    webhooks_subscriptions = api_call(
        path="webhooks/subscriptions", method="GET", model=None
    )

    # streams = api_call(
    #     path="streams",
    #     model=StreamsModel,
    #     user_login=BaseParam(name="user_login", required=True),
    # )

    #
    # get_games = api_call(path="games", model=GamesModel)
    #
    # get_search_channels = api_call(path="search/channels", model=SearchChannelsModel)
    #
    # get_users_follows = api_call(path="users/follows", model=UsersFollowsModel)
    #
    # get_users = api_call(path="users", model=UsersModel)
