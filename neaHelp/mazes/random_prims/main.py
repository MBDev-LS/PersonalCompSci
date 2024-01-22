
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / 'output'

import graphs, prims, graphEncoding, exportingToPdfs, wilsons

WIDTH = 16
HEIGHT = 16

graphList = graphs.generateGraph(WIDTH, HEIGHT, setUniformWeights=True)
# graphListWithWeights = graphs.setRandomWeights(graphList)
graphListWithWeights = graphs.setUniformWeights(graphList)

timeList = []

for i in range(10000):
	t0 = time.perf_counter()
	# mazeList = wilsons.findMinimumSpanningTree(graphListWithWeights)
	mazeList = prims.findMinimumSpanningTree(graphListWithWeights)
	t1 = time.perf_counter()

	timeList.append(t1-t0)

	# print(f'Generation time: {t1-t0}')

print(f'Mean generation time: {sum(timeList) / len(timeList)}')

minimumSpanningTree = graphs.removeInactiveEdges(mazeList)

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