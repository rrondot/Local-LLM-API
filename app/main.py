from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from .ollama_client import generate

app = FastAPI()

class ChatRequest(BaseModel):
    model: str = "llama3.1:8b"
    prompt: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/models")
def models():
    r = requests.get("http://localhost:11434/api/tags")
    return r.json()

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        response = generate(req.model, req.prompt)
        if response and "response" in response:
            return {"response": response["response"]}
        else:
            raise HTTPException(status_code=500, detail=f"Unexpected response format: {response}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Ollama service error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")