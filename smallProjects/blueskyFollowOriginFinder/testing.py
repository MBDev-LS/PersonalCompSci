from atproto import Client
import atproto_client
import atproto_client.models.app
import atproto_client.models.app.bsky
import atproto_client.models.app.bsky.graph
import atproto_client.models.app.bsky.graph.defs
import config
import requests
import json
from pprint import pprint
import re

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


listsWithUserMembership: list[dict[str, str]] = getListsWithUserMembership(user.did)
print(listsWithUserMembership[0]['did'][8:])
print(listsWithUserMembership[0]['did'])

listUrl = listsWithUserMembership[0]['url']
listAuthorDid = re.search(r'\/(did:plc:[a-z0-9]+)\/', listUrl).group(1)
listDid = re.search(r'\/([a-z0-9]+)\/*$', listUrl).group(1)
listAtUri = f'at://{listAuthorDid}/app.bsky.graph.list/{listDid}'

def getListFromBluesky(listAtUri: str, paginationLimit: int=100) -> list[atproto_client.models.app.bsky.graph.defs.ListItemView]:
	
	firstListSegmentResponse = client.app.bsky.graph.get_list({'list': listAtUri, 'limit': paginationLimit})
	outputList = firstListSegmentResponse.items
	cursor = firstListSegmentResponse.cursor

	while cursor != None:
		nextListSegmentResponse = client.app.bsky.graph.get_list({'list': listAtUri, 'limit': paginationLimit, cursor: cursor})
		outputList += nextListSegmentResponse.items
		cursor = nextListSegmentResponse.cursor
	
	return outputList

# tst = client.app.bsky.graph.get_list({'list': 'at://did:plc:5zvhaftvsgw5ispaqcmln77z/app.bsky.graph.list/3ldte46u6tc2e'})

pprint(getListFromBluesky(listAtUri))


cursor = None
'at://did:plc:5zvhaftvsgw5ispaqcmln77z/app.bsky.graph.list/3ldte46u6tc2e'
'https://bsky.app/profile/did:plc:5zvhaftvsgw5ispaqcmln77z/lists/3ldte46u6tc2e'

