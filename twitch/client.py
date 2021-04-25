import requests
from typing import Dict
from urllib.parse import urljoin
from typing import TypeVar, Callable
from dacite import from_dict
from .models import *
from .params import BaseParam
from .exception import APIError, ValidationError, NotProvideError

T = TypeVar("T")


def api_call(model: T, oauth=False, **config) -> Callable[..., T]:
    class APIMethod(object):

        path = config["path"]
        method = config.get("method", "get")
        params = dict()

        def __new__(cls, *args, **kwargs):
            if oauth:
                raise NotProvideError(
                    message=f"py-twitch does not support '{cls.path}' yet"
                )
            return super(APIMethod, cls).__new__(cls, **kwargs)

        def __init__(self, client, **kwargs):
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

    channels_commercial = api_call(
        path="channels/commercial",
        method="POST",
        oauth=True,
        model=ChannelsCommercialModel,
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
