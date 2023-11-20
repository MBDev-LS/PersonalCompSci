
from math import inf
from graphs import new_test_graph as node_dict_list
import time
from pprint import pprint

import copy


class Node:
	def __init__(self, name: str, edges: list = None):
		self.name = name
		self.edges = [] if edges is None else edges

		self.previous_node = None

	def __str__(self):
		return f'<Node {self.name} [{", ".join([edge.node1.name + ": " + str(edge.weight) for edge in self.edges])}]>'

	def __repr__(self):
		return f'Node(name={self.name}, edges={self.edges})'


class Edge:
	def __init__(self, node0: Node, node1: Node, weight: int):
		self.node0 = node0
		self.node1 = node1
		self.weight = weight

	def __str__(self):
		return f'<edge n0={self.node0.name} n1={self.node1.name} weight={self.weight}>'

	def __repr__(self):
		return f'edge(node0={self.node0}, node1={self.node1}, weight={self.weight})'


def get_node_index_by_name(name: Node, node_list: list):
	for i, node in enumerate(node_list):
		if node.name == name:
			return i
	return -1


# def sort_node_list(node_list: list):
# 	return sorted(node_list, key=lambda n: n.cost, reverse=True)


t0 = time.perf_counter()

node_list = []

for node in node_dict_list:
	node_list.append(Node(node['name']))

for node in node_dict_list:
	for edge_node in node['edges']:
		node0 = get_node_index_by_name(node['name'], node_list)
		node1 = get_node_index_by_name(edge_node['node'], node_list)
		if node0 == -1 or node1 == -1:
			raise('node_dict_list not valid')

		node_list[node0].edges.append(
			Edge(node_list[node0], node_list[node1], edge_node['weight']))


# print(node_list)

def get_all_edges(nodeList: list, reverseSortEdges: bool=False) -> list:
	edgeList = []

	for node in nodeList:
		edgeList += node.edges
	
	return edgeList if reverseSortEdges is False else sorted(edgeList, key=lambda edge: edge.weight, reverse=True)


def remove_edges(nodeList: list) -> list:
	newNodeList = []

	for node in nodeList:
		newNode = copy.deepcopy(node)

		newNode.edges = []

		newNodeList.append(newNode)
	
	return newNodeList

def add_existing_edge_to_node_list(nodeList: list, edge: Edge):
	edge.node0.edges.append(edge)
	
	for node in nodeList:
		if node.name == edge.node0.name:
			pass

emptyNodeList = remove_edges(node_list)

sortedEdgeList = get_all_edges(node_list, reverseSortEdges=True)

firstEdge = sortedEdgeList.pop()

minimumSpanningTree = [firstEdge]

while len(sortedEdgeList) > 0:
	nextEdge = minimumSpanningTree

	testNodeList = copy.deepcopy(emptyNodeList)

