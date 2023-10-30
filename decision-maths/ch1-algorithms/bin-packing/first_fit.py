

class Item:
	def __init__(self, identifier: str, size: int) -> None:
		self.size = size
		self.identifier = identifier
	
	def __str__(self) -> str:
		return f'{self.identifier}({self.size})'


class Bin():
	BIN_CAPACITY = 20

	def __init__(self, idenitifer, capacity: int=None, itemList: list=None) -> None:
		self.capacity = capacity if capacity is not None else Bin.BIN_CAPACITY
		self.items = itemList if itemList is not None else []
		self.idenitifer = idenitifer
	
	def get_total_items_size(self):
		return sum([item.size for item in self.items])
	
	def add_item(self, item):
		self.items.append(item)
	
	def __str__(self) -> str:
		return f'Bin \'{self.idenitifer}\' [ {", ".join([str(item) for item in self.items])} ]'

BIN_CAPACITY = 20

itemQueue = [
	Item('A', 8),
	Item('B', 7),
	Item('C', 14),
	Item('D', 9),
	Item('E', 6),
	Item('F', 9),
	Item('G', 5),
	Item('H', 15),
	Item('I', 6),
	Item('J', 7),
	Item('K', 8),
]

def first_fit(itemQueue: list):
	initialBindex = 1
	binList = [Bin(initialBindex)]
	bindex = initialBindex + 1 # 'bindex', a very funny portmanteau of 'bin' and 'index'. Hahaha.

	for currentItem in itemQueue:
		binFound = False

		for currentBin in binList:
			if currentBin.get_total_items_size() + currentItem.size <= currentBin.capacity:
				currentBin.add_item(currentItem)
				binFound = True

				break
		
		if binFound is False:
			binList.append(Bin(bindex, itemList=[currentItem]))
			bindex += 1

	return binList

print('# First Fit')
print('\n'.join([str(currentBin) for currentBin in first_fit(itemQueue)]))


def first_fit_decreasing(itemQueue: list):
	sortedItemQueue = sorted(itemQueue, reverse=True, key=lambda item: item.size)
	
	return first_fit(sortedItemQueue)

print('# First Fit Decreasing')
print('\n'.join([str(currentBin) for currentBin in first_fit_decreasing(itemQueue)]))

