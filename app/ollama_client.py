import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://llm-api-ollama:11434")

def generate(model: str, prompt: str, stream: bool = False, timeout: int = 60):
    payload = {"model": model, "prompt": prompt, "stream": stream}
    
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        stream=stream,
        timeout=timeout
    )
    
    if not stream:
        r.raise_for_status()
        return r.json()
    
    def stream_generator():
        for line in r.iter_lines():
            if line:
                yield line.decode()
    
    return stream_generator()

def list_models():
    r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
    r.raise_for_status()
    return r.json()

def check_health():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return r.status_code == 200
    except:
        return False