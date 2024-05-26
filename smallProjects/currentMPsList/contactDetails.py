
import requests
import json
import time
import random

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

contactInfoList = []

with open(BASE_DIR / 'mpsList.json', 'rt') as f:
	mpsList = json.loads(f.read())

print()

for i, mpDict in enumerate(mpsList):
	print(f'		{i} / {len(mpsList)} ({round(i/len(mpsList)*100)}%)', end='\r')
	contactUrl = 'https://members-api.parliament.uk/api' + mpDict['links'][3]['href']

	mpContactJson = requests.get(contactUrl).json()
	mpContactJson['mpId'] = mpDict['value']['id']

	contactInfoList.append(mpContactJson)

	if i % 75 == 0:
		with open(BASE_DIR / 'mpsContactInfoList_cache.json', 'wt') as f:
			f.write(json.dumps(contactInfoList))

		randomSleepDuration = random.randint(5,20)
		print(f'\nCached data. Sleeping for {randomSleepDuration} seconds.\n')
		
		time.sleep(randomSleepDuration)


with open(BASE_DIR / 'mpsContactInfoList.json', 'wt') as f:
	f.write(json.dumps(contactInfoList))
