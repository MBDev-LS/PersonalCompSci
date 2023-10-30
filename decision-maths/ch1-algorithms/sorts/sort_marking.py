passes = [
	[48, 57, 55, 32, 48, 63, 49, 61, 39, 72], 
	[48, 55, 32, 48, 57, 49, 61, 39, 63, 72], 
	[48, 32, 48, 55, 49, 57, 39, 61, 63, 72], 
	[32, 48, 48, 49, 55, 39, 57, 61, 63, 72], 
	[32, 48, 48, 49, 39, 55, 57, 61, 63, 72], 
	[32, 48, 48, 39, 49, 55, 57, 61, 63, 72], 
	[32, 48, 39, 48, 49, 55, 57, 61, 63, 72], 
	[32, 39, 48, 48, 49, 55, 57, 61, 63, 72], 
	[32, 39, 48, 48, 49, 55, 57, 61, 63, 72]
]

def intInput(prompt: str='Enter an integer: '):
	userInput = input(prompt)

	while userInput.isdigit() is not True:
		userInput = input(prompt)

	return int(userInput)

for i, passList in enumerate(passes):
	print(f'START OF PASS {i+1}')

	for item in passList:
		userAnswer = intInput()

		if item != userAnswer:
			print(f'Error: {item} != {userAnswer}')
			input()
	
	print(f'END OF PASS {i+1}')
