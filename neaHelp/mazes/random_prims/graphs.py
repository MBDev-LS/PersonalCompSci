
class Node():
	def __init__(self, identifier):
		self.identifier = identifier

		self.upEdge = None
		self.rightEdge = None
		self.downEdge = None
		self.leftEdge = None

		self.visitedFlag = False


class Edge():
	def __init__(self, node0: Node, node1: Node):
		self.node0 = node0
		self.node1 = node1
		
		self.weight = None 
		self.active = False 


def generate_graph(width: int, height: int):
	graphList = []

	for i in range(0, width * height+1):
		graphList.append(Node(i))

		# print('Current', i, '|', graphList)

		for j in range(i % width, i, width):
			# print('Con', j)

generate_graph(4,4)