# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y unzip curl build-essential git && \
    rm -rf /var/lib/apt/lists/*

# Install Reflex CLI globally
RUN pip install --no-cache-dir reflex

# Copy source files
COPY . .

# ✅ Build the Reflex app (no --backend-port here!)
RUN reflex export --env prod

# Set port for Cloud Run
EXPOSE 8080

# ✅ Run the already-built backend
CMD ["python", "-m", "reflex.run", "--backend-port", "8080", "--env", "prod"]
