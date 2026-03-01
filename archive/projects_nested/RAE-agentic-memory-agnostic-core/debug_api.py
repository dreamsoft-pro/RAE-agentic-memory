import requests
import json

url = "http://localhost:8001/v2/memories/"
payload = {
    "content": "Test memory for diagnostic purposes",
    "project": "rae-core",
    "source": "diagnostic-script",
    "importance": 1.0,
    "layer": "reflective",
    "tags": ["test"]
}

headers = {
    "Content-Type": "application/json",
    "X-Tenant-ID": "00000000-0000-0000-0000-000000000000"
}

response = requests.post(url, json=payload, headers=headers)
print(f"Status Code: {response.status_code}")
try:
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except:
    print(f"Raw Response: {response.text}")
