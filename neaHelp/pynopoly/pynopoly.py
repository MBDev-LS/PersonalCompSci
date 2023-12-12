
import config

import sqlite3
import re

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
	def getYesNoInput(cls, prompt: str) -> bool:
		print("Please respond to the following prompt with 'yes' or 'no':")
		userInput = input(prompt)

		while userInput.lower() not in ['yes', 'no', 'y', 'n']:
			print("Please respond to the following prompt with 'yes' or 'no':")
			userInput = input(prompt)
		
		return userInput.lower() in ['yes', 'y']
	
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

				playAsGuest = Player.getYesNoInput('Would you like to play as a guest? ')
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

		print(loginQueryResult)

		self.loadPlayerInfo(loginQueryResult)
		self.guest = False

		signupCur.close()
	
	
	def loadGuestDetails(self) -> None:
		print('\nYou have chosen to play as a guest, your details, including your score, will not be stored.')

		self.name = Player.nameInput()
		self.username = Player.getValidUsername()
		self.guest = True


	def loadPlayerProfile(self):
		playerHasAccount = Player.getYesNoInput('Do you have an account already? ')

		if playerHasAccount is True:
			self.loginPlayer()
		else:
			loggedIn = self.signupPlayer()

			if loggedIn == False:
				self.loadGuestDetails()



def databaseSetup():
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


class SpaceWrapper():
	def __init__(self, name: str) -> None:
		self.name = name
		self.landFunction = None # The function which is called when a player lands on the square.

		self.owner = None # The player that owns the space, None if not owned


class SiteSpace():
	def __init__(self, name: str) -> None:
		self.name = name
		self.value = None

		self.numOfHouses = 0
		self.hasHotel = True


class Board():
	pass

# The board will handle the gameloop


def main():
	databaseSetup()

	player = Player()
	Player.validateUsername('mb')
	Player.validateUsername('mblss')
	player.loadPlayerProfile()


if __name__ == '__main__':
	main()

