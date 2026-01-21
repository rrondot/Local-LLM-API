# AI Coding Guidelines for Local-LLM-API

## Architecture Overview
This project implements two LLM API variants:
- **Local Ollama API** (`app/`): FastAPI wrapper around Ollama for CPU-based inference
- **GPU-accelerated API** (`docker/`): vLLM-based FastAPI server for GPU inference

Key components:
- `app/main.py`: FastAPI endpoints (/health, /models, /chat) routing to Ollama
- `app/ollama_client.py`: Direct HTTP client to Ollama's `/api/generate` endpoint
- `docker/app.py`: vLLM-powered endpoints with model preloading and GPU metrics

## Developer Workflows
### Local Development
```bash
# Start Ollama server
ollama serve

# Run FastAPI app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Test API
python app/test.py

# Benchmark Ollama directly
python app/benchmark.py

# Generate benchmark report
python app/generate_report.py
```

### Docker Deployment
```bash
cd docker
docker build -t llm-api:v1 .
docker run --gpus all -p 8000:8000 -e MODEL_NAME="facebook/opt-125m" llm-api:v1
```

## Code Patterns
### API Requests
Use Pydantic models for request/response validation:
```python
class ChatRequest(BaseModel):
    model: str = "llama3.1:8b"  # Default model in requests
    prompt: str
```

### Ollama Integration
Direct HTTP calls to `http://localhost:11434/api/generate`:
```python
payload = {"model": model, "prompt": prompt, "stream": False}
response = requests.post(f"{OLLAMA_URL}/api/generate", json=payload).json()
```

### Error Handling
Raise HTTPException for API errors:
```python
except requests.exceptions.RequestException as e:
    raise HTTPException(status_code=502, detail=f"Ollama service error: {str(e)}")
```

### vLLM Usage
Preload models at startup, use SamplingParams for generation:
```python
llm = LLM(model=MODEL_NAME, max_model_len=2048, gpu_memory_utilization=0.9)
outputs = llm.generate([prompt], SamplingParams(temperature=0.7, max_tokens=100))
```

## Key Files
- `app/main.py`: Main FastAPI app with Ollama routing
- `docker/app.py`: GPU-accelerated vLLM implementation
- `app/benchmark.py`: Performance testing against Ollama API
- `docker/Dockerfile`: NVIDIA CUDA base with vLLM installation</content>
<parameter name="filePath">/home/admin/Local-LLM-API/.github/copilot-instructions.md