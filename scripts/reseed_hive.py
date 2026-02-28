import requests
import json
import os

NODE1_API = "http://100.68.166.117:8001/v2/memories/"

def seed_doc(file_path, project="RAE-Hive"):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        return
    
    with open(file_path, "r") as f:
        content = f.read()
    
    payload = {
        "content": content,
        "layer": "semantic",
        "project": project,
        "tags": ["documentation", "bootstrapped"],
        "importance": 1.0
    }
    
    print(f"Seeding {file_path}...")
    response = requests.post(NODE1_API, json=payload)
    if response.status_code == 200:
        print(f"✅ Success: {file_path}")
    else:
        print(f"❌ Failed {file_path}: {response.status_code} - {response.text}")

docs = [
    "docs/plans/RAE-poprawa-determinizmu-1.txt",
    "docs/specs/RAE_BEHAVIORAL_ONTOLOGY.md",
    "STATUS.md",
    "docs/plans/RAE-poprawa-determinizmu-2.txt"
]

for doc in docs:
    seed_doc(doc)
