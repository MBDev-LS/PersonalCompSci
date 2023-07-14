
import itertools
import config

graphDict = config.GRAPH_DICT

18 + 18 + 9 + 9
pList = graphDict.keys()

possibleGroups = itertools.permutations(pList, 3)

def check_group_validity(group: list) -> bool:
	for primary in group:
		if len([value for value in graphDict[primary] if value in group]) == 0:
			return False
	
	return True
	
validGroups = []

for group in possibleGroups:
	if check_group_validity(group) == True:
		validGroups.append(group)
		
print(validGroups)

combinations = 0

print('Getting perms 2')
validGroupPermutations = itertools.permutations(validGroups, 5)
print('Got perms 2')

def check_group_permutation_validity(groupPermutation: list) -> bool:
	wholeGroup = []
	for groupList in groupPermutation:
		for pItem in groupList:
			wholeGroup.append(pItem)
	
	return wholeGroup == list(set(wholeGroup))
		
validGroupPermutationsList = []
count = 0

for groupPermutation in validGroupPermutations:
	print(f'{count / 30019230521280 * 100}', end='\r')
	if check_group_permutation_validity(groupPermutation) == True:
		validGroupPermutationsList.append(groupPermutation)
	
	count += 1

print(validGroupPermutationsList)