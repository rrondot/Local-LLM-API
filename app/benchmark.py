import time
import requests
import psutil

def benchmark(model="llama3.1", prompt="Hello, how are you?"):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    start = time.time()
    r = requests.post("http://localhost:11434/api/generate", json=payload).json()
    end = time.time()

    output = r["response"]
    tokens = len(output.split())
    latency = end - start
    tps = tokens / latency

    return {
        "tokens": tokens,
        "latency_sec": latency,
        "tokens_per_sec": tps
    }

if __name__ == "__main__":
    small = benchmark(prompt="Hello!")
    medium = benchmark(prompt="Explain to me the double play rule in baseball.")
    long = benchmark(prompt="Write a detailed summary of the life of Babe Ruth over 2000 words.")

    print("Small prompt:", small)
    print("Medium prompt:", medium)
    print("Large prompt:", long)

def get_memory():
    mem = psutil.virtual_memory()
    return {
        "total_gb": mem.total / 1e9,
        "used_gb": mem.used / 1e9,
        "percent": mem.percent
    }

result = get_memory()
print(result)