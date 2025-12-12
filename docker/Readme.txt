Build the container
docker build -t llm-api:v1 .

Try different models:

docker run --gpus all -p 8000:8000 \
  -e MODEL_NAME="TinyLlama/TinyLlama-1.1B-Chat-v1.0" \
  llm-api:v1

Or try OPT-125M (faster but lower quality)

docker run --gpus all -p 8000:8000 \
  -e MODEL_NAME="facebook/opt-125m" \
  llm-api:v1

  Test the api
  curl http://localhost:8000/health

  Generate text
  curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain baseball in one sentence",
    "max_tokens": 50
  }'