# Use official Python image
FROM python:3.11-slim

# Install Node.js for Prettier
RUN apt-get update && apt-get install -y nodejs npm && \
    npm install -g npx && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies using uv
RUN pip install uv && uv pip install --system

# Ensure Prettier is installed
RUN npm install --save-dev --save-exact prettier

# Expose FastAPI default port
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "agent:app", "--host", "0.0.0.0", "--port", "8000"]