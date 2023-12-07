# Use an official lightweight Python image.
FROM python:3.9-slim

# Define environment variables for Python unbuffered mode and headless Chrome.
ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

# Set the working directory in the container to /app.
WORKDIR /app

# Install system dependencies for Chrome, xvfb, and ffmpeg.
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium-driver \
    xvfb \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies.
# Copy the requirements.txt file into the container at /app.
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container at /app.
COPY . /app

# Start Xvfb for headless Chrome operation.
RUN Xvfb :99 -screen 0 1024x768x16 &

# Your application runs on port 4000, so expose that port.
EXPOSE 4000

# Run main.py when the container launches.
CMD ["python", "main.py"]
