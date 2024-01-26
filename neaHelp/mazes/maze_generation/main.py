
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / 'output'

import graphs, prims, graphEncoding, exportingToPdfs, wilsons


def getOptionsInput(*options):
	prompt = '\n'.join([str(i+1) + ' - ' + options[i] for i in range(0, len(options))])
	print(prompt)

	user_input = input("Enter a valid choice: ")
	while user_input not in [str(i+1) for i in range(0, len(options))]:
		user_input = input("Enter a valid choice: ")
	
	return options[int(user_input)-1]


def intInput(prompt: str) -> int:
	userInput = input(prompt)

	while not userInput.isdigit():
		userInput = input(prompt)
	
	return int(userInput)


def getGeneratedMaze(mazeGenerationAlgorithmName: str, graphList: list[graphs.Node]) -> list[graphs.Node]:
	if mazeGenerationAlgorithmName == 'Prims':
		return prims.findMinimumSpanningTree(graphList)
	elif mazeGenerationAlgorithmName == 'Wilsons':
		return wilsons.findMinimumSpanningTree(graphList)
	else:
		raise Exception(f"Unkown maze generation algorithm '{mazeGenerationAlgorithmName}'")



if __name__ == '__main__':
	mazeGeneratingAlgorithm = getOptionsInput('Prims', 'Wilsons')
	mazeNum = intInput("Enter the number of mazes you'd like to generate: ")
	outputFileName = input("Enter the file name for the output PDFs ('$i' will be incremeted by one for each new maze): ")
	
	mazeHeight = intInput('Enter maze height: ')
	mazeWidth = intInput('Enter maze width: ')

	for i in range(mazeNum):
		graphList = graphs.generateGraph(mazeWidth, mazeHeight, setUniformWeights=True)
		mazeList = getGeneratedMaze(mazeGeneratingAlgorithm, graphList)

		# while graphs.checkForSwastika(mazeList, mazeWidth) or graphs.checkForSwastika(mazeList, mazeWidth, True):
		# 	mazeList = getGeneratedMaze(mazeGeneratingAlgorithm, graphList)

		minimumSpanningTree = graphs.removeInactiveEdges(mazeList)
		encodedMazeData = graphEncoding.getEncodedMazeData(mazeList, mazeWidth, mazeHeight)
		graphEncoding.displayMazeData(encodedMazeData)

		exportingToPdfs.exportToPDF(encodedMazeData, str(OUTPUT_DIR / outputFileName.replace('$i', str(i+1))))




