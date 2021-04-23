import requests
from typing import Dict
from urllib.parse import urljoin
from typing import TypeVar, Callable
from dacite import from_dict
from .models import *

T = TypeVar("T")


class APIError(Exception):
    def __init__(self, status_code, error_message):
        self.status_code = status_code
        self.error_message = error_message


def api_call(model: T = None, **config) -> Callable[..., T]:
    class APIMethod(object):

        path = config["path"]
        method = config.get("method", "get")
        # required = config.get('required', None)
        params = dict()

        def __init__(self, client, **kwargs):
            self.model = model if model else config.get("model")
            self.client = client
            self.header = {
                "client-id": self.client.client_id,
                "Authorization": f"Bearer {self.client.bearer_token}",
            }
            # TODO raise required args exception block
            for key in kwargs.keys():
                self.params[key] = kwargs[key]
            self.url = urljoin(client.uri, self.path)

        def _request(self, url, params, header):
            request = getattr(self.client.session, self.method.lower())
            response = request(url=url, headers=self.header, params=self.params)

            if response.status_code // 100 != 2:
                raise APIError(response.status_code, response.url)
            return response

        def execute(self, model):
            response = self._request(self.url, self.params, self.header)
            if self.model:
                try:
                    return from_dict(self.model, response.json())
                except Exception:
                    raise APIError(response.status_code, response.text)
            else:
                return response.json()

    def _call(client, **kwargs):
        api = APIMethod(client, **kwargs)
        return api.execute(model)

    return _call


class TwitchAPIClient:
    uri = "https://api.twitch.tv/helix/"
    auth_url = "https://id.twitch.tv/oauth2/token"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.bearer_token = self._bearer_generator()

    def _bearer_generator(self):
        auth_response = self.session.post(
            self.auth_url,
            params={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
        ).json()

        if "access_token" not in auth_response:
            raise Exception("Wrong Client Key")
        return auth_response.get("access_token")

    get_streams = api_call(path="streams", model=StreamsModel)

    get_games = api_call(path="games", model=GamesModel)

    get_search_channels = api_call(path="search/channels", model=SearchChannelsModel)

    get_users_follows = api_call(path="users/follows", model=UsersFollowsModel)

    get_users = api_call(path="users", model=UsersModel)
