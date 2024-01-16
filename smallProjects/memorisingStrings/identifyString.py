
import os
import random
import string

STRING_TO_IDENTIFY = 'dQw4w9WgXc'
PERCENT_CHANCE_OF_STRING = 5


def getYesNoInput(prompt: str) -> bool:
		print("\nPlease respond to the following prompt with 'yes' or 'no':")
		userInput = input(prompt)

		while userInput.lower() not in ['yes', 'no', 'y', 'n', '1', '2']:
			print("Please respond to the following prompt with 'yes' or 'no':")
			userInput = input(prompt)
		
		return userInput.lower() in ['yes', 'y', '2']



while True:
	os.system('clear')
	showString = random.randint(0, 100) <= PERCENT_CHANCE_OF_STRING
	specialCharacterPool =  "" if random.randint(0, 100) < 15 else "$-_.+!*'()"
	charPool = string.ascii_letters + string.digits + specialCharacterPool
	randomString = ''.join(random.choices(charPool, k=11))


	print(f"STRING: '{randomString if showString == False else STRING_TO_IDENTIFY}'")
	responseBool = getYesNoInput('Is this the string? ')

	if responseBool != showString:
		print(f'Incorrect, this is {"not" if showString != True else ""} the string.')
		input()

