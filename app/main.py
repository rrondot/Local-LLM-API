from fastapi import FastAPI, HTTPException, Security
from fastapi.responses import Response
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import time
import os
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry
import psutil
from ollama_client import generate

app = FastAPI()

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(key: str = Security(api_key_header)):
    if not API_KEY:
        return None
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return key


registry = CollectorRegistry()

REQUEST_COUNT = Counter('llm_requests_total', 'Total requests', ['model', 'status'], registry=registry)
REQUEST_DURATION = Histogram('llm_request_duration_seconds', 'Request duration', ['model'], registry=registry)
TOKENS_GENERATED = Counter('llm_tokens_generated_total', 'Tokens generated', ['model'], registry=registry)
TOKENS_INPUT = Counter('llm_tokens_input_total', 'Input tokens', ['model'], registry=registry)
OLLAMA_DURATION = Histogram('ollama_api_duration_seconds', 'Ollama API duration', ['model'], registry=registry)
OLLAMA_ERRORS = Counter('ollama_errors_total', 'Ollama errors', ['error_type'], registry=registry)
ACTIVE_REQUESTS = Gauge('llm_active_requests', 'Active requests', registry=registry)
CPU_USAGE = Gauge('llm_cpu_usage_percent', 'CPU usage', registry=registry)
MEMORY_USAGE = Gauge('llm_memory_usage_bytes', 'Memory usage', registry=registry)

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.1:8b")

class ChatRequest(BaseModel):
    prompt: str
    model: str = DEFAULT_MODEL
    temperature: float = 0.7
    max_tokens: int = 100

class ChatResponse(BaseModel):
    response: str
    model: str
    tokens_generated: int = 0
    latency_ms: float = 0

@app.get("/health")
def health():
    cpu = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    return {
        "status": "healthy",
        "default_model": DEFAULT_MODEL,
        "cpu_percent": cpu,
        "memory_percent": mem.percent
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, api_key: str = Security(verify_api_key)):
    start = time.time()
    model = request.model
    
    ACTIVE_REQUESTS.inc()
    
    try:
        input_tokens = len(request.prompt) // 4
        TOKENS_INPUT.labels(model=model).inc(input_tokens)
        
        ollama_start = time.time()
        result = generate(model=model, prompt=request.prompt, stream=False)
        OLLAMA_DURATION.labels(model=model).observe(time.time() - ollama_start)
        
        response_text = result.get("response", "")
        tokens_out = result.get("eval_count", 0)
        
        if tokens_out > 0:
            TOKENS_GENERATED.labels(model=model).inc(tokens_out)
        
        duration = time.time() - start
        REQUEST_DURATION.labels(model=model).observe(duration)
        REQUEST_COUNT.labels(model=model, status="success").inc()
        
        CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
        MEMORY_USAGE.set(psutil.virtual_memory().used)
        
        return ChatResponse(
            response=response_text,
            model=model,
            tokens_generated=tokens_out,
            latency_ms=round(duration * 1000, 2)
        )
        
    except Exception as e:
        error_type = type(e).__name__
        OLLAMA_ERRORS.labels(error_type=error_type).inc()
        REQUEST_COUNT.labels(model=model, status="error").inc()
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        ACTIVE_REQUESTS.dec()

@app.get("/metrics")
def metrics():
    CPU_USAGE.set(psutil.cpu_percent(interval=0.1))
    MEMORY_USAGE.set(psutil.virtual_memory().used)
    return Response(content=generate_latest(registry), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def root():
    return {
        "service": "LLM API",
        "default_model": DEFAULT_MODEL
    }