FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend
COPY .env.example .env

# Create data directory
RUN mkdir -p data logs

# Expose port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
