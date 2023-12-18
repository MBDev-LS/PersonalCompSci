
import config

import sqlite3
import re
import colorist
import os
import time
import json

import pathlib
from pathlib import Path


# Utility Functions

def getYesNoInput(prompt: str) -> bool:
		print("\nPlease respond to the following prompt with 'yes' or 'no':")
		userInput = input(prompt)

		while userInput.lower() not in ['yes', 'no', 'y', 'n']:
			print("Please respond to the following prompt with 'yes' or 'no':")
			userInput = input(prompt)
		
		return userInput.lower() in ['yes', 'y']


def clearTerminal(delay: int=0):
	if delay > 0:
		time.sleep(delay)

	os.system('clear')



class Player():
	def __init__(self):
		# Player profile setup
		self.name = None
		self.username = None
		self.playerId = None
		self.guest = None

		# Game setup
		self.inJail = False
		self.getOutOfJailFreeCountCard = 0
		self.turnsInJail = 0

		self.balance = 1500
		self.currentLocationIndex = 0

		self.currentSpace = 0
	
	@classmethod
	def validatePlayerPin(cls, playerPin: str) -> bool:
		return len(playerPin) >= 4 and len(playerPin) <= 6 and playerPin.isdigit()
	
	@classmethod
	def checkUsernameIsUnique(cls, playerUsername: str) -> bool:

		usernameLookupCon = sqlite3.connect(config.DATABASE_DIR)
		usernameLookupCur = usernameLookupCon.cursor()

		queryResult = usernameLookupCur.execute(
			'SELECT * FROM Players WHERE playerUsername = :username', 
			{'username': playerUsername}
		)

		numOfResults = len(queryResult.fetchall())

		usernameLookupCon.close()

		return numOfResults == 0

	@classmethod
	def validateUsername(cls, playerUsername: str) -> dict:
		
		if len(playerUsername) == 0:
			return {'valid': False, 'error': 'No username provided.'}
		elif len(playerUsername) > 25:
			return {'valid': False, 'error': 'Username exceeds maximum length (25).'}
		elif re.match(r'^[a-zA-Z0-9\-\_\.]{1,25}$', playerUsername) == None:
			return {'valid': False, 'error': 'Username contains prohibited character.'}
		
		return {'valid': True, 'error': None}
	
	
	@classmethod
	def getValidUsername(cls, forceUnique: bool=True) -> str:
		usernameIsUnique = False

		while usernameIsUnique == False:
			newPlayerUsername = input('Please enter your username (Max length 50, may contain letters, numbers and _ - .): ')
			validUsernameDict = Player.validateUsername(newPlayerUsername)

			while validUsernameDict['valid'] == False:
				print(f'\nError: {validUsernameDict['error']}')
				newPlayerUsername = input('Please enter your username (Max length 50, may contain letters, numbers and _ - .): ')
				validUsernameDict = Player.validateUsername(newPlayerUsername)
			
			if forceUnique == False or Player.checkUsernameIsUnique(newPlayerUsername) == True:
				break
			else:
				print('Error: Someone is already using this username, please pick a different.')
		
		return newPlayerUsername
	
	@classmethod
	def securityPinInput(cls, overidePrompt: str=None) -> str:
		inputPrompt = overidePrompt if overidePrompt != None else 'Please enter your security pin: '

		playerPin = input(inputPrompt)
		while Player.validatePlayerPin(playerPin) is False:
			print('Please enter a valid security pin.')
			playerPin = input(inputPrompt)
		
		return playerPin


	@classmethod
	def nameInput(cls, overidePrompt: str=None) -> str:
		inputPrompt = overidePrompt if overidePrompt != None else 'Please enter your name: '

		nameInput = input(inputPrompt)
		while len(nameInput) == 0 or len(nameInput) > 50:
			print('Error: Invalid name supplied.')
			nameInput = input(inputPrompt)
		
		return nameInput


	
	def loadPlayerInfo(self, sqlQueryResult: tuple) -> None:
		self.username = sqlQueryResult[1]
		self.name = sqlQueryResult[2]


	def loginPlayer(self) -> bool:
		"""
		Bool returned indicating whether
		user has logged in (True), or will
		play as a guest (False).
		"""
		successfulLogin = False

		while successfulLogin == False:
			loginUsername = self.getValidUsername(forceUnique=False)
			loginPin = Player.securityPinInput()

			loginCon = sqlite3.connect(config.DATABASE_DIR)
			loginCur = loginCon.cursor()

			loginQueryResult = loginCur.execute(
				'SELECT * FROM Players WHERE playerUsername = :username AND playerPin = :securityPin', 
				{'username': loginUsername, 'securityPin': loginPin}
			).fetchall()

			if len(loginQueryResult) == 0:
				print('\nError: No player profile found with those details.')

				signupInstead = getYesNoInput('Would you like to sign up instead? ')
				if signupInstead is True:
					self.signupPlayer()
					return True
				
				playAsGuest = getYesNoInput('Would you like to play as a guest? ')
				if playAsGuest is True:
					return False
			else:
				self.loadPlayerInfo(loginQueryResult[0])
				self.guest = False

				return True
	
	

	def signupPlayer(self):
		newPlayerName = Player.nameInput('Please enter your name (Max length 50): ')
		
		newPlayerUsername = Player.getValidUsername()
		

		newPlayerPin = Player.securityPinInput('Please enter your security pin (it must be an integer with 4 to 6 digits, both inclusive): ')

		signupCon = sqlite3.connect(config.DATABASE_DIR)
		signupCur = signupCon.cursor()

		signupCur.execute(f'''
		INSERT INTO Players (playerId, playerUsername, playerName, playerPin, playerWinCount, playerPlayCount)
		VALUES (NULL, ?, ?, ?, ?, ?);
		''', [newPlayerUsername, newPlayerName, newPlayerPin, 0, 0])

		signupCon.commit()

		loginQueryResult = signupCon.execute(
			'SELECT * FROM Players WHERE playerId = :lastRowId', 
			{'lastRowId': signupCur.lastrowid}
		).fetchone()

		self.loadPlayerInfo(loginQueryResult)
		self.guest = False

		signupCur.close()
	
	
	def loadGuestDetails(self) -> None:
		print('\nYou have chosen to play as a guest, your details, including your score, will not be stored.')

		self.name = Player.nameInput()
		self.username = Player.getValidUsername()
		self.guest = True


	def loadPlayerProfile(self):
		playerHasAccount = getYesNoInput('Do you have an account already? ')

		if playerHasAccount is True:
			loggedIn = self.loginPlayer()

			if loggedIn != True:
				self.loadGuestDetails()
		else:
			if getYesNoInput('Would you like to play as a guest? ') == False:
				self.signupPlayer()
			else:
				self.loadGuestDetails()
	

	# Game functions

	def getBalanceStr(self) -> str:
		return f'£{self.balance}'
	

	def printBalanceUpdate(self, oldBalance: int) -> None:
		print(f"\n{self.name}'s updated: {self.getBalanceStr(oldBalance)} -> {self.getBalanceStr(self.balance)}\n")

	def addToBalance(self, amount: int) -> None:
		oldBalance = self.balance

		self.balance += amount
		
		self.printBalanceUpdate(oldBalance)

	def removeFromBalance(self, amount: int) -> None:
		oldBalance = self.balance

		self.balance -= amount
		
		self.printBalanceUpdate(oldBalance)


	def hasAmount(self, amount: int) -> bool:
		"""
		Checks whether player has the
		specified amount of money.

		Returns bool.
		"""
		return self.balance >= amount



