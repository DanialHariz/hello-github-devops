# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y unzip curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Reflex uses
#EXPOSE 3000

# Use the Cloud Run port (Google injects $PORT, default 8080)
EXPOSE 8080

# Start the Reflex app
CMD ["reflex", "run", "--backend-port", "8080", "--env", "dev"]


