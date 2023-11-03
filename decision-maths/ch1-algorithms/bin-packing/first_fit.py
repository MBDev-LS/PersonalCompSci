

class Item:
	def __init__(self, identifier: str, size: int) -> None:
		self.size = size
		self.identifier = identifier
	
	def __str__(self) -> str:
		return f'{self.identifier}({self.size})'


class Bin():
	BIN_CAPACITY = 180

	def __init__(self, idenitifer, capacity: int=None, itemList: list=None) -> None:
		self.capacity = capacity if capacity is not None else Bin.BIN_CAPACITY
		self.items = itemList if itemList is not None else []
		self.idenitifer = idenitifer
	
	def get_total_items_size(self):
		return sum([item.size for item in self.items])
	
	def add_item(self, item):
		self.items.append(item)
	
	def get_free_space(self) -> int:
		return self.capacity - self.get_total_items_size()
	
	def is_full(self) -> bool:
		return self.get_free_space() == 0
	
	def __str__(self) -> str:
		return f'Bin \'{self.idenitifer}\' [ {", ".join([str(item) for item in self.items])} ]'
		

	@classmethod
	def get_free_space_in_bin_list(cls, binList: list):
		return sum([currentBin.get_free_space() for currentBin in binList])


BIN_CAPACITY = 20

# itemQueue = [
# 	Item('A', 8),
# 	Item('B', 7),
# 	Item('C', 14),
# 	Item('D', 9),
# 	Item('E', 6),
# 	Item('F', 9),
# 	Item('G', 5),
# 	Item('H', 15),
# 	Item('I', 6),
# 	Item('J', 7),
# 	Item('K', 8),
# ]

itemQueue = [
	Item('A', 30),
	Item('B', 30),
	Item('C', 30),
	Item('D', 45),
	Item('E', 45),
	Item('F', 60),
	Item('G', 60),
	Item('H', 60),
	Item('I', 60),
	Item('J', 75),
	Item('K', 90),
	Item('L', 120),
	Item('M', 120),
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

print('\n# First Fit')
fist_fit_bin_list = first_fit(itemQueue)
print('\n'.join([str(currentBin) for currentBin in fist_fit_bin_list]))
print(f'Free space: {Bin.get_free_space_in_bin_list(fist_fit_bin_list)}')

def first_fit_decreasing(itemQueue: list):
	sortedItemQueue = sorted(itemQueue, reverse=True, key=lambda item: item.size)
	
	return first_fit(sortedItemQueue)

print('\n# First Fit Decreasing')
fist_fit_decreasing_bin_list = first_fit_decreasing(itemQueue)
print('\n'.join([str(currentBin) for currentBin in fist_fit_decreasing_bin_list]))
print(f'Free space: {Bin.get_free_space_in_bin_list(fist_fit_decreasing_bin_list)}')

