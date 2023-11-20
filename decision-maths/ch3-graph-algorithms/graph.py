
from pprint import pprint

def printList(lst: list, returnPrintableList: bool=False) -> None:
	if returnPrintableList is True:
		return [str(item) for item in lst]
	
	print([str(item) for item in lst])



class Edge():
	def __init__(self, innerNode, outerNode, weight: int=1, ) -> None:
		self.innerNode = innerNode
		self.outerNode = outerNode
		self.weight = weight
		self.active = False
	
	def __str__(self) -> str:
		activeFlag = 'T' if self.active is True else 'F'

		return f"{self.innerNode.name} -({self.weight})({activeFlag})-> {self.outerNode.name}"
	
	def activateNodes(self) -> None:
		self.innerNode.active = True
		self.outerNode.active = True


class Node():
	def __init__(self, name: str) -> None:
		self.name = name
		self.active = False
		self.edgeList = []

		self.dfsVisited = False

	def __str__(self) -> str:
		return f"<Node \'{self.name}\' [{', '.join([edge.outerNode.name + '(' + str(edge.weight) + ')' for edge in self.edgeList])}] ({self.active})>"
	
	def getEdgeList(self, require_active: bool=False) -> list:
		return self.edgeList if require_active is False else [edge for edge in self.edgeList if edge.outerNode.is_active()]
	
	def addEdge(self, connectedNode, weight: int=None) -> None:
		self.edgeList.append(Edge(self, connectedNode, weight))
	
	def is_active(self) -> bool:
		return self.active
	
	def set_active(self, isActive: bool) -> None:
		self.active = isActive
	
	


class Graph():
	def __init__(self, nodeList: list) -> None:
		self.nodeList = nodeList
	
	def __str__(self) -> str:
		nodeList = ',\n'.join([str(node) for node in self.nodeList])
		return f"<Graph nodelist = [\n{nodeList}\n]>"

	def getNode(self, nodeName: str) -> Node | None:
		for node in self.nodeList:
			if node.name == nodeName:
				return node
		
		return None
	
	def get_graph_edge_list(self, sortList: bool=False, onlyActive: bool=False) -> list:
		graphEdgeList = []

		for node in self.nodeList:
			graphEdgeList += node.getEdgeList()
		
		if onlyActive:
			graphEdgeList = [edge for edge in graphEdgeList if edge.active == True]

		
		return graphEdgeList if sortList is False else sorted(graphEdgeList, key=lambda edge: edge.weight)
	
	def getNodeList(self, onlyActive: bool=False) -> list:
		return self.nodeList if onlyActive is False else [node for node in self.nodeList if node.active is True]
	
	def checkIfAllNodesAreActive(self) -> bool:

		for node in self.nodeList:
			if node.active is False:
				return False
		
		return True
	
	def resetDfsVisitedFlags(self) -> None:
		for node in self.nodeList:
			node.dfsVisited = False

	def clearEdges(self) -> None:
		for node in self.nodeList:
			node.edgeList = []
	

	def reverseEdges(self) -> None:
		currentEdges = self.get_graph_edge_list()
		self.clearEdges()

		for edge in currentEdges:
			edge.outerNode.addEdge(edge.innerNode, edge.weight)


	def dfsCycleCheck(self, currentNode: Node, onlyActive: bool=False):
		currentNode.dfsVisited = True
		localCycleFlag = False

		for edge in currentNode.edgeList:
			if edge.active == False and onlyActive == True:
				continue
			elif edge.outerNode.dfsVisited == True:
				return True
			
			localCycleFlag = self.dfsCycleCheck(edge.outerNode)

		return localCycleFlag
	
	def checkForCycles(self, onlyActive: bool=None) -> bool:
		"""
		onlyActive - Only check for active edges.
		"""
		self.resetDfsVisitedFlags()

		if len(self.nodeList) == 0:
			return False

		return self.dfsCycleCheck(self.nodeList[0], onlyActive)
	

	def dfsConnectedCheck(self, currentNode: Node, onlyActive: bool=False):
		currentNode.dfsVisited = True
		visitedList = [currentNode]

		for edge in currentNode.edgeList:
			if edge.active == False and onlyActive == True:
				continue
			elif edge.outerNode.dfsVisited == True:
				continue
			
			visitedList += self.dfsConnectedCheck(edge.outerNode)

		return visitedList
	

	def checkGraphIsConnected(self, onlyActive: bool=None) -> bool:
		"""
		onlyActive - Only check for active edges.

		See for details:
		- https://www.geeksforgeeks.org/check-if-a-directed-graph-is-connected-or-not/
		- https://www.geeksforgeeks.org/python-intersection-two-lists/
		"""
		self.resetDfsVisitedFlags()

		if len(self.nodeList) == 0:
			return False
		
		originalCheckList = self.dfsConnectedCheck(self.nodeList[0], onlyActive)
		self.reverseEdges()
		reverseCheckList = self.dfsConnectedCheck(self.nodeList[0], onlyActive)
		self.reverseEdges()

		nodesNotVisited = [
			node for node in self.nodeList if node not in originalCheckList + reverseCheckList
		]

		# print(
		# 	printList(self.nodeList, True), 
		# 	printList(originalCheckList, True), 
		# 	printList(reverseCheckList, True), 
		# 	printList(nodesNotVisited, True)
		# )

		return len(nodesNotVisited) == 0





# graphDict = {
# 	'A': [{'node': 'C', 'weight': 7}, {'node': 'D', 'weight': 4}, {'node': 'E', 'weight': 2}, {'node': 'F', 'weight': 8}],
# 	'B': [{'node': 'C', 'weight': 1}, {'node': 'E', 'weight': 5}, {'node': 'F', 'weight': 3}],
# 	'C': [{'node': 'A', 'weight': 7}, {'node': 'D', 'weight': 8}, {'node': 'B', 'weight': 1}],
# 	'D': [{'node': 'A', 'weight': 4}, {'node': 'C', 'weight': 8}],
# 	'E': [{'node': 'A', 'weight': 2}, {'node': 'B', 'weight': 5}, {'node': 'F', 'weight': 10}],
# 	'F': [{'node': 'A', 'weight': 8}, {'node': 'B', 'weight': 3}, {'node': 'E', 'weight': 10}],
# }

graphDict = {
	'A': [{'node': 'B', 'weight': 4}],
	'B': [],
	'C': [{'node': 'A', 'weight': 2}],
}


graph = Graph([Node(nodeName) for nodeName in graphDict])

for currentNode in graph.nodeList:
	for connectedNodeDict in graphDict[currentNode.name]:
		currentNode.addEdge(graph.getNode(connectedNodeDict['node']), connectedNodeDict['weight'])


print(graph)
print('----------')

print('Cycles:', graph.checkForCycles())
print('Connected:', graph.checkGraphIsConnected())

# graph.reverseEdges()
# print(graph)