class SpaceGroup():
	def __init__(self, name: str, hexColour: str) -> None:
		self.name = name
		self.hexColour = hexColour

		self.spaces = []

	def getHexColour(self) -> str:
		"""
		Returns the hex code for
		the group's colour.

		Without hashtag (#).
		"""
		return self.hexColour
	
	def checkForMonopoly(self, playerToCheck: Player=None) -> bool:
		"""
		Checks for a monopoly, returns
		boolean.

		If player to check is specified,
		will only return boolean if that
		player has monopoly.
		"""
		spaceOwners = set()

		for space in self.spaces:
			spaceOwners.add(space.owner)
		
		if playerToCheck == None:
			return len(spaceOwners) == 1 and spaceOwners[0] != None
		else:
			return len(spaceOwners) == 1 and spaceOwners[0] == playerToCheck
	

	def numberOfSpacesOwned(self, player: Player) -> int:
		ownershipCount = len([space for space in self.spaces if space.owner == player])
		
		return ownershipCount
	

	def addSpace(self, spaceObj) -> None:
		self.spaces.append(spaceObj)



class PropertySpace():
	def __init__(
			self, 
			name: str, 
			value: int, 

			mortgageValue: int,
			spaceGroup: SpaceGroup,

			locationIndex: int,

			parentGame
		) -> None:
		
		self.locationIndex = locationIndex
		
		self.name = name
		self.value = value
		self.mortgageValue = mortgageValue

		self.owner = None
		self.isMortgaged = False

		self.spaceGroup = spaceGroup
		self.parentGame = parentGame
	

	def getValueStr(self) -> str:
		return f'£{self.value}'
	

	def getNameForPrint(self) -> str:
		groupColour = colorist.ColorHex(self.spaceGroup.getHexColour())

		return f'{groupColour}{self.name}{groupColour.OFF}'
	

	def sellSelfToPlayer(self, playerBuying: Player):
		self.owner = playerBuying
	

	def sellSpace(self, landingPlayer: Player):
		print(f"You're the first to land on {self.getNameForPrint()}!")

		if landingPlayer.hasAmount(self.value) == True:
			if getYesNoInput(f'Would you like to buy it for {self.getValueStr()}? '):
				self.sellSelfToPlayer(landingPlayer)

				return
		else:
			print(f'Unfortunately, it costs {self.getValueStr()} and you only have {landingPlayer.getBalanceStr()}, so you can\'t afford to buy it.')
		
		print('\nAs the property has not been bought, it must be auctioned! Hold an auction amongst yourselves.') # Lazy? Yes.

		auctionWinner = self.parentGame.getPlayerInput('Who won the auction? ')

		self.sellSelfToPlayer(auctionWinner)
	

	def calculateRent() -> str:
		raise Exception('Rent function not defined.')
	

	def collectRent(self, landingPlayer: Player, *args, **kwargs) -> None:
		print(f'{landingPlayer.name} has landed on {self.name}, which is owned by {self.owner.name}!')
		
		rentAmount = self.calculateRent(*args, **kwargs)
		landingPlayer.removeFromBalance(rentAmount)
		self.owner.addToBalance(rentAmount)

		print(f'{landingPlayer.name} has paid {self.name} £{rentAmount}.')



