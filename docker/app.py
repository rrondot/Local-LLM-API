
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
import time
import os

app = FastAPI()


MODEL_NAME = os.getenv("MODEL_NAME", "facebook/opt-125m")
llm = LLM(
    model=MODEL_NAME,
    max_model_len=2048,
    gpu_memory_utilization=0.9 
)

class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    tokens_generated: int
    latency_ms: float

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "gpu_available": True
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    start = time.time()
    
    sampling_params = SamplingParams(
        temperature=request.temperature,
        max_tokens=request.max_tokens
    )
    
    outputs = llm.generate([request.prompt], sampling_params)
    
    latency = (time.time() - start) * 1000
    
    return ChatResponse(
        response=outputs[0].outputs[0].text,
        tokens_generated=len(outputs[0].outputs[0].token_ids),
        latency_ms=round(latency, 2)
    )

@app.get("/metrics")
def metrics():
    """Basic metrics for monitoring"""
    return {
        "model": MODEL_NAME,
        "gpu_memory_allocated": "TODO: Add GPU metrics"
    }
