import httpx
import json

API_URL = "http://localhost:8001/v2/memories/"
HEADERS = {"X-API-Key": "test-key", "X-Tenant-Id": "00000000-0000-0000-0000-000000000000"}

def test_error_audit_flow():
    print("🚀 Triggering intentional Contract Violation...")
    
    # Payload that violates L1 (analysis too short)
    bad_data = {
        "content": "Too short", # This will fail AgentOutputContract validation
        "layer": "working",
        "source": "error_test",
        "tags": ["agent_decision"]
    }
    
    try:
        resp = httpx.post(API_URL, json=bad_data, headers=HEADERS, timeout=10.0)
        print(f"Status Code: {resp.status_code}")
        print(f"Response: {json.dumps(resp.json(), indent=2)}")
        
        if resp.status_code == 422:
            print("✅ SUCCESS: API correctly handled the RAE domain error.")
        else:
            print("❌ FAILURE: Unexpected status code.")
            
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_error_audit_flow()
