
import config

import sqlite3



con = sqlite3.connect(config.DATABASE_DIR)
cur = con.cursor()


cur.execute('''
	CREATE TABLE IF NOT EXISTS players(
			playerId 		INT 			NOT NULL,
			playerUsername 	VARCHAR(25) 	NOT NULL,
			playerName 		VARCHAR(50) 	NOT NULL,
			playerPin 		VARCHAR(6) 		NOT NULL,
			playerWinCount		INT,

			PRIMARY KEY (playerId, playerUsername)
		)
''')



print(config.BASE_DIR)

class Player():
	def __init__(self):
		self.balance = 1500
		self.currentLocationIndex = 0

		self.name = None
		self.username = None

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
	

	def loginPlayer(self):
		pass

	def signupPlayer(self):
		newPlayerName = input('Please enter your name: ')
		newPlayerUsername = input('Please enter your username: ')

		newPlayerPin = input('Please enter your security pin (it must be an integer with 4 to 6 digits, both inclusive): ')
		while Player.validatePlayerPin(newPlayerPin) is False:
			print('Please enter a valid security pin.')
			newPlayerPin = input('Please enter your security pin (it must be an integer with 4 to 6 digits, both inclusive): ')

		signupCon = sqlite3.connect(config.DATABASE_DIR)
		signupCur = signupCon.cursor()



	def loadPlayerProfile(self):
		playerHasAccount = Player.getYesNoInput('Do you have an account already? ')

		if playerHasAccount is True:
			self.loginPlayer()
