FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000  

# Health check (optional but recommended)
HEALTHCHECK --interval=5s --timeout=5s --retries=3 CMD ["curl", "-f", "http://localhost:8000/health"] || exit 1