
import pyperclip
import config
import json

import os


existingPropertyDictsList = [
	{'spaceId': 2,	 "name": "Old Kent Road", "cost": "600"},
	{"spaceId": 4,	 "name": "Whitechapel Road",  "cost": "600"},
	{"spaceId": 7,	 "name": "The Angel Islington", "cost": "1000"},
	{"spaceId": 9,	 "name": "Euston Road",  "cost": "1000"},
	{"spaceId": 10,	 "name": "Pentonville Road", "cost": "1200"},
	{"spaceId": 12,	 "name": "Pall Mall", "cost": "1400"},
	{"spaceId": 14,	 "name": "Whitehall", "cost": "1400"},
	{"spaceId": 15,	 "name": "Northumberland Avenue", "cost": "1600"},
	{"spaceId": 17,	 "name": "Bow Street", "cost": "1800"},
	{"spaceId": 19,	 "name": "Marlborough Street", "cost": "1800"},
	{"spaceId": 20,	 "name": "Vine Street", "cost": "2000"},
	{"spaceId": 22,	 "name": "The Strand", "cost": "2200"},
	{"spaceId": 24,	 "name": "Fleet Street", "cost": "2200"},
	{"spaceId": 25,	 "name": "Trafalgar Square",  "cost": "2400"},
	{"spaceId": 27,	 "name": "Leicester Square", "cost": "2600"},
	{"spaceId": 28,	 "name": "Coventry Street", "cost": "2600"},
	{"spaceId": 30,	 "name": "Piccadilly", "cost": "2800"},
	{"spaceId": 32,	 "name": "Regent Street", "cost": "3000"},
	{"spaceId": 33,	 "name": "Oxford Street", "cost": "3000"},
	{"spaceId": 35,	 "name": "Bond Street", "cost": "3200"},
	{"spaceId": 38,	 "name": "Park Lane", "cost": "3500"},
	{"spaceId": 40,	 "name": "Mayfair", "cost": "4000"},
	# {"spaceId": 6,	 "name": "Kings Cross Station", "cost": "2000"},
	# {"spaceId": 16,	 "name": "Marylebone Station", "cost": "2000"},
	# {"spaceId": 26,	 "name": "Fenchurch St Station", "cost": "2000"}, 
	# {"spaceId": 36,	"name":"Liverpool Street Station","cost": "2000"},
	# {"spaceId": 13,	 "name": "Electric Company",  "cost": "1500"},
	# {"spaceId": 29,	 "name": "Water Works", "cost": "1500"}
]



def getYesNoInput(prompt: str) -> bool:
		print("Please respond to the following prompt with 'yes' or 'no':")
		userInput = input(prompt)

		while userInput.lower() not in ['yes', 'no', 'y', 'n']:
			print("Please respond to the following prompt with 'yes' or 'no':")
			userInput = input(prompt)
		
		return userInput.lower() in ['yes', 'y']


def intInput(prompt: str) -> int:
	userInput = input(prompt)

	while not userInput.isdigit():
		userInput = input(prompt)
	
	return int(userInput)


def getGroupInput() -> str:
	groupList = ['brown', 'light_blue', 'pink', 'orange', 'red', 'yellow', 'green', 'dark_blue']

	print('''
Groups: 
	1. brown
	2. light_blue
	3. pink
	4. orange
	5. red
	6. yellow
	7. green
	8. dark_blue
	''')

	groupSelectedIndex = intInput('Pick a group (1-8): ')
	while groupSelectedIndex == 0 or groupSelectedIndex > 8:
		groupSelectedIndex = intInput('Pick a group (1-8): ')
	
	return groupList[groupSelectedIndex - 1]


def savePropertyList(propertyList: list, overrideFileName: str=None, printList: bool=True) -> None:

	fileName = overrideFileName if overrideFileName != None else 'properties.json'

	with open(config.BASE_DIR / 'setup' / fileName, 'wt') as f:
		f.write(json.dumps(propertyList))

	if printList == True:
		print(propertyList)

	pyperclip.copy(json.dumps(propertyList))



with open(config.BASE_DIR / 'setup' / 'properties.json', 'rt') as f:
	propertiesDictsList = json.loads(f.read())


for property in propertiesDictsList:
	os.system('clear')
	print(f"PROPERTY: {property['name']}\n")
	
	newValue = intInput('Enter property value: ')

	property['rents'] = property['values']
	del property['values']

	property['value'] = newValue



# for i, propertyDict in enumerate(propertiesDictsList):
# 	propertyDict['spaceIndex'] = existingPropertyDictsList[i]['spaceId'] - 1

savePropertyList(propertiesDictsList)


# propertyList = []

# for i, existingPropertyDict in enumerate(existingPropertyDictsList):
# 	while True:
# 		os.system('clear')

# 		print(f'{i}/{len(existingPropertyDictsList)} ({round(i/len(existingPropertyDictsList)*100)}%)\n')

# 		print(f'NAME: 	{existingPropertyDict['name']}')
# 		print(f'ID(?):	{existingPropertyDict['spaceId'] - 1}\n')


# 		propertySpaceIndex = intInput("Property space index: ")

# 		propertyName = existingPropertyDict['name'] # Automated
# 		propertyGroup = getGroupInput()

# 		siteValue = intInput('Enter property value (SITE ONLY): ')
# 		valueWith1House = intInput('Enter property value (1 House): ')
# 		valueWith2Houses = intInput('Enter property value (2 House): ')
# 		valueWith3Houses = intInput('Enter property value (3 House): ')
# 		valueWith4Houses = intInput('Enter property value (4 House): ')
# 		valueWithHotel = intInput('Enter property value (WITH HOTEL): ')

# 		houseCost = intInput("Enter cost of houses: ")
# 		hotelCost = intInput("Enter cost of hotels: ")

# 		mortgageValue = intInput("Enter mortgage value: ")

# 		print(f'''
# Check these details:

# NAME:		"{propertyName}"
# SPACE ID: 	{propertySpaceIndex}

# GROUP:		{propertyGroup}

# VALUES:
# 	SITE:		{siteValue}
# 	1 HOUSE:	{valueWith1House}
# 	2 HOUSES:	{valueWith2Houses}
# 	3 HOUSES:	{valueWith3Houses}
# 	4 HOUSES:	{valueWith4Houses}
# 	HOTEL:		{valueWithHotel}

# HOUSE COST:	{houseCost}
# HOTEL COST:	{hotelCost}

# MORTGAGE:	{mortgageValue}

# 		''')

# 		if getYesNoInput('Details are correct: ') == True:
# 			break


# 	propertyList.append({
# 		"name": propertyName,
# 		"group": propertyGroup,
# 		"spaceIndex": propertySpaceIndex,

# 		"values": {
# 			"SITE": 		siteValue, 
# 			"oneHouse": 	valueWith1House, 
# 			"twoHouses": 	valueWith2Houses, 
# 			"threeHouses": 	valueWith3Houses, 
# 			"fourHouses": 	valueWith4Houses, 
# 			"HOTEL": 		valueWithHotel
# 		},

# 		"houseCost": houseCost,
# 		"hotelCost": hotelCost,
		
# 		"siteMortgageValue": mortgageValue
# 	})

# 	savePropertyList(propertyList, overrideFileName='properties_cache.json', printList=False)

# pyperclip.copy(json.dumps(propertyList))



# savePropertyList(propertyList)