class UtilitySpace(PropertySpace):
	def __init__(
				self, 
				name: str, 
				value: int, 
				baseRentDiceMultiplier: int, 
				monopolyRentDiceMultiplier: int,
				mortgageValue: int,
				spaceGroup: SpaceGroup,
				locationIndex: int,
				parentGame
			) -> None:
		
		super().__init__(
			name, value, mortgageValue, spaceGroup, locationIndex, parentGame
		)
		
		self.baseRentDiceMultiplier = baseRentDiceMultiplier
		self.monopolyRentDiceMultiplier = monopolyRentDiceMultiplier

	
	def calculateRent(self, diceNum: int) -> int:
		if self.spaceGroup.checkForMonopoly() == True:
			return diceNum * self.monopolyRentDiceMultiplier
		else:
			return diceNum * self.baseRentDiceMultiplier

	
	def landFunction(self, landingPlayer: Player, diceNum: int) -> None:
		if self.owner == None:
			self.__sellUtility(landingPlayer)
		elif landingPlayer == self.owner:
			print(f'{landingPlayer.name} has landed on {self.name} and already own it!')
			return
		else:
			self.collectRent(landingPlayer, diceNum)


class StationSpace(PropertySpace):
	def __init__(
				self, 
				name: str, 
				value: int, 
				baseRent: int, 
				rentsWithOtherStations: list,
				mortgageValue: int,
				spaceGroup: SpaceGroup,

				locationIndex: int,

				parentGame
			) -> None:
		
		super().__init__(
			name, value, mortgageValue, spaceGroup, locationIndex, parentGame
		)

		self.baseRent = baseRent
		self.rentsWithOtherStations = rentsWithOtherStations

	
	def calculateRent(self) -> int:
		numOfStationsOwned = self.spaceGroup.numberOfSpacesOwned(self.owner)

		if numOfStationsOwned == 1:
			return self.baseRent
		else:
			return self.rentsWithOtherStations[numOfStationsOwned - 2]
	
	
	def landFunction(self, landingPlayer: Player) -> None:
		if self.owner == None:
			print(f'{landingPlayer.name} has landed on {self.name}')
			self.sellSpace(landingPlayer)
		elif self.owner == landingPlayer:
			print(f'You\'ve landed on {self.name}, which you already own!')
			return
		else:
			print(f'You\'ve landed on {self.name}, which is owned by {self.owner.name}! You must pay them rent.')
			self.collectRent()



