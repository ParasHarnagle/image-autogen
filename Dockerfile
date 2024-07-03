FROM python:3.9-slim

# System dependencies for Pillow (image processing)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl-dev \
    tk-dev

WORKDIR /app

# Copy the application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Start Streamlit
CMD ["streamlit", "run", "app.py"]
