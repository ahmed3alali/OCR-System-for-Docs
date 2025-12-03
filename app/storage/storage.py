# app/storage.py
import os
import uuid
from pathlib import Path
from typing import Tuple

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(filename: str, file_bytes: bytes) -> str:
    """
    Save uploaded file under a generated UUID file_id.

    Returns:
        file_id (str)
    """
    file_id = str(uuid.uuid4())
    # Preserve original extension if exists
    ext = os.path.splitext(filename)[1]
    stored_name = f"{file_id}{ext}"
    stored_path = UPLOAD_DIR / stored_name

    with open(stored_path, "wb") as f:
        f.write(file_bytes)

    return file_id


def get_file_path(file_id: str) -> Path:
    """
    Find the stored file matching the file_id (by prefix).
    We saved files as <file_id>.<ext>
    """
    for path in UPLOAD_DIR.iterdir():
        if path.name.startswith(file_id):
            return path
    raise FileNotFoundError(f"File with id {file_id} not found")
