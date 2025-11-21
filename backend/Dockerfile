FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set Hugging Face cache path (so it's predictable)
ENV HF_HOME=/models/hf_cache

COPY . .

# Pre-download the CLIP model at build time (so container is self-contained)
# RUN python -c "from transformers import pipeline; pipeline('zero-shot-image-classification', model='openai/clip-vit-base-patch32')"

# Expose port (optional, for clarity)
EXPOSE 8000

COPY alembic.ini ./alembic.ini
COPY migrations ./migrations

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
