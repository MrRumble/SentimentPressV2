# Use an official lightweight Python image as the base
FROM python:3.10-slim

# Install system dependencies required by psycopg
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to install dependencies first (improves caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask runs on
EXPOSE 5002

# Define the command to run the app
CMD ["python", "run.py"]
