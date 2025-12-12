from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
import time
import os
import logging
import torch

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

MODEL_NAME = os.getenv("MODEL_NAME", "facebook/opt-125m")

logger.info(f"Loading model: {MODEL_NAME}")
try:
    llm = LLM(
        model=MODEL_NAME,
        max_model_len=2048,
        gpu_memory_utilization=0.9,
        download_dir="/tmp/models",
        dtype="float16", 
        trust_remote_code=True
    )
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise


class ChatRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    tokens_generated: int
    latency_ms: float
    model: str

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "gpu_available": True
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Generate text completion"""
    start = time.time()
    
    try:
        sampling_params = SamplingParams(
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        outputs = llm.generate([request.prompt], sampling_params)
        
        latency = (time.time() - start) * 1000
        
        return ChatResponse(
            response=outputs[0].outputs[0].text,
            tokens_generated=len(outputs[0].outputs[0].token_ids),
            latency_ms=round(latency, 2),
            model=MODEL_NAME
        )
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    """Basic metrics for monitoring"""
    return {
        "model": MODEL_NAME,
        "status": "running"
    }
