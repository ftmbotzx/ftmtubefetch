# Use the official Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy the repository files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose Railway's default port
EXPOSE 8080

# Start Gunicorn and the bot together
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:8080 & python3 bot.py"]
