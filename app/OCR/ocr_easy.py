
from pathlib import Path
from typing import Optional
import easyocr
import fitz  # PyMuPDF
from PIL import Image
import io
import tempfile
import os


_reader: Optional[easyocr.Reader] = None


def get_reader(lang_list=("en", "tr")) -> easyocr.Reader:
    """
    Creates and caches the EasyOCR reader.
    """
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(list(lang_list)) 
    return _reader


def pdf_to_images(pdf_path: Path, dpi: int = 200):
    """
    Convert PDF pages to images using PyMuPDF (no poppler required).
    Returns a list of PIL Image objects.
    """
    doc = fitz.open(pdf_path)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=dpi)          # rasterize page
        img_bytes = pix.tobytes("png")          # convert to PNG bytes
        img = Image.open(io.BytesIO(img_bytes)) # load into PIL
        images.append(img)

    return images


def extract_text_with_easyocr(file_path: Path) -> str:
    """
    Extract text from an image or a PDF using EasyOCR.
    """

    reader = get_reader()

    # --- CASE 1: PDF ---
    if file_path.suffix.lower() == ".pdf":
        text_blocks = []
        images = pdf_to_images(file_path)

        with tempfile.TemporaryDirectory() as temp_dir:
            for idx, img in enumerate(images):
                img_temp_path = os.path.join(temp_dir, f"page_{idx}.png")
                img.save(img_temp_path, "PNG")

                results = reader.readtext(img_temp_path, detail=0)
                text_blocks.append("\n".join(results))

        return "\n".join(text_blocks)

    # --- CASE 2: Image (JPG, PNG, etc.) ---
    results = reader.readtext(str(file_path), detail=0)
    return "\n".join(results)
