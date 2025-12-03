
from pathlib import Path
from openai import OpenAI
import fitz  # PyMuPDF
import base64

client = OpenAI()  # picks up OPENAI_API_KEY


def pdf_to_images(pdf_path: Path, dpi: int = 200):
    """
    Convert PDF pages to PNG bytes using PyMuPDF (no poppler required)
    """
    doc = fitz.open(pdf_path)
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        png_bytes = pix.tobytes("png")
        images.append(png_bytes)

    return images


def encode_base64(image_bytes: bytes) -> str:
    """
    Convert raw bytes → base64 string for OpenAI Vision
    """
    return base64.b64encode(image_bytes).decode("utf-8")


def extract_text_from_image_bytes(image_bytes: bytes, model: str):
    """
    Send one image to OpenAI Vision OCR
    """
    b64 = encode_base64(image_bytes)

    response = client.chat.completions.create(
        model=model,
        messages=[
          {
                "role": "system",
                "content": (
                    "You are an OCR engine. Extract **all text and numeric data** from the document, "
                    "including the labels and the values in the associated fields. "
                    "Specifically, ensure the text and number in the 'VERGİ KİMLİK NO' field are captured. "
                    "Return ONLY the extracted text, formatted clearly."
                )
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{b64}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content.strip()


def extract_text_with_llm_ocr(file_path: Path, model: str = "gpt-4o-mini"):
    """
    OCR for: PNG, JPG, PDF (with page conversion)
    """

    # CASE 1 — PDF
    if file_path.suffix.lower() == ".pdf":
        images = pdf_to_images(file_path)
        all_text = []

        for img_bytes in images:
            text = extract_text_from_image_bytes(img_bytes, model)
            all_text.append(text)

        return "\n".join(all_text)

    # CASE 2 — Normal image
    image_bytes = file_path.read_bytes()
    return extract_text_from_image_bytes(image_bytes, model)
