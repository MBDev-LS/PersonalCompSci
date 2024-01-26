
from pprint import pprint

import random
import math

def removeItemFromList(lst: list, item) -> list:
	# Would a for loop be better?
	while item in lst:
		lst.remove(item)
	
	return lst

class Node():
	def __init__(self, identifier):
		self.identifier = identifier

		self.upEdge = None
		self.rightEdge = None
		self.downEdge = None
		self.leftEdge = None

		self.visitedFlag = False
		self.mazePart = False
		self.wilsonArrow: Edge = None
	
	def setUpEdgeWeightIfNotNone(self, newWeight: int) -> None:
		if self.upEdge != None:
			self.upEdge.weight = newWeight

	def setRightEdgeWeightIfNotNone(self, newWeight: int) -> None:
		if self.rightEdge != None:
			self.rightEdge.weight = newWeight

	def setDownEdgeWeightIfNotNone(self, newWeight: int) -> None:
		if self.downEdge != None:
			self.downEdge.weight = newWeight

	def setLeftEdgeWeightIfNotNone(self, newWeight: int) -> None:
		if self.leftEdge != None:
			self.leftEdge.weight = newWeight
	
	def getEdgeList(self) -> list:
		return [edge for edge in [
			self.upEdge,
			self.rightEdge,
			self.downEdge,
			self.leftEdge
		] if edge != None]
	
	def getAdjacentEdges(self, removeVisited: bool=False) -> list:
		adjacentEdgesList = [
			self.upEdge, self.rightEdge, self.downEdge, self.leftEdge
		]

		if removeVisited == True:
			adjacentEdgesList = [edge for edge in adjacentEdgesList if edge.visitedFlag != True] 

		return removeItemFromList(adjacentEdgesList, None)
		
	
	def __str__(self) -> str:
		upVal = self.upEdge.node1.identifier if self.upEdge != None else None
		rightVal = self.rightEdge.node1.identifier if self.rightEdge != None else None
		downVal = self.downEdge.node1.identifier if self.downEdge != None else None
		leftVal = self.leftEdge.node1.identifier if self.leftEdge != None else None
		
		return f'<Node {self.identifier} (U:{upVal}, R:{rightVal}, D:{downVal}, L:{leftVal})>'


class Edge():
	def __init__(self, node0: Node, node1: Node, weight: int=None):
		self.node0 = node0
		self.node1 = node1
		
		self.weight = None if weight == None else weight
		self.active = False
		self.visitedFlag = False
	
	def __str__(self) -> str:
		return f"<Edge ({self.node0.identifier} -> {self.node1.identifier}) ({self.weight}, {self.active}) >"


def setRandomWeights(graphList: list[Node]) -> list[Node]:
	for node in graphList:
		node.setUpEdgeWeightIfNotNone(random.randint(1, 100))
		node.setRightEdgeWeightIfNotNone(random.randint(1, 100))
		node.setDownEdgeWeightIfNotNone(random.randint(1, 100))
		node.setLeftEdgeWeightIfNotNone(random.randint(1, 100))
	
	return graphList


def setUniformWeights(graphList: list[Node]) -> list[Node]:
	for node in graphList:
		node.setUpEdgeWeightIfNotNone(1)
		node.setRightEdgeWeightIfNotNone(1)
		node.setDownEdgeWeightIfNotNone(1)
		node.setLeftEdgeWeightIfNotNone(1)
	
	return graphList


def generateGraph(width: int, height: int, setUniformWeights: bool=False) -> list[Node]:
	graphList = []

	for i in range(0, width * height):
		newNode = Node(i)

		upConnectedIndex = i - width

		if upConnectedIndex >= 0:
			upConnectedNode = graphList[upConnectedIndex]

			edgeWeights = 1 if setUniformWeights == True else None
			newNode.upEdge = Edge(newNode, upConnectedNode, weight=edgeWeights)
			upConnectedNode.downEdge = Edge(upConnectedNode, newNode, weight=edgeWeights)
		
		leftConnectedIndex = i - 1

		if i % width > 0 and i > 0:
			leftConnectedNode = graphList[leftConnectedIndex]

			newNode.leftEdge = Edge(newNode, leftConnectedNode)
			leftConnectedNode.rightEdge = Edge(leftConnectedNode, newNode)
		
		graphList.append(newNode)
	
	return graphList


