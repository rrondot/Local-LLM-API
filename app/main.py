from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from ollama_client import generate

app = FastAPI(title="LLM API", description="FastAPI service for LLM inference via Ollama")

class ChatRequest(BaseModel):
    model: str = "llama3.1:8b"
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class ChatResponse(BaseModel):
    response: str
    model: str

@app.get("/health")
def health():
    ollama_url = os.getenv("OLLAMA_URL", "http://ollama-service:11434")
    try:
        r = requests.get(f"{ollama_url}/api/tags", timeout=5)
        ollama_status = "healthy" if r.status_code == 200 else "unhealthy"
    except:
        ollama_status = "unreachable"
    
    return {
        "status": "ok",
        "ollama_status": ollama_status,
        "ollama_url": ollama_url
    }

@app.get("/models")
def models():
    ollama_url = os.getenv("OLLAMA_URL", "http://ollama-service:11434")
    try:
        r = requests.get(f"{ollama_url}/api/tags", timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ollama service error: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        response = generate(req.model, req.prompt)
        if response and "response" in response:
            return ChatResponse(
                response=response["response"],
                model=req.model
            )
        else:
            raise HTTPException(status_code=500, detail="Invalid response format from Ollama")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")