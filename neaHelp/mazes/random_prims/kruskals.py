

from pprint import pprint
import graphs

def getListWithoutNone(*args) -> list:
	return [item for item in args if item != None]


def sortEdgeListByWeight(graphList: list[graphs.Node]) -> list[graphs.Edge]:
	return sorted(graphList, key=lambda edge: edge.weight)



def getOppositeEdge(edgeList: list[graphs.Edge], targetEdge: graphs.Edge) -> graphs.Edge:
	if targetEdge == None:
		return None
	
	for edge in edgeList:
		if edge.node0 == targetEdge.node1 and edge.node1 == targetEdge.node0:
			return edge
	
	return None


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

def checkForCycles(graphList: list[graphs.Node], edgeList: list[graphs.Edge], currentNode: graphs.Node, activeEdgesOnly: bool=False) -> bool:
	currentNode.visitedFlag = True
	print('_'*100 + '\nVISITING:', currentNode)
	cyclesFound = False

	for currentEdge in currentNode.getEdgeList():
		print('_'*70 + '\nCHECKING EDGE:', str(currentEdge))
		currentEdge.visitedFlag = True
		oppositeEdge = getOppositeEdge(edgeList, currentEdge)

		if activeEdgesOnly == True and currentEdge.active != True:
			print('EDGE IGNORED (NOT ACTIVE)')
			continue
		elif oppositeEdge != None and oppositeEdge.visitedFlag == True:
			print('EDGE IGNORED (OPPOSITE EDGE ALREADY VISITED)')
			continue

		if currentEdge.node1.visitedFlag == True:
			print('ALREADY VISITED NODE, CYCLE DETECTED.')
			return True
		else:
			print('CALLING SELF')
			cyclesFound = checkForCycles(graphList, edgeList, currentEdge.node1, activeEdgesOnly)
	
	print('NO CYCLES FOUND')
	return cyclesFound



def findMinimumSpanningTree(graphList: list[graphs.Node]) -> list[graphs.Node]:
	
	edgeList = getEdgeList(graphList, True)

	pprint([str(edge) for edge in edgeList])
	print('-------------\n\n')

	for currentEdge in edgeList:
		print('_' * 115)
		currentEdge.active = True
		pprint([str(edge) for edge in edgeList if edge.active == True])

		currentOppositeEdge = getOppositeEdge(edgeList, currentEdge)
		currentOppositeEdge.active = True

		print()
		print(currentEdge)
		print()
		pprint([str(edge) for edge in edgeList if edge.active == True])

		edgeCreatesCycle = checkForCycles(graphList, edgeList, currentEdge.node0, True)
		for node in graphList:
			node.visitedFlag = False

		for edge in edgeList:
			edge.visitedFlag = False

		if edgeCreatesCycle == True:
			currentEdge.active = False
			currentOppositeEdge.active = False

	# print([str(edge) for edge in edgeList])
	return edgeList



# minimumSpanningTree = graphs.setRandomWeights(minimumSpanningTree)
graphList = graphs.generateGraph(3,3)
graphListWithWeights = graphs.setUniformWeights(graphList)

minimumSpanningTreeWithFlags = findMinimumSpanningTree(graphListWithWeights)
minimumSpanningTree = removeOppositeEdges([edge for edge in minimumSpanningTreeWithFlags if edge.active == True])

print(minimumSpanningTree)
pprint([str(edge) for edge in minimumSpanningTree])
