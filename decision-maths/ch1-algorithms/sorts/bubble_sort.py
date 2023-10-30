
import copy

lst = [63, 48, 57, 55, 32, 48, 72, 49, 61, 39]

def bubble_sort(lst):
	passes = []
	itemSwapped = True

	while itemSwapped:
		itemSwapped = False

		for i, item in enumerate(lst):
			if i == len(lst) -1:
				continue

			if item > lst[i+1]:
				lst[i+1], lst[i] = item, lst[i+1]
				itemSwapped = True

		passes.append(copy.copy(lst))

	print(str(passes).replace('], [', '], \n['))
	
	return lst

print(bubble_sort(lst))
