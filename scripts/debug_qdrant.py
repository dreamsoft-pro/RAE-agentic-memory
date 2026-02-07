import requests
import random
import json

url = "http://localhost:6333/collections/memories/points?wait=true"
vector = [random.random() for _ in range(768)]

payload = {
    "points": [
        {
            "id": "5f4e4346-6f4e-4b4e-8b4e-4b4e4b4e4b4e",
            "vector": {
                "dense": vector
            },
            "payload": {"test": "true"}
        }
    ]
}

try:
    r = requests.put(url, json=payload)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(e)
