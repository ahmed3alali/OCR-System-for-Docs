FROM python:3.11-slim

# --------------------
# System packages
# --------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libxrender1 \
    libxext6 \
    libsm6 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# --------------------
# Set workdir
# --------------------
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY app /app/app

# Make upload directory
RUN mkdir -p /app/app/storage/uploads

# Expose port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
