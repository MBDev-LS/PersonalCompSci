
import requests
import json

global_request_count = 0

def handleHttpErrors(httpFunction):
	def handleHttpErrorsDectorator(*args, **kwargs):
		httpFunction(*args, **kwargs)
		try:
			return httpFunction(*args, **kwargs)
		except requests.exceptions.ConnectionError:
			print('No internet connection.')
		except Exception:
			print('Unidentified error with requests.')
	
	return handleHttpErrorsDectorator

@handleHttpErrors
def getPartList() -> list:
	response = requests.get('https://erskinemay-api.parliament.uk/api/Part')
	global global_request_count
	global_request_count += 1
	
	if response.status_code == 200:
		return json.loads(response.text)

def fetchSection(sectionId: int) -> dict:
	response = requests.get(f'https://erskinemay-api.parliament.uk/api/Section/{sectionId}')
	global global_request_count
	global_request_count += 1
	
	if response.status_code == 200:
		sectionDict = json.loads(response.text)
	else:
		raise KeyError(f'Section not found with ID \'{sectionId}\'')
	
	if len(sectionDict['subSections']) == 0:
		return sectionDict

	newSubsectionList = []
	
	for subsectionDict in sectionDict['subSections']:
		newSubsectionList.append(fetchSection(subsectionDict['id']))
	
	sectionDict['subSections'] = newSubsectionList

	return sectionDict



def fetchChapter(chapterId: int) -> dict:
	response = requests.get(f'https://erskinemay-api.parliament.uk/api/Chapter/{chapterId}')
	global global_request_count
	global_request_count += 1

	if response.status_code == 200:
		chapterDict = json.loads(response.text)
	
	chapterDict['chapterId'] = chapterId

	newSectionsList = []

	for sectionDict in chapterDict['sections']:
		newSectionsList.append(fetchSection(sectionDict['id']))
	
	chapterDict['sections'] = newSectionsList

	return chapterDict


def cacheEntireDocument(outputFileLocation: str):
	if not outputFileLocation.endswith('.json'):
		outputFileLocation += '.json'
	
	partsList = getPartList()
	chapterCount = 0

	for partDict in partsList:
		chapterCount += len(partDict['sections'])
	
	for i in range(1, chapterCount + 1):
		pass


# print(getPartList()[0])

def jsonPrint(obj: dict | list) -> None:
	print(json.dumps(obj))

# jsonPrint(fetchSection(4499))

jsonPrint(fetchChapter(1))
print('REQUESTS:', global_request_count)