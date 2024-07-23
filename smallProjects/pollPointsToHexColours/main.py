
import csv
import re

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

pointsFileName = 'points.csv'
pointsFileDir = BASE_DIR / pointsFileName

CONSTITUENCY_COL_NAME = 'Constituency'
PARTY_DETAIL_DICTS = {
	'conservative': {
		'columnName': 'Con',
		'hexColour': '0281aa',
		'verboseName': 'Conservative'
	},
	'labour': {
		'columnName': 'Lab',
		'hexColour': 'E4003B',
		'verboseName': 'Labour'
	},
	'lib_dem': {
		'columnName': 'LDem',
		'hexColour': 'FAA61A',
		'verboseName': 'Liberal Democrats'
	},
	'green': {
		'columnName': 'Grn',
		'hexColour': '02A95B',
		'verboseName': 'Green'
	},
	'snp': {
		'columnName': 'SNP',
		'hexColour': 'FDF38E',
		'verboseName': 'Scottish National Party'
	},
	'plaid': {
		'columnName': 'PC',
		'hexColour': '005B54',
		'verboseName': 'Plaid Cymru'
	},
	'reform': {
		'columnName': 'Ref',
		'hexColour': '12B6CF',
		'verboseName': 'Reform UK'
	},
	'other': {
		'columnName': 'Ind_Oth',
		'hexColour': 'd3d3d3',
		'verboseName': 'Other'
	},
}

TOO_CLOSE_TO_CALL_HEX = 'E5E4E2'
SPEAKER_HEX = '36454F'
SPEAKER_CONSTITUENCY_NAME = 'Chorley'

with open(pointsFileDir) as pointsFile:
	pointsCsvReader = csv.reader(pointsFile, delimiter=',')
	pointsCsvList = list(pointsCsvReader)


# Source: https://www.geeksforgeeks.org/python-program-to-find-second-largest-number-in-a-list/

def getSecondMax(lst: list[int]) -> int:
	mx = max(lst[0], lst[1]) 
	secondmax = min(lst[0], lst[1]) 
	n = len(lst)
	for i in range(2,n): 
		if lst[i] > mx: 
			secondmax = mx
			mx = lst[i] 
		elif lst[i] > secondmax and \
			mx != lst[i]: 
			secondmax = lst[i]
		elif mx == secondmax and \
			secondmax != lst[i]:
			secondmax = lst[i]
	
	return secondmax

# End of GeeksForGeeks code


def getColumnNum(csvList: list[list], columnName: str) -> int | None:
	"""
	Returns column number (zero-indexed)
	for a given column name.

	Returns None if column name is not used.
	"""

	firstRow = csvList[0]

	try:
		firstIndex = firstRow.index(columnName)

		return firstIndex
	except:
		return None



def generatePartyLookupDict(csvList: list[list], partyInfoDict: dict) -> dict:
	partyLookupDict = {}

	for partyDictKey in partyInfoDict:
		partyColumnNum = getColumnNum(csvList, partyInfoDict[partyDictKey]['columnName'])
		partyLookupDict[partyColumnNum] = partyDictKey
	
	return partyLookupDict

CONSTITUENCY_COL_NUM = getColumnNum(pointsCsvList, CONSTITUENCY_COL_NAME)
partyLookupDict = generatePartyLookupDict(pointsCsvList, PARTY_DETAIL_DICTS)


def percentageStringToInt(percentageString: str, rowList) -> int:
	if percentageString == '':
		return 0
	
	match = re.match(r'\d{1,3}', percentageString)
	numGroup = match.group()

	return int(numGroup)

outputList = []

def getWinnerInfo(rowList: list, partyLookupDict: dict) -> dict | None:
	"""
	Returns winning party's ____

	Returns None if too close to call.
	"""
	winningPointValue = max([
		percentageStringToInt(pointValue, rowList) for i, pointValue in enumerate(rowList) if i in list(partyLookupDict)
	])

	secondPointValue = getSecondMax([
		percentageStringToInt(pointValue, rowList) for i, pointValue in enumerate(rowList) if i in list(partyLookupDict)
	])

	print(winningPointValue)

	if rowList.count(winningPointValue) > 1:
		return None
	
	else:
		return {
			'winningPartyKey': partyLookupDict[rowList.index(f'{winningPointValue}%')],
			'winningVoteShare': winningPointValue,
			'secondVoteShare': secondPointValue
		}

def generateWinnersDicts(pointsCsvList: list[list], partyLookupDict: dict[str]) -> list[dict]:
	outputList = [] 

	for i, rowList in enumerate(pointsCsvList):
		if i == 0:
			continue

		winnerInfo = getWinnerInfo(rowList, partyLookupDict)

		# [['Constituency', 'Winner', 'VoteShare', 'HexColour']]
		outputList.append({
			'constituency': rowList[CONSTITUENCY_COL_NUM],
			'winnerName': winnerInfo['winningPartyKey'],
			'margin': winnerInfo['winningVoteShare'] - winnerInfo['secondVoteShare']
		})
	
	return outputList


# print(generateWinnersDicts(pointsCsvList, partyLookupDict))

winnerInfoDictsList = generateWinnersDicts(pointsCsvList, partyLookupDict)

maxMargin = max([winnerDict['margin'] for winnerDict in winnerInfoDictsList])

def generateCsvList(winnerInfoDictsList: list[dict]) -> list[list]:
	outputList = [['Constituency', 'Value', 'Region color', 'Winning Party']]

	for winnerInfoDict in winnerInfoDictsList:
		if winnerInfoDict['constituency'].lower() != SPEAKER_CONSTITUENCY_NAME.lower():
			winnerColour = PARTY_DETAIL_DICTS[winnerInfoDict['winnerName']]['hexColour']
			winningPartyName = PARTY_DETAIL_DICTS[winnerInfoDict['winnerName']]['verboseName']
		else:
			winnerColour = SPEAKER_HEX
			winningPartyName = 'Speaker'

		outputList.append([
			winnerInfoDict['constituency'],
			round((winnerInfoDict['margin'] / maxMargin) * 100),
			f'#{winnerColour}',
			winningPartyName
		])
	
	return outputList


with open(BASE_DIR / 'mapData.csv', 'w', newline='') as outputFile:
    wr = csv.writer(outputFile, quoting=csv.QUOTE_NONE, escapechar='"')
    wr.writerows(generateCsvList(winnerInfoDictsList))

