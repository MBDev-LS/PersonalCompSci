# import random
import secrets
import pyperclip


def secureShuffle(lst: list) -> list:
	outputList = []

	for i in range(len(lst)):
		outputList.append(secrets.choice(list(set(lst) - set(outputList))))

	return outputList



HORSE_LIST = [
	'I Am Maximus',
	'Royale Pagaille',
	'Nick Rockett',
	'Grangeclare West',
	'Hewick',
	'Minella Indo',
	'Appreciate It',
	'Minella Cocooner',
	'Conflated',
	'Stumptown',
	'Hitman',
	'Beauport',
	'Bravemansgame',
	'Chantry House',
	'Threeunderthrufive',
	'Perceval Legallois',
	'Kandoo Kid',
	'Iroko',
	'Intense Raffles',
	'Senior Chief',
	'Idas Boy',
	'Fil Dor',
	'Broadway Boy',
	'Coko Beach',
	'Stay Away Fay',
	'Meetingofthewaters',
	'Monbeg Genius',
	'Vanillier',
	'Horantzau Dairy',
	'Hyland',
	'Celebre DAllen',
	'Three Card Brag',
	'Twig',
	'Duffle Coat',
	'Shakem Uparry',
	'Roi Mage',
	'Favori De Champdou',
	'Fantastic Lady',
]


NAMES_LIST = [
	'Adam',
	'Kate',
	'Louis',
	'Anna',
	'Phil',
	'Tina',
	'Martin',
	'Celia',
	'Josh',
	'Noah',
	'Cissy',
]


PEOPLE_COUNT = len(NAMES_LIST)

horsesPerPerson = len(HORSE_LIST) // PEOPLE_COUNT

if horsesPerPerson == 0:
	raise Exception('Must more horses than people')

HORSE_LIST = secureShuffle(HORSE_LIST)

outputString = ''

for i in range(0, min(len(HORSE_LIST), PEOPLE_COUNT * horsesPerPerson - 1), horsesPerPerson):
	outputString += f'\n\n{NAMES_LIST[i//horsesPerPerson]}: {", ".join(HORSE_LIST[i:i+3])}'

outputString += f'\n\n\nNot Assigned: {", ".join(HORSE_LIST[i+3:])}'

print(outputString)
pyperclip.copy(outputString)
