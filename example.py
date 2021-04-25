from twitch.client import TwitchAPIClient


if __name__ == "__main__":
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



    # Multi Query Parameters Example
    data = client.get_users(id=["141981764", "171003792"])
    for user in data.data:
        print(f"display_name is {user.display_name}")
