# Use official Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install uv and create a virtual environment
RUN pip install uv && uv venv && uv pip install -r requirements.txt

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the application
CMD ["uv", "pip", "install", "--system"] && ["python", "agent.py"]