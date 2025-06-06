FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y build-essential git \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt

COPY . .

# Spustí FastAPI server na portu 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
