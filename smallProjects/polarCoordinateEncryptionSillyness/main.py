
import math

def convertPasswordStringToInt(passwordString: str) -> int:
	passwordSum = sum([ord(char) for char in passwordString])

	return passwordSum % math.pi
	# return math.floor(sum([ord(char) for char in passwordString]) ^ 2)

def polarEquation(aConstant: int, theta: int) -> int:
	return aConstant * theta


def encrypt(plainText: str, passwordString: str, privateKey: int) -> str:
	passwordInt = convertPasswordStringToInt(passwordString)

	encryptionPoint = polarEquation(privateKey, )
