import requests

OLLAMA_URL = "http://localhost:11434"

def generate(model: str, prompt: str, stream: bool = False):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, stream=stream)
    
    if not stream:
        r.raise_for_status()
        return r.json()
    

    def stream_generator():
        for line in r.iter_lines():
            if line:
                yield line.decode()
    
    return stream_generator()