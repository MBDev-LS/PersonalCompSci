import secrets

# def secureShuffle(lst: list) -> list:
# 	outputList = []

# 	for i in range(len(lst)):
# 		outputList.append(secrets.choice(list(set(lst) - set(outputList))))

# 	return outputList


def secureShuffle(lst: list) -> list:
	outputList = []

	for i in range(len(lst)):
		outputList.append(secrets.choice(list(set(lst) - set(outputList))))

	return outputList


print(''.join([f'\n\n{[ 'Adam', 'Kate', 'Louis', 'Adam', 'Phil', 'Tina', 'Martin', 'Celia', 'Josh', 'Noah', 'Cissy'][i//3]}: {", ".join(secureShuffle(['I Am Maximus', 'Royale Pagaille', 'Nick Rockett', 'Grangeclare West', 'Hewick', 'Minella Indo', 'Appreciate It', 'Minella Cocooner', 'Conflated', 'Stumptown', 'Hitman', 'Beauport', 'Bravemansgame', 'Chantry House', 'Threeunderthrufive', 'Perceval Legallois', 'Kandoo Kid', 'Iroko', 'Intense Raffles', 'Senior Chief', 'Idas Boy', 'Fil Dor', 'Broadway Boy', 'Coko Beach', 'Stay Away Fay', 'Meetingofthewaters', 'Monbeg Genius', 'Vanillier', 'Horantzau Dairy', 'Hyland', 'Celebre DAllen', 'Three Card Brag', 'Twig', 'Duffle Coat', 'Shakem Uparry', 'Roi Mage', 'Favori De Champdou', 'Fantastic Lady'])[i:i+3])}' for i in range(0, min(38, 11 * 3 - 1), 3)]))