class SiteSpace(PropertySpace):
	def __init__(
				self, 
				name: str, 
				spaceGroup: SpaceGroup,

				value: int, 
				baseRent: int,
				houseRents: list,
				hotelRent: int,
				mortgageValue: int,

				locationIndex: int,

				parentGame
			) -> None:
		
		super().__init__(
			name, value, mortgageValue, spaceGroup, locationIndex, parentGame
		)

		self.baseRent = baseRent
		self.houseRents = houseRents
		self.hotelRent = hotelRent

		self.numOfHouses = 0
		self.hasHotel = False


	def calculateRent(self) -> int:
		rentMultiplier = 2 if self.spaceGroup.checkForMonopoly() == True else 1

		if self.hasHotel == True:
			return self.hotelRent * rentMultiplier
		elif self.numOfHouses > 0:
			return self.houseRents[self.numOfHouses - 1] * rentMultiplier
		else:
			return self.baseRent * rentMultiplier
	

	def collectRent(self, renterPlayer: Player):
		rentAmount = self.__calculateRent()

		renterPlayer.removeFromBalance(rentAmount)
		self.owner.addToBalance(rentAmount)

		print(f'{renterPlayer.name} has paid {self.owner.name} £{rentAmount} in rent for stopping on {self.getNameForPrint()}!')
		if self.spaceGroup.checkForMonopoly() == True:
			print(f"That's double rent as {renterPlayer.name} has a monopoly!")
	

	def landFuntion(self, landingPlayer: Player):
		if self.owner == None:
			self.sellSpace(landingPlayer)
		elif self.owner == landingPlayer:
			print(f'{landingPlayer} landed on their own property!')

		self.collectRent(self.owner)



class ChanceCardManager():
	def __init__(self, parentGame) -> None:
		self.parentGame = parentGame

		self.cardFunctions = [
			self.advanceToGo,
			self.a
		]


	def advanceToGo(self, player: Player) -> int:
		"""
		Advance to Go (Collect £200)
		
		Returns new space's ID (integer). None if no change.
		"""
		return 0


	def advanceToSiteWithId24(self, player: Player) -> None:
		"""Advance to site with space ID (cloest to) 24. If you pass Go, collect £200

		Normally Trafalgar Square.
		
		Returns new space's ID (integer). None if no change.
		"""
		pass


	def advanceToLastSite(self, player: Player) -> None:
		"""Advance to last site before Go.
		
		Normally Mayfair.

		Returns new space's ID (integer). None if no change.
		"""
		pass


	def advanceToSiteWithId11(self, player: Player) -> None:
		"""Advance to site with space ID (cloest to) 11. If you pass Go, collect £200

		Usually Pall Mall
		
		Returns new space's ID (integer). None if no change.
		"""
		pass


	def advanceToNearestStation(self, player: Player) -> None:
		"""Advance to the nearest Station. If unowned, you may buy it from the Bank
		If owned, pay wonder twice the rental to which they are otherwise entitled
		
		Returns new space's ID (integer). None if no change.
		"""
		pass


	def advanceToNearestUtility(self, player: Player) -> None:
		"""Advance token to nearest Utility. If unowned, you may buy it from the Bank.
		If owned, throw dice and pay owner a total ten times amount thrown.
		
		Returns new space's ID (integer). None if no change.
		"""
		pass
	

	def bankPaysDividend(self, player: Player) -> None:
		"""Bank pays you dividend of £50
		
		Returns new space's ID (integer). None if no change.
		"""

		print('Bank pays you dividend of £50')
		player.addToBalance(50)


	def getOutOfJailFree(self, player: Player) -> None:
		"""Get Out of Jail Free - to be used at any time
		
		Returns new space's ID (integer). None if no change.
		"""

		print("Get Out of Jail Free - to be used at any time")
		player.getOutOfJailFreeCountCard += 1


	def goBackThreeSpaces(self, player: Player) -> None:
		"""Go Back 3 Spaces
		
		Returns new space's ID (integer). None if no change.
		"""
		
		return (player.currentSpace - 3) % self.parentGame.totalSpaceCount


	def goTojail(self, player: Player) -> None:
		"""Go to Jail. Go directly to Jail, do not pass Go, do not collect £200
		
		Returns new space's ID (integer). None if no change.
		"""

		print('Go to Jail. Go directly to Jail, do not pass Go, do not collect £200')

		return -1


	def makeGeneralRepairs(self, player: Player) -> None:
		"""Make general repairs on all your property.
		For each house pay £25. For each hotel pay £100
		
		Returns new space's ID (integer). None if no change.
		"""
		pass
	

	def speedingFine(self, player: Player) -> None:
		"""Speeding fine £15
		
		Returns new space's ID (integer). None if no change.
		"""
		
		print('Speeding fine £15')
		player.removeFromBalance(15)


	def goToFirstStation(self, player: Player) -> None:
		"""Take a trip to {self.parentGame.firstStation.name}. If you pass Go, collect £200
		
		Returns new space's ID (integer). None if no change.
		"""
		
		print(f'Take a trip to {self.parentGame.firstStation.name}. If you pass Go, collect £200')

		return self.parentGame.firstStation.locationIndex


	def electedChairman(self, player: Player) -> None:
		"""You have been elected Chairman of the Board. Pay each player £50
		
		Returns new space's ID (integer). None if no change.
		"""

		print('You have been elected Chairman of the Board. Pay each player £50')

		otherPlayers = [candidatePlayer for candidatePlayer in self.parentGame.playersList if candidatePlayer != player]

		for otherPlayer in otherPlayers:
			otherPlayer.addToBalance(50)
		
		player.removeFromBalance( 50 * otherPlayers )


	def buildingLoanMatures(self, player: Player) -> None:
		"""Your building loan matures. Collect £150
		
		Returns new space's ID (integer). None if no change.
		"""
		
		print('Your building loan matures. Collect £150')
		player.addToBalance(150)


