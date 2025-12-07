FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway/Render will set PORT env var)
EXPOSE 8050

# Use gunicorn to run the app
# PORT will be set by Railway/Render, default to 8050 if not set
CMD sh -c "gunicorn src.app:server --bind 0.0.0.0:${PORT:-8050} --workers 2 --threads 4 --timeout 120"

