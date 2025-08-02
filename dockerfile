# Base image with Python and Streamlit
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libfreetype6-dev \
    libjpeg-dev \
    libpng-dev \
    libopenblas-dev \
    libfontconfig1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt ./
COPY . ./

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit default port
EXPOSE 8501

# Default command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.]()
