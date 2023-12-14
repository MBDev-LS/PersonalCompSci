
import config

import sqlite3
import re
import colorist
import os
import time

import pathlib
from pathlib import Path


# Utility Functions

def getYesNoInput(prompt: str) -> bool:
		print("Please respond to the following prompt with 'yes' or 'no':")
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
		self.turnsInJail = 0

		self.balance = 1500
		self.currentLocationIndex = 0
	
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
			self.loginPlayer()
		else:
			loggedIn = self.signupPlayer()

			if loggedIn == False:
				self.loadGuestDetails()
	

	# Game functions

	def getBalanceStr(self) -> str:
		return f'£{self.balance}'

	def addToBalance(self, amount: int) -> None:
		self.balance += amount

	def removeFromBalance(self, amount: int) -> None:
		self.balance -= amount

	def hasAmount(self, amount: int) -> bool:
		"""
		Checks whether player has the
		specified amount of money.

		Returns bool.
		"""
		return self.balance >= amount







class SpaceWrapper():
	def __init__(self, name: str) -> None:
		self.name = name
		self.landFunction = None # The function which is called when a player lands on the square.

		# self.owner = None # The player that owns the space, None if not owned


class LocationGroup():
	def __init__(self, name: str, hexColour: str) -> None:
		self.name = name
		self.hexColour = hexColour

		self.properties = []

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
		propertyOwners = set()

		for property in self.properties:
			propertyOwners.add(property.owner)
		
		if playerToCheck == None:
			return len(propertyOwners) == 1 and propertyOwners[0] != None
		else:
			return len(propertyOwners) == 1 and propertyOwners[0] == playerToCheck



class SiteSpace():
	def __init__(
			self, 
			name: str, 
			locationGroup: LocationGroup,
			value: int, 
			baseRent: int,
			houseRents: list,
			hotelRent: int,
			mortgageValue: int,

			parentBoard
		) -> None:
		self.name = name
		self.locationGroup = locationGroup
		
		self.value = value

		self.owner = None

		self.baseRent = baseRent
		self.houseRents = houseRents
		self.hotelRent = hotelRent
		self.mortgageValue = mortgageValue

		self.numOfHouses = 0
		self.hasHotel = True
		
		self.isMortgaged = False

		self.parentBoard = parentBoard
	
	def __getValueStr(self) -> str:
		return f'£{self.value}'

	def getNameForPrint(self) -> str:
		groupColour = colorist.ColorHex(self.locationGroup.getHexColour())

		return f'{groupColour}{self.name}{groupColour.OFF}'


	def __calculateRent(self) -> int:
		rentMultiplier = 2 if self.locationGroup.checkForMonopoly() == True else 1

		if self.hasHotel == True:
			return self.hotelRent * rentMultiplier
		elif self.numOfHouses > 0:
			return self.houseRents[self.numOfHouses - 1] * rentMultiplier
		else:
			return self.baseRent * rentMultiplier
	

	def __collectRent(self, renterPlayer: Player):
		rentAmount = self.__calculateRent()

		renterPlayer.removeFromBalance(rentAmount)
		self.owner.addToBalance(rentAmount)

		print(f'{renterPlayer.name} has paid {self.owner.name} £{rentAmount} in rent for stopping on {self.getNameForPrint()}!')
		if self.locationGroup.checkForMonopoly() == True:
			print(f"That's double rent as {renterPlayer.name} has a monopoly!")
	

	def sellSelfToPlayer(self, playerBuying: Player):
		self.owner = playerBuying

	def __sellProperty(self, landingPlayer: Player):
		print(f"You're the first to land on {self.getNameForPrint()}!")

		if landingPlayer.hasAmount(self.value) == True:
			if getYesNoInput(f'Would you like to buy it for {self.__getValueStr()}? '):
				self.sellSelfToPlayer(landingPlayer)

				return
		else:
			print(f'Unfortunately, it costs {self.__getValueStr()} and you only have {landingPlayer.getBalanceStr()}, so you can\'t afford to buy it.')
		
		print('\nAs the property has not been bought, it must be auctioned! Hold an auction amongst yourselves.') # Lazy? Yes.

		auctionWinner = self.parentBoard.getPlayerInput('Who won the auction? ')

		self.sellSelfToPlayer(auctionWinner)




	def landFuntion(self, landingPlayer: Player):
		if self.owner == None:
			self.__sellProperty(landingPlayer)

		self.__collectRent(self.owner)

		pass




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
			if i > 1 and getYesNoInput(f'Would you like to add another player (you\'ve currently added {i})') == True:
				break
			print('Adding new player...\n_____________________________')
			newPlayer = Player()
			newPlayer.loadPlayerProfile()

			self.playersList.append(newPlayer)
		
		print('Players added successfull! Clearing terminal.')
		clearTerminal(2)


	def setupBoard(self):
		pass


	def setup(self) -> None:
		if getYesNoInput('Would you like to clear the terminal? ') == True:
			clearTerminal()
		
		print('Welcome to Pynopoly!')
		print("First you'll need to set up the players.")
		self.setupPlayers()

		self.setupBoard()
		pass



	def getPlayerInput(self, prompt: str) -> Player:
		"""
		Gets an valid player input
		and returns the player object
		for that player.
		"""
		pass

# The board will handle the gameloop


def main():
	

	testGame = Pynopoly(config.BASE_DIR)

	# player = Player()
	# Player.validateUsername('mb')
	# Player.validateUsername('mblss')
	# player.loadPlayerProfile()


if __name__ == '__main__':
	main()

