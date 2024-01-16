from pathlib import Path
from pypdf import PdfMerger

BASE_DIR = Path(__file__).resolve().parent
INPUT_ONE_DIR = BASE_DIR / 'input1'
INPUT_TWO_DIR = BASE_DIR / 'input2'
OUTPUT_DIR = BASE_DIR / 'output'

from os import listdir
from os.path import isfile, join

input1Files = [f for f in listdir(INPUT_ONE_DIR) if isfile(join(INPUT_ONE_DIR, f))]


print(input1Files)

for inputPdfName in input1Files:
    idNumber = inputPdfName.split(' ')[0]

    pdfs = [INPUT_ONE_DIR / inputPdfName,  INPUT_TWO_DIR / inputPdfName]

    merger = PdfMerger()

    for pdf in pdfs:
        merger.append(pdf)

    merger.write(OUTPUT_DIR / inputPdfName)
    merger.close()