# gmft_pymupdf

Use [pymupdf](https://github.com/pymupdf/PyMuPDF) with [gmft](https://github.com/conjuncts/gmft).

## Installation

```bash
pip install git+https://github.com/conjuncts/gmft_pymupdf.git
```

## Usage

```python
from gmft_pymupdf import PyMuPDFDocument

doc = PyMuPDFDocument("path/to/pdf")

# gmft remains unchanged
from gmft.auto import TableDetector
detector = TableDetector()

tables = []
for page in doc:
    tables += detector.extract(page)

```

## License

gmft_pymupdf is licensed under AGPL-3.0, in accordance with PyMuPDF's AGPL-3.0 license.
