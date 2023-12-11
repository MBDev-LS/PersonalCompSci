
import config

import sqlite3

import re

class Player():
	def __init__(self):
		self.balance = 1500
		self.currentLocationIndex = 0

		self.name = None
		self.username = None
		self.playerId = None

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

		return len(queryResult.fetchall()) == 0

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
	def getValidUsername(cls) -> str:
		usernameIsUnique = False

		while usernameIsUnique == False:
			newPlayerUsername = input('Please enter your username (Max length 50, may contain letters, numbers and _ - .): ')
			validUsernameDict = Player.validateUsername(newPlayerUsername)

			while validUsernameDict['valid'] == False:
				print(f'\nError: {validUsernameDict['error']}')
				newPlayerUsername = input('Please enter your username (Max length 50, may contain letters, numbers and _ - .): ')
				validUsernameDict = Player.validateUsername(newPlayerUsername)
			
			if Player.checkUsernameIsUnique(newPlayerUsername) == True:
				break
			else:
				print('Error: Someone is already using this username, please pick a different.')
		
		return newPlayerUsername

	def loginPlayer(self):
		pass

	def signupPlayer(self):
		newPlayerName = input('Please enter your name (Max length 50): ')
		
		newPlayerUsername = Player.getValidUsername()
		

		newPlayerPin = input('Please enter your security pin (it must be an integer with 4 to 6 digits, both inclusive): ')
		while Player.validatePlayerPin(newPlayerPin) is False:
			print('Please enter a valid security pin.')
			newPlayerPin = input('Please enter your security pin (it must be an integer with 4 to 6 digits, both inclusive): ')

		signupCon = sqlite3.connect(config.DATABASE_DIR)
		signupCur = signupCon.cursor()

		signupCur.execute(f'''
		INSERT INTO Players (playerId, playerUsername, playerName, playerPin, playerWinCount)
		VALUES (NULL, ?, ?, ?, ?);
		''', [newPlayerUsername, newPlayerName, newPlayerPin, 0])

		signupCon.commit()

		signupCur.close()


	def loadPlayerProfile(self):
		playerHasAccount = Player.getYesNoInput('Do you have an account already? ')

		if playerHasAccount is True:
			self.loginPlayer()
		else:
			self.signupPlayer()


player = Player()
Player.validateUsername('mb')
Player.validateUsername('mblss')
player.loadPlayerProfile()


def databaseSetup():
	con = sqlite3.connect(config.DATABASE_DIR)
	cur = con.cursor()

	cur.execute('''
		CREATE TABLE IF NOT EXISTS Players(
				playerId 		INTEGER 		PRIMARY KEY,
				playerUsername 	VARCHAR(25) 	NOT NULL,
				playerName 		VARCHAR(50) 	NOT NULL,
				playerPin 		VARCHAR(6) 		NOT NULL,
				playerWinCount		INT
			)
	''')

	#PRIMARY KEY (playerUsername) - Removed


def main():
	databaseSetup()


if __name__ == '__main__':
	main()

