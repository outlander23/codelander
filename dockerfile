FROM python:3.10-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    --extra-index-url https://download.pytorch.org/whl/cpu

# Copy application code
COPY app.py .

# Copy the local Hugging Face model into the image
COPY codelander ./codelander

EXPOSE 8345

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8345"]
