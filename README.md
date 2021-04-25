# py-twitch

![python](https://img.shields.io/badge/python-v3.7-blue)

`py-twitch` is Twitch Helix REST API client library.

This library supports typing using dataclass, so you can use IDE's auto complete.

## Note

*Api with OAuth is not implemented. It will be implemented in the future.*


## Installation



```shell
pip install py-twitch
```

## Requirements


+ python ( > 3.7 )
+ requests
+ dacite

## Usage

every client method named method_url. 

For example, `GET https://api.twitch.tv/helix/users` is defined as `get_users`


### Example
```python
from twitch.client import TwitchAPIClient
client_id = "YOUR CLIENT ID"
client_secret = "YOUR CLIENT SECRET"

client = TwitchAPIClient(client_id, client_secret)
data = client.get_users(login='twitch')

print(data)
```

