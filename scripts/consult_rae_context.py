import requests
import json

API_URL = "http://100.66.252.117:8000/v1/memory/query"
HEADERS = {"X-Tenant-Id": "screenwatcher", "Content-Type": "application/json"}

def ask_rae(question):
    print(f"\n🤖 Asking RAE: '{question}'")
    payload = {
        "query_text": question,
        "project": "screenwatcher_project",
        "k": 3
    }
    try:
        res = requests.post(API_URL, json=payload, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            data = res.json()
            results = data.get("results", [])
            if not results:
                print("  ⚠️ No results found.")
            for i, r in enumerate(results):
                # Display first 250 chars to verify context retrieval
                print(f"  🔹 [Context {i+1} | Score: {r['score']:.2f}] {r['content'][:250]}...")
        else:
            print(f"  ❌ Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"  ❌ Connection Error: {e}")

if __name__ == "__main__":
    # Pytanie 1: O zasady jakości i dryftu (Core Mandates)
    ask_rae("What are the agent rules regarding Zero Drift, quality, and migrations?")
    
    # Pytanie 2: O obecny status zadań (Context)
    ask_rae("What is the current status of Dashboard filters and Notification system?")

