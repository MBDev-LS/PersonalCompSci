
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / 'output'

import graphs, prims, graphEncoding, exportingToPdfs

WIDTH = 22
HEIGHT = 11

graphList = graphs.generateGraph(WIDTH, HEIGHT, setUniformWeights=True)
# graphListWithWeights = graphs.setRandomWeights(graphList)
graphListWithWeights = graphs.setUniformWeights(graphList)

minimumSpanningTree = graphs.removeInactiveEdges(prims.findMinimumSpanningTree(graphListWithWeights))

encodedMazeData = graphEncoding.getEncodedMazeData(minimumSpanningTree, WIDTH, HEIGHT)

print()
graphEncoding.displayMazeData(encodedMazeData)
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