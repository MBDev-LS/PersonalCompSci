
from pprint import pprint

import random

class Node():
	def __init__(self, identifier):
		self.identifier = identifier

		self.upEdge = None
		self.rightEdge = None
		self.downEdge = None
		self.leftEdge = None

		self.visitedFlag = False
	
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
	
	
	def __str__(self) -> str:
		upVal = self.upEdge.node1.identifier if self.upEdge != None else None
		rightVal = self.rightEdge.node1.identifier if self.rightEdge != None else None
		downVal = self.downEdge.node1.identifier if self.downEdge != None else None
		leftVal = self.leftEdge.node1.identifier if self.leftEdge != None else None
		
		return f'<Node {self.identifier} (U:{upVal}, R:{rightVal}, D:{downVal}, L:{leftVal}, )>'


class Edge():
	def __init__(self, node0: Node, node1: Node):
		self.node0 = node0
		self.node1 = node1
		
		self.weight = None 
		self.active = False
	
	def __str__(self) -> str:
		return f"<Edge ({self.node0.identifier} -> {self.node1.identifier}) ({self.weight}, {self.active}) >"


def generateGraph(width: int, height: int) -> list:
	graphList = []

	for i in range(0, width * height):
		newNode = Node(i)

		upConnectedIndex = i - width

		if upConnectedIndex >= 0:
			upConnectedNode = graphList[upConnectedIndex]

			newNode.upEdge = Edge(newNode, upConnectedNode)
			upConnectedNode.downEdge = Edge(upConnectedNode, newNode)
		
		leftConnectedIndex = i - 1

		if i % width > 0 and i > 0:
			leftConnectedNode = graphList[leftConnectedIndex]

			newNode.leftEdge = Edge(newNode, leftConnectedNode)
			leftConnectedNode.rightEdge = Edge(leftConnectedNode, newNode)
		
		graphList.append(newNode)
	
	return graphList


def setRandomWeights(graphList: list[Node]) -> list[Node]:
	for node in graphList:
		node.setUpEdgeWeightIfNotNone(random.randint(1, 100))
		node.setRightEdgeWeightIfNotNone(random.randint(1, 100))
		node.setDownEdgeWeightIfNotNone(random.randint(1, 100))
		node.setLeftEdgeWeightIfNotNone(random.randint(1, 100))
	
	return graphList

if __name__ == '__name__':
	pprint([str(node) for node in setRandomWeights( generateGraph(9,4) )])
