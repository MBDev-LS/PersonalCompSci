
import random
import graphs

def getListWithoutNone(*args) -> list:
	return [item for item in args if item != None]


def sortEdgeListByWeight(graphList: list[graphs.Node]) -> list[graphs.Edge]:
	return sorted(graphList, key=lambda edge: edge.weight)


def getEdgeList(graphList: list[graphs.Node], sortList: bool=False) -> list[graphs.Edge]:
	edgeList = []

	for node in graphList:
		edgeList += getListWithoutNone(
			node.upEdge,
			node.rightEdge,
			node.downEdge,
			node.leftEdge,
		)
	
	return edgeList if sortList != True else sortEdgeListByWeight(edgeList)

def checkForCycles(graphList: list[graphs.Node], activeEdgesOnly: bool=False) -> bool:
	return bool(random.getrandbits(1))

	# Source: https://stackoverflow.com/a/6824868/15394242

def findMinimumSpanningTree(graphList: list[graphs.Node]) -> list[graphs.Node]:
	graphList = graphs.setRandomWeights( graphs.generateGraph(9,4) )
	edgeList = getEdgeList(graphList, True)

	for currentEdge in edgeList:
		currentEdge.active = True

		edgeCreatesCycle = checkForCycles(graphList)

		if edgeCreatesCycle == True:
			currentEdge.active = False


	print([str(edge) for edge in edgeList])
