FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install vLLM (optimized for inference)
RUN pip3 install vllm==0.5.0 fastapi uvicorn

# Download model during build to avoid runtime downloads
# This caches the model in the container
RUN python3 -c "from vllm import LLM; LLM('facebook/opt-125m')"

# API server
COPY app.py /app/app.py
WORKDIR /app

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
