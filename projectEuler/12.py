
import math

def getPrimeFactors(num: int) -> list[int]:
	resultList = []

	while num % 2 == 0:
		resultList.append(2)
		num = int(num / 2)

	for i in range(3, int(math.sqrt(num))+1, 2):
		if num % i == 0:
			resultList.append(i)
			num = int(num / i)

	if num > 2:
		resultList.append(num)
	
	return resultList

def getNumberOfFactors(num: int) -> bool:
	primeFactors = getPrimeFactors(num)
	primeFactorsSet = set(primeFactors)

	resultProduct = 1

	for factor in primeFactorsSet:
		resultProduct *= primeFactors.count(factor) + 1
	
	return int(resultProduct)

# print(getNumberOfFactors(108))

for n in range(100, 100000):
	currentNum = n * (n + 1) /2
	
	if getNumberOfFactors(currentNum) >= 500:
		print(currentNum)
		exit()