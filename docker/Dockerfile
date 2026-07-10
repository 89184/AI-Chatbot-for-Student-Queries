FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (required for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Create necessary directories
RUN mkdir -p backend data frontend logs

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet')"

# Train the model (optional - you can skip this if model is already trained)
# This will run during build
RUN python backend/train.py || echo "Model training skipped, using existing model"

# Expose the port
EXPOSE 5000

# Run with gunicorn (production server)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]