def removeInactiveEdges(graphList: list[Node]) -> list[Node]:
	for node in graphList:
		node.upEdge = node.upEdge if node.upEdge != None and node.upEdge.active == True else None
		node.rightEdge = node.rightEdge if node.rightEdge != None and node.rightEdge.active == True else None
		node.downEdge = node.downEdge if node.downEdge != None and node.downEdge.active == True else None
		node.leftEdge = node.leftEdge if node.leftEdge != None and node.leftEdge.active == True else None
	
	return graphList


def getOppositeEdgeStatus(edge: Edge) -> bool:
	"""
	Returns False if no edge is found.
	"""
	possibleEdges = edge.node1.getAdjacentEdges()

	for candidateEdge in possibleEdges:
		if candidateEdge.node1 == edge.node0:
			return candidateEdge.active
	
	return False


def swastikaLeftRightCheck(graphList: list[Node], startIndex: int, mainCount: int, checkBool: bool, gridWidth: int) -> int:
	rightCount = 0
	
	for i in range(startIndex, min(startIndex + mainCount + 2, math.ceil(startIndex / gridWidth) * gridWidth)):
		if graphList[i].rightEdge == None or (graphList[i].rightEdge.active != checkBool and (getOppositeEdgeStatus(graphList[i].rightEdge) != checkBool) or checkBool == False):
			break
		
		rightCount += 1
	
	leftCount = 0
	
	for i in range(startIndex, max(startIndex - mainCount - 2, math.floor(startIndex / gridWidth) * gridWidth), -1):
		if graphList[i].leftEdge == None or (graphList[i].leftEdge.active != checkBool and (getOppositeEdgeStatus(graphList[i].leftEdge) != checkBool) or checkBool == False):
			break
		
		leftCount += 1
	
	return min(abs(mainCount - leftCount), abs(mainCount - rightCount))


def checkForDownSwastikaComponent(graphList: list[Node], startIndex: int, gridWidth: int, checkBool: bool=False) -> int:
	currentIndex = startIndex
	downCount = 0

	useActualCurrentIndex = False

	while currentIndex + gridWidth < len(graphList):
		if graphList[currentIndex].downEdge == None:
			useActualCurrentIndex = True
			break
		elif graphList[currentIndex].downEdge.active != checkBool and (getOppositeEdgeStatus(graphList[currentIndex].downEdge) != checkBool or checkBool == False):
			useActualCurrentIndex = True
			break

		downCount += 1
		currentIndex += gridWidth

	# startIndex = currentIndex if useActualCurrentIndex == True else currentIndex - gridWidth
	startIndex = currentIndex
	
	if downCount == 0:
		return math.inf

	return swastikaLeftRightCheck(graphList, startIndex, downCount, checkBool, gridWidth)


def checkForUpSwastikaComponent(graphList: list[Node], startIndex: int, gridWidth: int, checkBool: bool=False) -> int:
	currentIndex = startIndex
	upCount = 0

	useActualCurrentIndex = False

	while currentIndex + gridWidth >= 0:
		if graphList[currentIndex].upEdge == None:
			useActualCurrentIndex = True
			break
		elif graphList[currentIndex].upEdge.active != checkBool and (getOppositeEdgeStatus(graphList[currentIndex].upEdge) != checkBool or checkBool == False):
			useActualCurrentIndex = True
			break

		upCount += 1
		currentIndex -= gridWidth

	startIndex = currentIndex # if useActualCurrentIndex == True else currentIndex + gridWidth

	if upCount == 0:
		return math.inf
	
	return swastikaLeftRightCheck(graphList, startIndex, upCount, checkBool, gridWidth)


