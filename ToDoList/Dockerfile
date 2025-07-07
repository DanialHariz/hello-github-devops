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

# ✅ Add this line to make sure 'reflex' is in PATH
RUN ln -s /usr/local/bin/python3 /usr/bin/python && \
    ln -s /usr/local/bin/reflex /usr/bin/reflex

# Copy the rest of the app
COPY . .

# Expose the correct port
EXPOSE 8080

# Start the Reflex app
CMD ["reflex", "run", "--backend-port", "8080", "--env", "dev"]