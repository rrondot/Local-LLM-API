import requests

res = requests.post(
    "http://localhost:8000/chat",
    json={"prompt": "Hello there!"}
)

print(res.json())