def swastikaUpDownCheck(graphList: list[Node], startIndex: int, mainCount: int, checkBool: bool, gridWidth: int) -> int:
	upCount = 0
	
	for i in range(startIndex, max(startIndex - (mainCount + 2) * gridWidth, startIndex % gridWidth), -gridWidth):
		if graphList[i].upEdge == None or (graphList[i].upEdge.active != checkBool and (getOppositeEdgeStatus(graphList[i].upEdge) != checkBool) or checkBool == False):
			break # Breaks, as edge is the down edge of node1, need to add function to get opposite edge
		
		upCount += 1
	
	downCount = 0
	
	for i in range(startIndex, max(startIndex + (mainCount + 2) * gridWidth, len(graphList) - (startIndex % gridWidth)), gridWidth):
		if graphList[i].downEdge == None or (graphList[i].downEdge.active != checkBool and (getOppositeEdgeStatus(graphList[i].downEdge) != checkBool) or checkBool == False):
			break
		
		downCount += 1
	
	return min(abs(mainCount - downCount), abs(mainCount - upCount))


def checkForRightSwastikaComponent(graphList: list[Node], startIndex: int, gridWidth: int, checkBool: bool=False) -> int:
	currentIndex = startIndex
	rightCount = 0

	useActualCurrentIndex = False

	while currentIndex - 1 <= math.ceil(startIndex / gridWidth) * gridWidth:
		if graphList[currentIndex].rightEdge == None:
			useActualCurrentIndex = True
			break
		elif graphList[currentIndex].rightEdge.active != checkBool and (getOppositeEdgeStatus(graphList[currentIndex].leftEdge) != checkBool or checkBool == False):
			useActualCurrentIndex = True
			break

		rightCount += 1
		currentIndex += 1
	
	startIndex = currentIndex # if useActualCurrentIndex == True else currentIndex - 1

	if rightCount == 0:
		return math.inf
	
	return swastikaUpDownCheck(graphList, startIndex, rightCount, checkBool, gridWidth)


def checkForLeftSwastikaComponent(graphList: list[Node], startIndex: int, gridWidth: int, checkBool: bool=False) -> int:
	currentIndex = startIndex
	leftCount = 0

	useActualCurrentIndex = False

	while currentIndex - 1 >= math.floor(startIndex / gridWidth) * gridWidth:
		if graphList[currentIndex].leftEdge == None:
			useActualCurrentIndex = True
			break
		elif graphList[currentIndex].leftEdge.active != checkBool and (getOppositeEdgeStatus(graphList[currentIndex].leftEdge) != checkBool or checkBool == False):
			useActualCurrentIndex = True
			break

		leftCount += 1
		currentIndex -= 1
	
	startIndex = currentIndex # if useActualCurrentIndex == True else currentIndex + 1

	if leftCount == 0:
		return math.inf
	
	return swastikaUpDownCheck(graphList, startIndex, leftCount, checkBool, gridWidth)

def checkForSwastika(graphList: list[Node], gridWidth: int, checkInactive: bool=False) -> bool:
	checkBool = not checkInactive

	for i in range(1, len(graphList) - 2):
		if i % gridWidth == 0 and gridWidth - (i % gridWidth) == 1:
			continue
		
		checkResultList = [
			checkForDownSwastikaComponent(graphList, i, gridWidth, checkBool),
			checkForUpSwastikaComponent(graphList, i, gridWidth, checkBool),
			checkForLeftSwastikaComponent(graphList, i, gridWidth, checkBool),
			checkForRightSwastikaComponent(graphList, i, gridWidth, checkBool)
		]
		
		if len([result for result in checkResultList if result <= 1]) >= 3:
			return True
	
	return False



# def checkForCycles(graphList: list[Node], currentNode: Node, activeEdgesOnly: bool=False) -> bool:
# 	currentNode.visitedFlag = True

# 	for edge in currentNode.getEdgeList():
# 		if activeEdgesOnly == True and edge.active != True:
# 			continue
		
# 		if edge.node1.visitedFlag == True:
# 			return True
# 		else:
# 			return checkForCycles(graphList, edge.node1, activeEdgesOnly)
	
# 	return False

if __name__ == '__main__':
	# pprint([str(node) for node in setRandomWeights( generateGraph(9,4) )])
	
	nodeA = Node('A')
	nodeB = Node('B')
	nodeC = Node('C')

	nodeA.rightEdge = Edge(nodeA, nodeB)
	nodeB.leftEdge = Edge(nodeB, nodeC)
	nodeC.upEdge = Edge(nodeB, nodeB)

	graphList = [nodeA, nodeB, nodeC]
	# print(checkForCycles(graphList, nodeA))
