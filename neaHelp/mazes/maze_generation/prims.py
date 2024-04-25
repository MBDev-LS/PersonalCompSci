
from pprint import pprint
import random

import graphs


def getOppositeEdge(edgeList: list[graphs.Edge], targetEdge: graphs.Edge) -> graphs.Edge:
	if targetEdge == None:
		return None
	
	for edge in edgeList:
		if edge.node0 == targetEdge.node1 and edge.node1 == targetEdge.node0:
			return edge
	
	return None

def removeOppositeEdges(edgeList: list[graphs.Edge]) -> list[graphs.Edge]:
	resultList = []

	for currentEdge in edgeList:
		if getOppositeEdge(resultList, currentEdge) == None:
			resultList.append(currentEdge)

	return resultList


def removeItemFromList(lst: list, item) -> list:
	# Would a for loop be better?
	while item in lst:
		lst.remove(item)
	
	return lst

def getLowestWeightedAdjacentEdge(node: graphs.Node) -> graphs.Node | None:
	adjacentEdgesList = [
		node.upEdge, node.rightEdge, node.downEdge, node.leftEdge
	]

	adjacentEdgesList = removeItemFromList(adjacentEdgesList, None)

	return sorted(adjacentEdgesList, key=lambda node: node.weight)[0]


def getAdjacentEdges(node: graphs.Node) -> list[graphs.Edge]:
	adjacentEdgesList = [
		node.upEdge, node.rightEdge, node.downEdge, node.leftEdge
	]

	return removeItemFromList(adjacentEdgesList, None)


def checkIfAllNodesAreVisited(graphList: list[graphs.Node]) -> bool:
	return len(set([node.visitedFlag for node in graphList])) == 1 and graphList[0].visitedFlag == True


def getAllVisitedNodes(graphList: list[graphs.Node]) -> list:
	return [node for node in graphList if node.visitedFlag == True]


def getLowestNonCyclingEdge(graphList: list[graphs.Node], possibleEdges: list[graphs.Edge]) -> graphs.Edge | None:
	sortedPossibleEdges = sorted(possibleEdges, key=lambda edge: edge.weight)
	
	for possibleEdge in sortedPossibleEdges:
		if possibleEdge.node1.visitedFlag == False:
			return possibleEdge
	
	return None


def getRandomNonCyclingEdge(possibleEdges: list[graphs.Edge]) -> graphs.Edge | None:
	nonCylcingEdges = []
	
	for possibleEdge in possibleEdges:
		if possibleEdge.node1.visitedFlag == False:
			nonCylcingEdges.append(possibleEdge)
	
	return random.choice(nonCylcingEdges)



def findMinimumSpanningTree(graphList: list[graphs.Node]) -> list[graphs.Node]:
	startIndex = random.randint(0, len(graphList) - 1)
	graphList[startIndex].visitedFlag = True

	while checkIfAllNodesAreVisited(graphList) is not True:
		visitedNodeList = getAllVisitedNodes(graphList)

		possibleEdges = []

		for node in visitedNodeList:
			possibleEdges += getAdjacentEdges(node)

		nextEdge = getRandomNonCyclingEdge(possibleEdges)

		if nextEdge == None:
			continue

		nextEdge.active = True
		nextEdge.node1.visitedFlag = True
	
	return graphList


if __name__ == '__main__':
	graphList = graphs.generateGraph(4,4)
	graphListfthWeights = graphs.setRandomWeights(graphList)

	minimumSpanningTree = findMinimumSpanningTree(graphListWithWeights)
	# print([str(node) for node in minimumSpanningTreeWithFlags])

	for node in minimumSpanningTree:
		print('\n____________________\n', node)
		for edge in getAdjacentEdges(node):
			if edge != None and edge.active == True:
				print(edge)