class Pynopoly():
	def __init__(self, BASE_DIR: Path, SETUP_JSON_NAME: str='pynopolySetup.json') -> None:
		self.BASE_DIR = BASE_DIR
		self.SETUP_JSON_NAME = SETUP_JSON_NAME
		self.checkForSetupJson()

		Pynopoly.databaseSetup()
		self.setup()
	

	@classmethod
	def databaseSetup(cls):
		con = sqlite3.connect(config.DATABASE_DIR)
		cur = con.cursor()

		cur.execute('''
			CREATE TABLE IF NOT EXISTS Players(
					playerId 			INTEGER 		PRIMARY KEY,
					playerUsername 		VARCHAR(25) 	NOT NULL,
					playerName 			VARCHAR(50) 	NOT NULL,
					playerPin 			VARCHAR(6) 		NOT NULL,
					playerWinCount		INT,
					playerPlayCount		INT
				)
		''')

		#PRIMARY KEY (playerUsername) - Removed
	

	def checkForSetupJson(self):
		setupJsonExists = pathlib.Path(self.BASE_DIR / self.SETUP_JSON_NAME).is_file()

		if setupJsonExists != True:
			raise Exception(f'Pynopoly setup JSON file not at BASE_DIR specified. (Tried {self.BASE_DIR / self.SETUP_JSON_NAME})')


	def setupPlayers(self):
		print("You'll need between 2 and 8 players (inclusive).")

		self.playersList = []
		
		for i in range(8):
			if i > 1 and getYesNoInput(f'Would you like to add another player (you\'ve currently added {i})? ') == False:
				break
			print('Adding new player...\n_____________________________\n')
			newPlayer = Player()
			newPlayer.loadPlayerProfile()

			self.playersList.append(newPlayer)
			print('\nAdded player!\n_____________________________\n')

		
		print('Players added successfull! Clearing terminal.')
		clearTerminal(2)
	

	def getSetupJson(self) -> dict:
		self.checkForSetupJson()

		with open(self.BASE_DIR / self.SETUP_JSON_NAME) as f:
			setupDict = json.loads(f.read())
		
		return setupDict

	
	def getSpaceGroup(self, name: str) -> SpaceGroup:
		for spaceGroup in self.spaceGroupsList:
			if spaceGroup.name == name:
				return spaceGroup


	def __loadPropertySpaces(self, setupDict: dict) -> list:
		self.spaceGroupsList = []

		for propertyGroupName in setupDict['propertyGroups']:
			self.spaceGroupsList.append(SpaceGroup(
				propertyGroupName,
				setupDict['propertyGroupHexColours'][propertyGroupName]
			))

		locationProperties = []
		
		for propertyDict in setupDict['properties']['locations']:

			newPropertySpace = SiteSpace(
				name=propertyDict['name'],
				spaceGroup=self.getSpaceGroup(propertyDict['group']),
				value=propertyDict['value'],
				baseRent=propertyDict['rents']['SITE'],
				houseRents=[propertyDict['rents']['oneHouse'], propertyDict['rents']['twoHouses'], propertyDict['rents']['threeHouses'], propertyDict['rents']['fourHouses']],
				hotelRent=propertyDict['rents']['HOTEL'],
				mortgageValue=propertyDict['siteMortgageValue'],
				locationIndex=propertyDict['spaceIndex'],
				parentGame=self
				)
			
			locationProperties.append(newPropertySpace)

			self.getSpaceGroup(propertyDict['group']).addSpace(newPropertySpace)
		
		# print(locationProperties)

		return locationProperties


	def __loadStationSpaces(self, setupDict: dict) -> list:
		stationSpaceGroup = SpaceGroup(
			'Utility',
			'6a6a6a'
		)

		self.spaceGroupsList.append(stationSpaceGroup)

		stationSpaces = []


		for stationDict in setupDict['properties']['stations']:

			"""
			{
				"name": "Kings Cross Station",
				"value": 200,
				"baseRent": 25,
				"multipleStationRents": [50, 100, 200],
				"mortgageValue": 100,

				"spaceIndex": 5
			},
			"""

			newUtilitySpace = StationSpace(
				name=stationDict['name'],
				spaceGroup=stationSpaceGroup,

				value=stationDict['value'],
				baseRent=stationDict['baseRent'],
				rentsWithOtherStations=stationDict['multipleStationRents'],
				mortgageValue=stationDict['mortgageValue'],

				locationIndex=stationDict['spaceIndex'],

				parentGame=self
			)
			
			stationSpaces.append(newUtilitySpace)

			stationSpaceGroup.addSpace(newUtilitySpace)

		self.firstStation = stationSpaces[0]

		return stationSpaces


	def __loadUtilitySpaces(self, setupDict: dict) -> list:
		utilitySpaceGroup = SpaceGroup(
			'Utility',
			'7f7f7f'
		)

		self.spaceGroupsList.append(utilitySpaceGroup)

		utilitySpaces = []

		for utilityDict in setupDict['properties']['utilities']:

			newUtilitySpace = UtilitySpace(

				name=utilityDict['name'],
				spaceGroup=utilitySpaceGroup,
				value=utilityDict['value'],
				baseRentDiceMultiplier=utilityDict['baseRentDiceMultiplier'],
				monopolyRentDiceMultiplier=utilityDict['monopolyRentDiceMultiplier'],

				mortgageValue=utilityDict['mortgageValue'],

				locationIndex=utilityDict['spaceIndex'],

				parentGame=self
			)
			
			utilitySpaces.append(newUtilitySpace)

			utilitySpaceGroup.addSpace(newUtilitySpace)

		return utilitySpaces


	def setupBoard(self) -> None:
		print('Setting up board...')

		setupDict = self.getSetupJson()

		locationSpaces = self.__loadPropertySpaces(setupDict)
		utilitySpaces = self.__loadUtilitySpaces(setupDict)
		stationSpaces = self.__loadStationSpaces(setupDict)

		print(len(locationSpaces + utilitySpaces + stationSpaces))

		self.spacesList = locationSpaces + utilitySpaces + stationSpaces


	def setup(self) -> None:
		if getYesNoInput('Would you like to clear the terminal? ') == True:
			clearTerminal()
		
		print('Welcome to Pynopoly!')
		print("First you'll need to set up the players.")
		# self.setupPlayers()

		self.setupBoard()


	def getPlayerInput(self, prompt: str) -> Player:
		"""
		Gets an valid player input
		and returns the player object
		for that player.
		"""
		pass




def main():
	

	testGame = Pynopoly(config.BASE_DIR)

	# player = Player()
	# Player.validateUsername('mb')
	# Player.validateUsername('mblss')
	# player.loadPlayerProfile()


if __name__ == '__main__':
	main()

