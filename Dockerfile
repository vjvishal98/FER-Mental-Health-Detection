FROM pytorch/pytorch:2.0.0-cpu

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for OpenCV, ffmpeg and general builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    wget \
    ca-certificates \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy source and requirements
COPY . /app
COPY requirements.txt ./requirements.txt

# Upgrade pip and install Streamlit
RUN python -m pip install --upgrade pip
RUN pip install streamlit

# Install all requirements except torch (we use the system-provided torch in the base image)
RUN sed '/^torch/Id' requirements.txt > req_no_torch.txt \
 && pip install --no-cache-dir -r req_no_torch.txt

ENV PORT=8502
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

EXPOSE 8502

CMD ["streamlit", "run", "dashboard.py", "--server.port", "8502", "--server.headless", "true"]
