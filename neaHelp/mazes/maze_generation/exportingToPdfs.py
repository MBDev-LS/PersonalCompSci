
from pprint import pprint

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def exportToPDF(encodedMazeData: list[bool], filename: str) -> None:

	tableHeight = len(encodedMazeData)
	tableWidth = len(encodedMazeData[0])

	# ROW_HEIGHT = COLUMN_WIDTH = (min(landscape(A4)) - min(landscape(A4)) * 0.1) / 16

	ROW_HEIGHT = COLUMN_WIDTH = min((landscape(A4)[0] - 160) / tableWidth, (landscape(A4)[1] - 160) / tableHeight)

	# print(ROW_HEIGHT)

	blankData = [['' for w in range(tableWidth)] for h in range(tableHeight)]#
	# blankData[1][0] = '→'
	# blankData[tableHeight-2][tableWidth-1] = '→'

	markedCoordinates = []

	for h, rowList in enumerate(encodedMazeData):
		for w, cellVlalue in enumerate(rowList):
			if cellVlalue == True and (h, w) not in [(1, 0), (tableHeight-2, tableWidth-1)]:
				markedCoordinates.append((w, h))
				

	doc = SimpleDocTemplate(filename, pagesize=landscape(A4))
	

	elements = []

	table = Table(blankData, rowHeights=ROW_HEIGHT, colWidths=COLUMN_WIDTH)


	table.setStyle(TableStyle([('BACKGROUND', coords, coords, colors.black) for coords in markedCoordinates] + [('GRID', coords, coords, 0.1, colors.black) for coords in markedCoordinates])) #  + [('NOSPLIT', (0,0), (tableWidth-1,tableHeight-1))]

	elements.append(table)

	doc.build(elements)


