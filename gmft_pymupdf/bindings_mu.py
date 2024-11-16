
# PyMuPDF bindings
from typing import Generator
import PIL
import pymupdf

from PIL.Image import Image as PILImage

from gmft.common import Rect
from gmft.pdf_bindings.common import BasePage, BasePDFDocument


def pixmap_to_PIL(pixmap: pymupdf.Pixmap) -> PILImage:
    """
    Convert a MuPDF pixmap to a PIL Image.
    
    :param pixmap: MuPDF pixmap
    :return: PIL Image
    """
    img = PIL.Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
    return img

class PyMuPDFPage(BasePage):
    
    def __init__(self, page: pymupdf.Page):
        self.page = page
        super().__init__(page.number)
        self.width = page.bound().width
        self.height = page.bound().height
    
    def get_positions_and_text(self) -> Generator[tuple[float, float, float, float, str], None, None]:
        for word in self.page.get_text("words"):
            yield word[:5]
    
    def get_positions_and_text_mu(self) -> Generator[tuple[float, float, float, float, str, int, int, int], None, None]:
        """
        Returns positions and text with mu's additional annotations: blockno, lineno, wordno.
        
        Each tuple should be: (x0, y0, x1, y1, word, blockno, lineno, wordno)
        """
        yield from self.page.get_text("words")
    
    _get_positions_and_text_and_breaks = get_positions_and_text_mu
    
    def get_filename(self) -> str:
        return self.page.parent.name
    
    def get_image(self, dpi: int=None, rect: Rect=None) -> PILImage:
        
        img = pixmap_to_PIL(self.page.get_pixmap(dpi=dpi, clip=None if rect is None else rect.bbox))
        return img
    
    def _get_text(self) -> str:
        """Ability to reconstruct the page, with line breaks, on a word-by-word basis.
        This is useful for selectively replacing certain text with other text."""
        result = ""
        # for x0, y0, x1, y1, word, blockno, lineno, wordno in self.page.get_text('words'):
        for x0, y0, x1, y1, word, blockno, lineno, wordno in self.get_positions_and_text_mu():
            # if prev_block != blockno:
            #     prev_block = blockno
            #     result += "\n\n"
            if wordno == 0:
                result += "\n"
            else:
                result += ' '
            result += word
        return result.lstrip()

class PyMuPDFDocument(BasePDFDocument):
    
    def __init__(self, filename: str, *args, **kwargs):
        """
        Creates a PyMuPDF document, with the same arguments as https://pymupdf.readthedocs.io/en/latest/document.html#document

        To create a memory document, set filename to None and refer to PyMuPDF's documentation.
        Example:
        ```
        
        # from a file
        doc = pymupdf.open("some.xps")
        # handle wrong extension
        doc = pymupdf.open("some.file", filetype="xps")

        # from memory, filetype is required if not a PDF
        doc = pymupdf.open("xps", mem_area)
        doc = pymupdf.open(None, mem_area, "xps")
        doc = pymupdf.open(stream=mem_area, filetype="xps")

        # new empty PDF
        doc = pymupdf.open()
        doc = pymupdf.open(None)
        doc = pymupdf.open("")

        ```

        :param filename: PDF filename
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments

        """
        self.doc = pymupdf.open(filename, *args, **kwargs)
        self.filename = filename
    
    def get_page(self, n: int) -> BasePage:
        return PyMuPDFPage(self.doc[n])
    
    def get_filename(self) -> str:
        return self.filename
    
    def __len__(self) -> int:
        return len(self.doc)
    
    def close(self):
        self.doc.close()