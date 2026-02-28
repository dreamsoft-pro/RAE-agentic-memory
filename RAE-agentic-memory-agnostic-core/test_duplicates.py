import requests
import time

URL = "http://localhost:8001/v2/memories/"
TENANT = "00000000-0000-0000-0000-000000000000"

def test_duplicates():
    content = "CRITICAL FACT: The boiler temperature is 150 degrees. [DEDUP-TEST]"
    headers = {"X-Tenant-ID": TENANT, "Content-Type": "application/json"}
    
    print("🚀 Sending the same fact 3 times...")
    for i in range(3):
        resp = requests.post(URL, json={"content": content, "project": "dedup-test"}, headers=headers)
        print(f"   Request {i+1}: Status {resp.status_code}")
    
    time.sleep(1)
    
    print("\n🔍 Checking for duplicates in RAE...")
    query_resp = requests.post(f"{URL}query", json={"query": "boiler temperature DEDUP-TEST", "k": 10}, headers=headers)
    results = query_resp.json().get("results", [])
    
    # Count results with the same content
    matches = [r for r in results if "[DEDUP-TEST]" in r.get("content", "")]
    
    print(f"   Found {len(matches)} memories with the same content.")
    if len(matches) > 1:
        print("   ❌ FAIL: System is cluttered with duplicates!")
    else:
        print("   ✅ SUCCESS: System deduplicated the facts.")

if __name__ == "__main__":
    test_duplicates()