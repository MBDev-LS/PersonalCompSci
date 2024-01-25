
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





def checkIfAllNodesAreVisited(graphList: list[graphs.Node]) -> bool:
	return len(set([node.visitedFlag for node in graphList])) == 1 and graphList[0].visitedFlag == True



def checkIfAllNodesAreInMaze(graphList: list[graphs.Node]) -> bool:
	return len(set([node.mazePart for node in graphList])) == 1 and graphList[0].mazePart == True


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


def resetWilsonArrows(graphList: list[graphs.Node]) -> list:
	for node in graphList:
		node.wilsonArrow = None
	
	return graphList


# ranintExclude adapted from: https://stackoverflow.com/a/42999190/15394242

def ranintExclude(lowerBound: int, upperBound: int, *exclude):
	exclude = set(exclude)
	randInt = random.randint(lowerBound,upperBound)

	return ranintExclude() if randInt in exclude else randInt 


def findMinimumSpanningTree(graphList: list[graphs.Node]) -> list[graphs.Node]:
	# startIndex = random.randint(0, len(graphList) - 1)
	
	startTargetIndex = random.randint(0, len(graphList) - 1)
	# while startTargetIndex == startIndex:
	# 	startTargetIndex = random.randint(0, len(graphList) - 1)

	graphList[startTargetIndex].mazePart = True

	while checkIfAllNodesAreInMaze(graphList) is not True:
		startIndex = ranintExclude(0, len(graphList) - 1, startTargetIndex)
		startTargetIndex = None

		currentNode = graphList[startIndex]

		while currentNode.mazePart != True:
			nextEdge = random.choice(currentNode.getAdjacentEdges())
			
			currentNode.wilsonArrow = nextEdge
			currentNode = nextEdge.node1

		currentNodeToAdd = graphList[startIndex]

		while currentNodeToAdd.mazePart != True:
			currentNodeToAdd.mazePart = True
			currentNodeToAdd.wilsonArrow.active = True

			currentNodeToAdd = currentNodeToAdd.wilsonArrow.node1
		
		resetWilsonArrows(graphList)
	
	
	
	
	
	return graphList


if __name__ == '__main__':
	graphList = graphs.generateGraph(4,4)
	# graphListWithWeights = graphs.setRandomWeights(graphList)

	minimumSpanningTree = findMinimumSpanningTree(graphList)
	# print([str(node) for node in minimumSpanningTreeWithFlags])

	for node in minimumSpanningTree:
		print('\n____________________\n', node)
		for edge in node.getAdjacentEdges():
			if edge != None and edge.active == True:
				print(edge)
