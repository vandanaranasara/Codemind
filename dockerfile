# Use official Python image
FROM python:3.12-slim

# Install system dependencies for psycopg2
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Expose port your app runs on
EXPOSE 8000

# Command to run your app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
