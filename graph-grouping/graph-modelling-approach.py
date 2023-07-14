

import config

# TEST_GRAPH_DICT = config.GRAPH_DICT

TEST_GRAPH_DICT = {
	'A': ['B', 'D', ],
	'B': ['C', 'A'],
	'C': ['E', 'B'],
	'D': ['B', 'A'],
	'E': ['C', 'F'],
	'F': ['E']
}


def dfs_cycles_check(adjacencyTable: dict, currentNode: str, visited: set=None) -> bool:
	if visited == None:
		visited = set()

	visited.add(currentNode)
	
	for adjacentNodes in adjacencyTable[currentNode]:
		if adjacentNodes in visited:
			return True
		else:
			visited = dfs_cycles_check(adjacencyTable, adjacentNodes, visited)

			if visited == True:
				return True
	
	return visited


def check_graph_for_cycles(adjacencyTable: dict) -> bool:
	if len(adjacencyTable) > 0:
		return dfs_cycles_check(adjacencyTable, list(adjacencyTable.keys())[0]) == True
	else:
		return False


def split_by_bfs(adjacencyTable: dict, groupSize: int) -> list:
	nodesWithOneEdge = [
		node for node in adjacencyTable if len(adjacencyTable[node]) == 1
	]

	if len(nodesWithOneEdge) > 0:
		currentNode = nodesWithOneEdge[0]
	else:
		currentNode = list(adjacencyTable.keys())[0]
	
	splitCount = 0
	splitList = [[] for i in range(int(len(adjacencyTable) / groupSize))]
	nodeQueue = [currentNode]
	visitedList = [currentNode]

	while len(nodeQueue) > 0:

		currentNode = nodeQueue.pop(0)
		visitedList.append(currentNode)
		splitList[splitCount // groupSize].append(currentNode)

		print(currentNode, end = " ")

		for adjacentNode in adjacencyTable[currentNode]:
			if adjacentNode not in visitedList:
				visitedList.append(adjacentNode)
				nodeQueue.append(adjacentNode)
		
		splitCount += 1
	print(splitList)
	return splitList

split_by_bfs(TEST_GRAPH_DICT, 3)

def get_splits_by_dfs(adjacencyTable: dict, groupSize: int, currentNode: str, visited: set=None) -> list:
	if visited == None:
		visited = set()


def get_groups_of_node_groups_of_n(adjacencyTable: dict, n: int) -> list:
	graphHasCycles = check_graph_for_cycles(TEST_GRAPH_DICT)
	
	if len(adjacencyTable) % n != 0:
		raise ValueError('The number of nodes in adjacencyTable must be a multiple of n.')
	elif 0 in [len(adjacencyTable[node]) for node in adjacencyTable]:
		raise ValueError('All nodes must have at least one adjacent node.')
	
		# Note: This is technically not true, as
		# the graph is directed and should work
		# as long as a node has a node pointing
		# to it. Maybe make the graph undirected?

	if graphHasCycles is True:
		return [split_by_bfs(adjacencyTable, n)]
	else:
		nodesWithOneEdge = [
			node for node in adjacencyTable if len(adjacencyTable[node]) == 1
		]

		return get_splits_by_dfs(adjacencyTable, n, )



	# nodesWithOneEdge = [
	# 	node for node in adjacencyTable if len(adjacencyTable[node]) == 1
	# ]

	
	# if len(nodesWithOneEdge) > 0:
	# 	cyclesInGraph = dfs_cycles_check(adjacencyTable, nodesWithOneEdge[0]) == True
	# else:
	# 	cyclesInGraph = dfs_cycles_check(adjacencyTable, adjacencyTable[0]) == True
	
	# return cyclesInGraph



groups_of_node_groups = get_groups_of_node_groups_of_n(TEST_GRAPH_DICT, 3)
