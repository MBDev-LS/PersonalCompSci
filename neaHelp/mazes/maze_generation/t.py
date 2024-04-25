import heapq

class Graph:
	def __init__(self, vertices):
		self.vertices = vertices
		self.adjacency_list = [[] for _ in range(vertices)]

	def add_edge(self, u, v, weight):
		self.adjacency_list[u].append((v, weight))
		self.adjacency_list[v].append((u, weight))

	def prim(self):
		visited = [False] * self.vertices
		min_heap = []
		minimum_spanning_tree = []

		# Start with vertex 0
		heapq.heappush(min_heap, (0, 0))

		while min_heap:
			weight, vertex = heapq.heappop(min_heap)

			if visited[vertex]:
				continue

			visited[vertex] = True

			if vertex != 0:
				minimum_spanning_tree.append((vertex, weight))

			for neighbor, edge_weight in self.adjacency_list[vertex]:
				if not visited[neighbor]:
					heapq.heappush(min_heap, (edge_weight, neighbor))

		return minimum_spanning_tree



	def draw_graph(graph):
		import matplotlib.pyplot as plt

		for u in range(graph.vertices):
			for v, weight in graph.adjacency_list[u]:
				plt.plot([u, v], [0, weight], 'bo-')

		plt.xlabel('Vertex')
		plt.ylabel('Weight')
		plt.title('Graph')
		plt.show()


# Example usage
g = Graph(5)
g.add_edge(0, 1, 2)
g.add_edge(0, 3, 6)
g.add_edge(1, 2, 3)
g.add_edge(1, 3, 8)
g.add_edge(1, 4, 5)
g.add_edge(2, 4, 7)
g.add_edge(3, 4, 9)

minimum_spanning_tree = g.prim()

print("Minimum Spanning Tree:")
for edge in minimum_spanning_tree:
	print(edge)

g.draw_graph()

