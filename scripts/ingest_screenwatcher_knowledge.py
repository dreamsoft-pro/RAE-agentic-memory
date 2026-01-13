import requests
import json
import time

API_URL = "http://100.66.252.117:8000/v1/memory"
HEADERS = {
    "Content-Type": "application/json", 
    "X-Tenant-Id": "screenwatcher"
}
PROJECT = "screenwatcher_project"

# Wiedza wydobyta z analizy plików i konfiguracji
KNOWLEDGE_BASE = [
    {
        "content": "ScreenWatcher is a comprehensive screen monitoring system featuring a Django-based backend and a Celery-powered asynchronous task queue for processing video/image data.",
        "tags": ["architecture", "django", "backend"],
        "layer": "semantic",
        "importance": 0.9
    },
    {
        "content": "The ScreenWatcher Dashboard (v4 Professional) provides a visual builder for configuring monitoring widgets and viewing real-time streams.",
        "tags": ["frontend", "dashboard", "ui"],
        "layer": "semantic",
        "importance": 0.8
    },
    {
        "content": "ScreenWatcher Edge Client includes an MVP ROI (Region of Interest) configurator, allowing users to define specific screen areas for targeted monitoring.",
        "tags": ["edge-computing", "feature", "roi"],
        "layer": "semantic",
        "importance": 0.85
    },
    {
        "content": "Infrastructure: ScreenWatcher shares the RAE Cluster nodes (Node1, Node2) for heavy computation and utilizes a dedicated Redis instance for task brokering.",
        "tags": ["infrastructure", "cluster", "deployment"],
        "layer": "semantic",
        "importance": 0.7
    },
    {
        "content": "Database Schema: ScreenWatcher uses PostgreSQL for structured data, including models for Dashboards, Widgets, and User configurations.",
        "tags": ["database", "postgres", "schema"],
        "layer": "semantic",
        "importance": 0.75
    }
]

def ingest_knowledge():
    print(f"🧠 Ingesting {len(KNOWLEDGE_BASE)} knowledge items about {PROJECT}...")
    
    for item in KNOWLEDGE_BASE:
        payload = {
            "content": item["content"],
            "tags": item["tags"],
            "layer": item["layer"],
            "importance": item["importance"],
            "project": PROJECT
        }
        
        try:
            res = requests.post(f"{API_URL}/store", headers=HEADERS, json=payload)
            if res.status_code == 200:
                mem_id = res.json().get("memory_id")
                print(f"✅ Stored: {item['content'][:50]}... (ID: {mem_id})")
            else:
                print(f"❌ Failed: {res.text}")
        except Exception as e:
            print(f"⚠️ Error: {e}")
            
    print("\n🎉 Ingestion complete. Waiting for indexing...")
    time.sleep(2)

def verify_search():
    print("\n🔍 Verifying Search for 'screenwatcher dashboard'...")
    query = {
        "query_text": "screenwatcher dashboard roi",
        "k": 3,
        "project": PROJECT
    }
    
    try:
        res = requests.post(f"{API_URL}/query", headers=HEADERS, json=query)
        if res.status_code == 200:
            results = res.json().get("results", [])
            for r in results:
                print(f"  🔹 [{r['score']:.4f}] {r['content']}")
        else:
            print(f"❌ Search Failed: {res.text}")
    except Exception as e:
        print(f"⚠️ Search Error: {e}")

if __name__ == "__main__":
    ingest_knowledge()
    verify_search()
