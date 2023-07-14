

import config

# TEST_GRAPH_DICT = config.GRAPH_DICT

TEST_GRAPH_DICT = {
	'A': ['B'],
	'B': ['C'],
	'C': [],
	'D': ['B']
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



print(check_graph_for_cycles(TEST_GRAPH_DICT))

def check_graph_for_cycles2(adjacencyTable: dict) -> bool:
	if len(adjacencyTable) == 0:
		return False

	nodesWithOneEdge = [
		node for node in adjacencyTable if len(adjacencyTable[node]) == 1
	]

	
	if len(nodesWithOneEdge) > 0:
		cyclesInGraph = dfs_cycles_check(adjacencyTable, nodesWithOneEdge[0]) == True
	else:
		cyclesInGraph = dfs_cycles_check(adjacencyTable, adjacencyTable[0]) == True
	
	return cyclesInGraph