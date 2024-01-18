
from pprint import pprint

import graphs
import prims
import kruskals


def displayMazeData(mazeData: list[bool]) -> None:
	for row in mazeData:
		print(''.join(["⬜️" if value == False else "⬛️" for value in row]))


def getMazeDataForDisplay(mazeData: list[bool]) -> None:
	return [''.join(["⬜️" if value == False else "🟥" for value in row]) for row in mazeData]


def getEncodedMazeData(minimumSpanningTree: list[graphs.Node], width: int, height: int) -> list:
	tableWidth = width * 2 + 1
	tableHeight = height * 2 + 1

	mazeData = [[None for w in range(tableWidth)] for h in range (tableHeight)]

	mazeData[0] = mazeData[tableHeight - 1] = [True for w in range(tableWidth)]
	
	for i in range(1, tableHeight-1):
		mazeData[i][0] = mazeData[i][tableWidth - 1] = True

	currentNodeIndex = 0

	for h in range(1, tableHeight - 1, 2):
		for w in range(1, tableWidth - 1, 2):
			currentNode = minimumSpanningTree[currentNodeIndex]

			mazeData[h][w] = False

			print(f'At [{h}][{w}]:')
			print(f'	UP: 	{str(currentNode.upEdge)} - [{h-1}][{w}]')
			print(f'	LEFT: 	{str(currentNode.leftEdge)} - [{h}][{w-1}]')
			print(f'	DOWN: 	{str(currentNode.downEdge)} - [{h-1}][{w}]')

			if mazeData[h-1][w] != False:
				mazeData[h-1][w] = currentNode.upEdge == None
			
			if mazeData[h][w+1] != False:
				mazeData[h][w+1] = currentNode.rightEdge == None 
			
			if mazeData[h+1][w] != False:
				mazeData[h+1][w] = currentNode.downEdge == None
			
			if mazeData[h][w-1] != False:
				mazeData[h][w-1] = currentNode.leftEdge == None
			
			currentNodeIndex += 1

	return mazeData


if __name__ == '__main__':
	WIDTH = 16
	HEIGHT = 16

	graphList = graphs.generateGraph(WIDTH,HEIGHT)
	graphListWithWeights = graphs.setRandomWeights(graphList)

	minimumSpanningTree = graphs.removeInactiveEdges(prims.findMinimumSpanningTree(graphListWithWeights))

	for node in minimumSpanningTree:
		print('\n____________________\n', node)
		for edge in prims.getAdjacentEdges(node):
			if edge != None and edge.active == True:
				print(edge)


	print('--------------------------------')




	# pprint([str(edge) for edge in kruskals.getEdgeList(minimumSpanningTree)])

	encodedMazeData = getEncodedMazeData(minimumSpanningTree, WIDTH, HEIGHT)

	pprint(encodedMazeData)

	displayMazeData(encodedMazeData)

	# for row in encodedMazeData:
	# 	print(''.join(["⬜️" if value == False else "🟥" for value in row]))