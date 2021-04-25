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

    post_channels_commercial = api_call(
        path="channels/commercial",
        method="POST",
        oauth=True,
        model=None,
        broadcaster_id=BaseParam(name="broadcaster_id", required=True, types=str),
        length=BaseParam(name="length", required=True, types=int),
    )

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

    # TODO
    get_analytics_games = api_call(
        path="analytics/games",
        method="GET",
        oauth=True,
    )

    get_bits_leaderboard = api_call(
        path="bits/leaderboard",
        method="GET",
        oauth=True,
    )

    get_bits_cheermotes = api_call(
        path="bits/cheermotes",
        method="GET",
        model=BitsCheermotesModel,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str),
    )

    get_extensions_transactions = api_call(
        path="extensions/transactions",
        method="GET",
        model=None,
        extension_id=BaseParam(name="extension_id", types=str, required=True),
        id=BaseParam(name="extension_id", types=str),
        after=BaseParam(name="extension_id", types=str),
        first=BaseParam(name="extension_id", types=int, maximum=100),
    )

    get_helix_channels = api_call(
        path="helix/channels",
        method="GET",
        model=None,
        broadcaster_id=BaseParam(name="broadcaster_id", types=str),
    )

    get_channels = api_call(path="channels", method="GET", model=None, oauth=True)

    get_channels_editors = api_call(
        path="channels/editors", method="GET", model=None, oauth=True
    )

    get_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="GET", model=None, oauth=True
    )

    post_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="POST", model=None, oauth=True
    )

    delete_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="DELETE", model=None, oauth=True
    )

    path_channel_points_custom_rewards = api_call(
        path="channel_points/custom_rewards", method="PATH", model=None, oauth=True
    )

    get_channel_points_custom_rewards_redemptions = api_call(
        path="channel_points/custom_rewards/redemptions",
        method="GET",
        model=None,
        oauth=True,
    )

    path_channel_points_custom_rewards_redemptions = api_call(
        path="channel_points/custom_rewards/redemptions",
        method="PATH",
        model=None,
        oauth=True,
    )

    # TODO!!!
    get_clips = api_call(
        path="clips",
        method="GET",
        model=None,
    )

    post_clips = api_call(path="clips", method="POST", model=None, oauth=True)

    # TODO!!!
    get_entitlements_codes = api_call(
        path="entitlements/codes",
        method="GET",
        model=None,
        code=BaseParam(name="code", types=str),
        user_id=BaseParam(name="user_id", types=int),
    )

    get_entitlements_drops = api_call(
        path="entitlements/drops", method="GET", model=None, oauth=True
    )

    # TODO!!!
    post_entitlements_codes = api_call(
        path="entitlements/codes",
        method="POST",
        model=None,
        code=BaseParam(name="code", types=str),
        user_id=BaseParam(name="user_id", types=int),
    )

    # TODO!!!
    post_eventsub_subscriptions = api_call(
        path="eventsub/subscriptions",
        method="POST",
        model=None,
        type=BaseParam(name="type", types=str),
        version=BaseParam(name="version", types=str),
        condition=BaseParam(name="condition", types=dict),
        transport=BaseParam(name="transport", types=dict),
    )

    # TODO!!!
    delete_eventsub_subscriptions = api_call(
        path="eventsub/subscriptions",
        method="DELETE",
        model=None,
        id=BaseParam(name="id", types=str),
    )

    # TODO!!!
    get_eventsub_subscriptions = api_call(
        path="eventsub/subscriptions",
        method="GET",
        model=None,
        status=BaseParam(name="status", types=str),
        type=BaseParam(name="type", types=str),
    )

    # TODO!!!
    get_games_top = api_call(
        path="games/top",
        method="GET",
        model=None,
    )

    # TODO!!!
    get_games = api_call(path="games", method="GET", model=None)

    # TODO!!!
    get_hypetrain_events = api_call(path="hypetrain/events", method="GET", model=None)

    post_moderation_enforcements_status = api_call(
        path="moderation/enforcements/status", method="POST", model=None, oauth=True
    )

    get_moderation_banned_events = api_call(
        path="moderation/banned/events", method="GET", model=None, oauth=True
    )

    get_moderation_banned = api_call(
        path="moderation/banned", method="GET", model=None, oauth=True
    )

    # TODO!!!
    get_moderation_moderators = api_call(
        path="moderation/moderators",
        method="GET",
        model=None,
    )

    get_moderation_moderators_events = api_call(
        path="moderation/moderators/events", method="GET", model=None, oauth=True
    )

    # TODO!!!
    get_search_categories = api_call(
        path="search/categories",
        method="GET",
        model=None,
    )

    # TODO!!!
    get_search_channels = api_call(path="search/channels", method="GET", model=None)

    get_streams_key = api_call(path="streams/key", method="GET", model=None, oauth=True)

    # TODO!!!
    get_streams = api_call(
        path="streams",
        method="GET",
        model=None,
    )

    get_streams_followed = api_call(
        path="streams/followed", method="GET", model=None, oauth=True
    )

    post_streams_markers = api_call(
        path="streams/markers", method="POST", model=None, oauth=True
    )

    get_streams_markers = api_call(
        path="streams/markers", method="GET", model=None, oauth=True
    )

    get_subscriptions = api_call(path="subscriptions", method="GET", model=None, oauth=True)

    get_subscriptions_user = api_call(
        path="subscriptions/user", method="GET", model=None, oauth=True
    )

    # TODO!!!
    get_tags_streams = api_call(
        path="tags/streams",
        method="GET",
        model=None,
    )

    # TODO!!!
    get_streams_tags = api_call(path="streams/tags", method="GET", model=None)

    # TODO!!!
    put_streams_tags = api_call(
        path="streams/tags", method="GET", model=None, oauth=True
    )

    # TODO!!!
    get_teams_channel = api_call(
        path="teams/channel",
        method="GET",
        model=None,
    )

    # TODO!!!
    get_teams = api_call(
        path="teams",
        method="GET",
        model=None,
    )

    # TODO!!!
    get_users = api_call(
        path="users",
        method="GET",
        model=None,
        id=BaseParam(name="id", types=str),
        login=BaseParam(name="login", types=str),
    )

    put_users = api_call(path="users", method="PUT", model=None, oauth=True)

    # TODO!!!
    get_users_follows = api_call(path="users/follows", method="GET", model=None)

    post_users_follows = api_call(
        path="users/follows", method="POST", model=None, oauth=True
    )

    delete_users_follows = api_call(
        path="users/follows", method="DELETE", model=None, oauth=True
    )

    get_users_blocks = api_call(
        path="users/blocks", method="GET", model=None, oauth=True
    )

    put_users_blocks = api_call(
        path="users/blocks", method="PUT", model=None, oauth=True
    )

    delete_users_blocks = api_call(
        path="users/blocks", method="DELETE", model=None, oauth=True
    )

    get_users_extensions_list = api_call(
        path="users/extensions/list", method="GET", model=None, oauth=True
    )

    get_users_extensions = api_call(
        path="users/extensions", method="GET", model=None, oauth=True
    )

    put_users_extensions = api_call(
        path="users/extensions", method="PUT", model=None, oauth=True
    )

    get_videos = api_call(path="videos", method="GET", model=None)

    delete_videos = api_call(path="videos", method="DELETE", model=None)

    get_webhooks_subscriptions = api_call(
        path="webhooks/subscriptions", method="GET", model=None
    )
