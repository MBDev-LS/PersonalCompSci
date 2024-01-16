
import os

# STRING_TO_MEMORISE = input('Enter the string you would like to memorise: ')
STRING_TO_MEMORISE = 'dQw4w9WgXcQ'

while True:
	os.system('clear')
	input(f"The string is: '{STRING_TO_MEMORISE}'\n")
	os.system('clear')

	success = True

	for i, char in enumerate(STRING_TO_MEMORISE):
		os.system('clear')
		print(f"Current text: '{STRING_TO_MEMORISE[:i]}'")
		
		response = input('Enter next character: ')

		if response != char:
			print('Incorrect, attempt over.')
			input()
			success = False
			break
	
	if success == True:
		print('\nYou have successfully remembered the entire string!')
	
	input()

