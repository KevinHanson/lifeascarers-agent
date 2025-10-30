# Use a lightweight Python base image
FROM python:3.11-slim

# Install curl and any system tools you need
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    grep \
 && rm -rf /var/lib/apt/lists/*
 
# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the agent
CMD ["python", "agentic_pipeline.py"]
