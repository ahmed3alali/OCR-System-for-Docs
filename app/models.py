# app/models.py
from typing import Dict, Literal, Optional
from pydantic import BaseModel, Field


class FileUploadResponse(BaseModel):
    file_id: str


class FieldSpec(BaseModel):
    name: str
    description: str
    type: str = Field(..., description="Expected type like 'string', 'integer', 'float', 'date'")


class OCRRequest(BaseModel):
    file_id: str
    ocr: Literal["easyocr", "llm_ocr"]
    fields: Dict[str, FieldSpec]


class OCRResultResponse(BaseModel):
    file_id: str
    ocr: str
    result: Dict[str, Optional[str | int | float]]
    raw_ocr: str

