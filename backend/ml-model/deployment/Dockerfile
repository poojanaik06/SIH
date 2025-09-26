# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY prediction_api.py .

# Copy model artifacts and data (if available)
COPY ../models ./models
COPY ../data ./data

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=prediction_api.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "prediction_api:app"]