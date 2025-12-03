# OCR Service – EasyOCR + LLM OCR

A production-ready OCR microservice built with **FastAPI**, supporting:

- **EasyOCR** (local OCR engine)
- **LLM-based OCR** using OpenAI (Vision for images, direct text extraction for PDFs)
- **LLM parsing for structured field extraction**
- **Local file storage**
- **Dockerization**

This service allows users to upload any **Vergi Levhası** document and request **specific fields** (e.g., "Vergi Kimlik No"). The backend handles OCR + parsing and returns clean structured results.

---

## Features of our app : - 

### EasyOCR Processing
- PDF files are converted to images using **PyMuPDF** (EasyOCR only accepts images)
- Returns merged OCR text (e.g., `["VERGİ", "KİMLİK", "NO", "1111111"]`)

### Smart Field Parsing (LLM)
After extracting raw text, an LLM model parses the fields:
- Numbers
- Dates
- Names
- Tax IDs
- Any custom fields defined by user

---


### Important Notes
- **OpenAI API Key Required**: Add your own OpenAI key in an `.env` file
- **MacOS SSL Issue**: If using EasyOCR on MacOS, you may encounter SSL certification problems. Run this command to fix:
  ```bash
  /Applications/Python\ 3.11/Install\ Certificates.command
  ```

---

##  Running with Docker

1. Navigate to the `BACKEND` folder:
   ```bash
   cd BACKEND
   ```

2. Build the Docker image:
   ```bash
   docker build -t ocr-service .
   ```

3. Run the container:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e OPENAI_API_KEY="your-key-here" \
     ocr-service
   ```

4. The service will be running on `http://localhost:8000`

---

## Running with UV (Local Development)

1. Navigate to the `BACKEND` folder:
   ```bash
   cd BACKEND
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

4. Activate the environment:
   - **MacOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

5. Run the server:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

---

## API Endpoints

### 1. Upload File

**Endpoint:** `POST /file-upload`

Uploads a file and returns a unique file ID.

**Example:**
```bash
curl -X POST "http://localhost:8000/file-upload" \
  -F "file=@'/path/to/document.pdf'"
```

**Response:**
```json
{
  "file_id": "218fb967-e004-4671-8dbf-0405ff9401b3"
}
```

---

### 2. OCR with EasyOCR

**Endpoint:** `POST /ocr`

Extracts text using EasyOCR and parses specified fields.

**Example:**
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "7f3b73e7-c633-4ea7-bf91-b509eedc6399",
    "ocr": "easyocr",
    "fields": {
      "field_1a": {
        "name": "Vergi Numarası",
        "description": "Extract the vergi no from the document",
        "type": "integer"
      }
    }
  }'
```

**Response:**
```json
{
  "file_id": "7f3b73e7-c633-4ea7-bf91-b509eedc6399",
  "ocr": "easyocr",
  "result": {
    "field_1a": 00000000
  },
  "raw_ocr": "info from your document"
}
```

---

### 3. OCR with LLM

**Endpoint:** `POST /ocr`

Extracts text using OpenAI's Vision API (for images) or direct text extraction (for PDFs), then parses fields with LLM.

**Example:**
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "Content-Type: application/json" \
  -d '{
    "file_id": "351c6c5d-f0b6-4348-a548-bcf99964d7f2",
    "ocr": "llm_ocr",
    "fields": {
      "field_1a": {
        "name": "Vergi Numarası",
        "description": "Extract the vergi no from the document",
        "type": "integer"
      }
    }
  }'
```

**Response:**
```json
{
  "file_id": "351c6c5d-f0b6-4348-a548-bcf99964d7f2",
  "ocr": "llm_ocr",
  "result": {
    "field_1a": 0000000
  },
  "raw_ocr": "```\nInfo text from your document\n```"
}
```

---

## Technology Stack

- **FastAPI** - Modern web framework
- **EasyOCR** - Local OCR engine
- **OpenAI API** - LLM-based OCR and parsing
- **PyMuPDF** - PDF to image conversion
- **Docker** - Containerization
- **UV** - Fast Python package installer
