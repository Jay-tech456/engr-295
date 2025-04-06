FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, including CA certificates for SSL verification
RUN apt-get update && apt-get install -y \
    gcc libpq-dev build-essential libssl-dev ca-certificates \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that the Flask app runs on (if using Flask)
EXPOSE 5001

# Command to run the Flask application
CMD ["python", "app.py"]