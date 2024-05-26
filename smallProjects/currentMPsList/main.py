
import requests
import json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

fullMpList = []

counter = 0
counterLimit = (650 / 20) + 2

nextPage = '/Members/Search?skip=0&take=20'
print()

while True:
	counter += 1
	if counter > counterLimit:
		print('Counter limit hit, exiting loop.')
		break

	print(f'{counter}/ {650 / 20} ({round(counter / (650 / 20) * 100)}%)', end='\r')
	requestURL = f'https://members-api.parliament.uk/api{nextPage}&House=1&IsCurrentMember=true'

	response = requests.get(requestURL)

	responseJson = response.json()

	fullMpList += responseJson['items']

	if responseJson['links'][1]['href'] == nextPage:
		break

	nextPage = responseJson['links'][1]['href']



with open(BASE_DIR / 'mpsList.json', 'wt') as f:
	f.write(json.dumps(fullMpList))

