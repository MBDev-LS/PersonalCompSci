from atproto import Client
import config
import requests
import json
from pprint import pprint

userUsername = 'lte.bsky.social'
targetUsername = 'thickpurplecustard.bsky.social'

client = Client()
client.login(userUsername, config.BLUESKY_APP_PASSWORD)

user = client.get_profile(actor=userUsername)
# targetFollowingList = client.get_follows(targetUsername)
# # userFollowsList = client.get_follows(userUsername)
# print(targetFollowingList.follows)

def getListsWithUserMembership(did: str) -> list | None:
	try:
		clearskyResponse = requests.get(f'https://api.clearsky.services/api/v1/anon/get-list/{did}')
	except:
		return None
	else:
		return json.loads(clearskyResponse.text)['data']['lists']


listsWithUserMembership = getListsWithUserMembership(user.did)

tst = client.app.bsky.graph.get_list(listsWithUserMembership[0].did)
print(tst)
