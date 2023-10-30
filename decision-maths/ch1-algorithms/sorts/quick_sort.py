
lst = []

def quick_sort(lst: list) -> list:
	pivotIndex = len(lst) - 1
	pivotValue = lst[pivotIndex]

	lst.remove(pivotValue)

	leftOfPivot = [item for item in lst if item <= pivotValue]
	rightOfPivot = [item for item in lst if item > pivotValue]

	print(leftOfPivot)
	sortedLeftList = leftOfPivot if len(leftOfPivot) <= 1 else quick_sort(leftOfPivot)
	sortedRightList = rightOfPivot if len(rightOfPivot) <= 1 else quick_sort(rightOfPivot)

	return sortedLeftList + [pivotValue] + sortedRightList

print(quick_sort([9, 8, 7, 6, 5, 4, 3, 2, 1, 4]))
