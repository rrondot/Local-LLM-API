# LLM API Project

A FastAPI-based application for interacting with Ollama language models, featuring comprehensive benchmarking and reporting tools.

## Prerequisites

- Python 3.x
- [Ollama](https://ollama.ai/) installed on your system
- An Ollama model (this project was tested with `llama3.1:8b`)
- Docker (optional, for containerized deployment)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

Install Ollama on your system and download a model of your choice. This project was tested with `llama3.1:8b`.

## Getting Started

### Start Ollama Server

Launch the Ollama service:

```bash
ollama serve
```

### Start FastAPI Application

Launch the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Usage

### Testing the API

Test the LLM with the API:

```bash
python test.py
```

### Performance Benchmarking

Display token usage, generation latency, tokens per second, and memory usage:

```bash
python benchmark.py
```

### Generate Reports

Generate a comprehensive performance report:

```bash
python generate_report.py
```

## Docker Deployment

This application has been containerized for easy deployment with GPU support.

### Build the Container

```bash
docker build -t llm-api:v1 .
```

### Run with Different Models

#### TinyLlama (Recommended for Testing)

```bash
docker run --gpus all -p 8000:8000 \
  -e MODEL_NAME="TinyLlama/TinyLlama-1.1B-Chat-v1.0" \
  llm-api:v1
```

#### OPT-125M (Faster but Lower Quality)

```bash
docker run --gpus all -p 8000:8000 \
  -e MODEL_NAME="facebook/opt-125m" \
  llm-api:v1
```

### Test the Docker Deployment

Check API health:

```bash
curl http://localhost:8000/health
```

Generate text:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain baseball in one sentence",
    "max_tokens": 50
  }'
```

## API Endpoints

- `GET /health` - Check API health status
- `POST /chat` - Generate text from a prompt
