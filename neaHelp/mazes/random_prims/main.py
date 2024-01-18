
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / 'output'

import graphs, prims, graphEncoding, exportingToPdfs

WIDTH = 16
HEIGHT = 16

graphList = graphs.generateGraph(WIDTH,HEIGHT)
graphListWithWeights = graphs.setRandomWeights(graphList)

minimumSpanningTree = graphs.removeInactiveEdges(prims.findMinimumSpanningTree(graphListWithWeights))

encodedMazeData = graphEncoding.getEncodedMazeData(minimumSpanningTree, WIDTH, HEIGHT)

print()
graphEncoding.displayMazeData(encodedMazeData)
print()

exportingToPdfs.exportToPDF(encodedMazeData, str(OUTPUT_DIR / 'test.pdf'))

