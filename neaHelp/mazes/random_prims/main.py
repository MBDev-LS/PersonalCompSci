
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / 'output'

import graphs, prims, graphEncoding, exportingToPdfs, wilsons

WIDTH = 3
HEIGHT = 3

graphList = graphs.generateGraph(WIDTH, HEIGHT, setUniformWeights=True)
# graphListWithWeights = graphs.setRandomWeights(graphList)
# graphListWithWeights = graphs.setUniformWeights(graphList)

timeList = []

# mazeList = wilsons.findMinimumSpanningTree(graphList)

mazeList = graphList
graphList[0].downEdge.active = True
graphList[1].rightEdge.active = True
graphList[4].upEdge.active = True
graphList[4].leftEdge.active = True
graphList[4].rightEdge.active = True
graphList[4].downEdge.active = True
graphList[5].downEdge.active = True
graphList[7].leftEdge.active = True


minimumSpanningTree = graphs.removeInactiveEdges(mazeList)
encodedMazeData = graphEncoding.getEncodedMazeData(minimumSpanningTree, WIDTH, HEIGHT)

print()
graphEncoding.displayMazeData(encodedMazeData)

print(graphs.checkForSwastika(mazeList, WIDTH), graphs.checkForSwastika(mazeList, WIDTH, True))
# mazeList = prims.findMinimumSpanningTree(graphListWithWeights)




print()

exportingToPdfs.exportToPDF(encodedMazeData, str(OUTPUT_DIR / 'test.pdf'))

# for i in range(20):
# 	graphList = graphs.generateGraph(WIDTH, HEIGHT, setUniformWeights=True)
# 	# graphListWithWeights = graphs.setRandomWeights(graphList)
# 	graphListWithWeights = graphs.setUniformWeights(graphList)

# 	minimumSpanningTree = graphs.removeInactiveEdges(prims.findMinimumSpanningTree(graphListWithWeights))

# 	encodedMazeData = graphEncoding.getEncodedMazeData(minimumSpanningTree, WIDTH, HEIGHT)

# 	print()
# 	graphEncoding.displayMazeData(encodedMazeData)
# 	print()

# 	exportingToPdfs.exportToPDF(encodedMazeData, str(OUTPUT_DIR / f'test_{i}.pdf'))