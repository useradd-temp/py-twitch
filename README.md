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
#### Single Parameter Example
```python
from twitch.client import TwitchAPIClient
client_id = "YOUR CLIENT ID"
client_secret = "YOUR CLIENT SECRET"

client = TwitchAPIClient(client_id, client_secret)

# Default Example
pagination = None
while True:
	
	data = client.get_users_follows(from_id="171003792", after=pagination)
	pagination = data.pagination.cursor
	
	for user in data.data:
		print(f"{171003792} following {user.to_name}")
	
	if not pagination:
		break

```

#### Multiple Parameter Example
```python
from twitch.client import TwitchAPIClient
client_id = "YOUR CLIENT ID"
client_secret = "YOUR CLIENT SECRET"

client = TwitchAPIClient(client_id, client_secret)

# Multi Query Parameters Example
data = client.get_users(id=["141981764", "171003792"])
for user in data.data:
	print(f"display_name is {user.display_name}")

print(data)
```


## TODO

+ Implements OAuth Methods

+ Change fields(such as started_at) type to DateTimeField 

+ Check Optional fields and List fields