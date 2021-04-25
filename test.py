from twitch.client import TwitchAPIClient






if __name__ == '__main__':
	client_id = "YOUR CLIENT ID"
	client_secret = "YOUR CLIENT SECRET"

	client = TwitchAPIClient(client_id, client_secret)
	print(client.users_GET(login='twitch'))
