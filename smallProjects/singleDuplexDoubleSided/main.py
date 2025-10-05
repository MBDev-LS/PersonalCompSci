
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

from pypdf import PdfReader, PdfWriter
import re

PDF_EXT_REGEX = r'\.pdf$'


def getEvenPages(pdfReader: PdfReader, numOfPages: int) -> list:
	evenPagesList = []

	for pageNum in range(1, numOfPages, 2): # Note: zero-indexed, so 1 is page 2 (even)
		evenPagesList.append(pdfReader.pages[pageNum])

	return evenPagesList


def getOddPages(pdfReader: PdfReader, numOfPages: int) -> list:
	oddPagesList = []

	for pageNum in range(0, numOfPages, 2): # Note: zero-indexed, so 0 is page 1 (odd)
		oddPagesList.append(pdfReader.pages[pageNum])

	return oddPagesList


def exportPageListToPdf(pageList: str, outputFileName: str) -> None:
	pdfWriter = PdfWriter()

	for pageObject in pageList:
		pdfWriter.add_page(pageObject)
	
	pdfWriter.write(outputFileName)



def splitPagesForPrinting(inputFileName):
	pdfReader = PdfReader(inputFileName)

	numOfPages = len(pdfReader.pages)
	evenPagesListReversed = reversed(getEvenPages(pdfReader, numOfPages))
	oddPagesList = getOddPages(pdfReader, numOfPages)

	fileNameIncludesExtension = bool(re.search(PDF_EXT_REGEX, str(inputFileName)))
	fileNameWithNoExtension = re.sub(PDF_EXT_REGEX, '', str(inputFileName), flags=re.IGNORECASE)
	outputExtensionString = '.pdf' if fileNameIncludesExtension == True else ''
	
	exportPageListToPdf(evenPagesListReversed, f'{str(fileNameWithNoExtension)} [PRINT FIRST]{outputExtensionString}')
	exportPageListToPdf(oddPagesList, f'{str(fileNameWithNoExtension)} [PRINT SECOND]{outputExtensionString}')


if __name__ == '__main__':
	splitPagesForPrinting(BASE_DIR / 'AQA Paper 2 Insert - June 2022.pdf')



# """
# ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
# ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
# □ ■ □ ■ □ ■ □ ■
# ■ □ ■ □ ■ □ ■ □
# □ ■ □ ■ □ ■ □ ■
# ■ □ ■ □ ■ □ ■ □
# ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
# ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
# """