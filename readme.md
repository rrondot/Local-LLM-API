# LLM API Project

A FastAPI application for interacting with Ollama language models with benchmarking tools.

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

## API Endpoints

- `GET /health` - Check API health status
- `POST /chat` - Generate text from a prompt
