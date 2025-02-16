FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000  

# Health check (optional but recommended)
HEALTHCHECK --interval=5s --timeout=5s --retries=3 CMD ["curl", "-f", "http://localhost:8000/health"] || exit 1

# No CMD needed; the base image handles it.

# Set environment variables if needed (or pass them at runtime as instructed)
# ENV AIPROXY_TOKEN=your_token_here (better to pass at runtime)