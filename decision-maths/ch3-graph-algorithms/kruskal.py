
from pprint import pprint

def printList(lst: list) -> None:
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


class Node():
	def __init__(self, name: str) -> None:
		self.name = name
		self.active = False
		self.edgeList = []

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
	
	def get_graph_edge_list(self, sortList: bool=False) -> list:
		graphEdgeList = []

		for node in self.nodeList:
			graphEdgeList += node.getEdgeList()
		
		return graphEdgeList if sortList is False else sorted(graphEdgeList, key=lambda edge: edge.weight)
	
	def checkIfAllNodesAreActive(self) -> bool:

		for node in self.nodeList:
			if node.active is False:
				return False
		
		return True

graphDict = {
	'A': [{'node': 'C', 'weight': 7}, {'node': 'D', 'weight': 4}, {'node': 'E', 'weight': 2}, {'node': 'F', 'weight': 8}],
	'B': [{'node': 'C', 'weight': 1}, {'node': 'E', 'weight': 5}, {'node': 'F', 'weight': 3}],
	'C': [{'node': 'A', 'weight': 7}, {'node': 'D', 'weight': 8}, {'node': 'B', 'weight': 1}],
	'D': [{'node': 'A', 'weight': 4}, {'node': 'C', 'weight': 8}],
	'E': [{'node': 'A', 'weight': 2}, {'node': 'B', 'weight': 5}, {'node': 'F', 'weight': 10}],
	'F': [{'node': 'A', 'weight': 8}, {'node': 'B', 'weight': 3}, {'node': 'E', 'weight': 10}],
}

graph = Graph([Node(nodeName) for nodeName in graphDict])

for currentNode in graph.nodeList:
	for connectedNodeDict in graphDict[currentNode.name]:
		currentNode.addEdge(graph.getNode(connectedNodeDict['node']), connectedNodeDict['weight'])


print(graph)

# print([str(edge) for edge in graph.get_graph_edge_list(sortList=True)])

sortedEdgeList = graph.get_graph_edge_list(sortList=True)
sortedEdgeList.reverse()


printList(sortedEdgeList)


while not graph.checkIfAllNodesAreActive():
	nextEdge = sortedEdgeList.pop()