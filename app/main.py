# app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()


from app.models import (
    FileUploadResponse,
    OCRRequest,
    OCRResultResponse,
)
from app.storage.storage import save_uploaded_file, get_file_path
from app.OCR.ocr_easy import extract_text_with_easyocr
from app.OCR.llm_ocr import extract_text_with_llm_ocr
from app.OCR.llm_parser import parse_fields_with_llm

app = FastAPI(
    title="OCR Service",
    version="0.1.0",
)

# CORS needed for frontends -- for future developments )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # we will tighten in production on frontend if needed 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to the OCR system !"}


@app.post("/file-upload", response_model=FileUploadResponse)
async def file_upload(file: UploadFile = File(...)):
    """
    Accept a single file, store it locally and return a file_id.
    """
    file_bytes = await file.read()
    file_id = save_uploaded_file(file.filename, file_bytes)

    return FileUploadResponse(file_id=file_id)


@app.post("/ocr", response_model=OCRResultResponse)
async def ocr_endpoint(payload: OCRRequest):
    """
    Perform OCR (easyocr or llm_ocr), then parse requested fields via LLM.
    """
    try:
        file_path = get_file_path(payload.file_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    # 1) RAW OCR LAYER
    if payload.ocr == "easyocr":
        raw_text = extract_text_with_easyocr(file_path)
    elif payload.ocr == "llm_ocr":
        raw_text = extract_text_with_llm_ocr(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported OCR type")

    if not raw_text:
        raw_text = ""

    # 2) PARSING LAYER (LLM)
    parsed_fields = parse_fields_with_llm(raw_text, payload.fields)

    return OCRResultResponse(
        file_id=payload.file_id,
        ocr=payload.ocr,
        result=parsed_fields,
        raw_ocr=raw_text,
    )
