# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y unzip curl build-essential git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies (including pymongo)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# ✅ Build the Reflex app with debug fallback
RUN reflex export --env prod || (echo " Reflex export failed" && cat ~/.reflex/logs/*.log || true && exit 1)

# Set the port Cloud Run expects
EXPOSE 8080

# ✅ Start backend using Python (ensures PORT is respected)
CMD ["python", "-m", "reflex.run", "--backend-port", "8080", "--env", "prod"]