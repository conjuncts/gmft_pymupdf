from gmft_pymupdf import PyMuPDFDocument

# try https://github.com/conjuncts/gmft/blob/main/test/samples/tiny.pdf
doc = PyMuPDFDocument("tiny.pdf")

# gmft remains unchanged
from gmft import TableDetector
detector = TableDetector()

tables = detector.extract(doc[0])

print(tables[0].text())