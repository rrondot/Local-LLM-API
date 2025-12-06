Install requirements:
pip install -r requirements.txt

Install Ollama on your system and a model of your choice,
We used llama3.1:8b on this test
To launch ollama use:
ollama serve

to launch FastAPI use:

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Test the llm with the API using test.py
Display Token usage, latency of generation and token per sec + memory usage with benchmark.py
Generate a report with generate_report.py