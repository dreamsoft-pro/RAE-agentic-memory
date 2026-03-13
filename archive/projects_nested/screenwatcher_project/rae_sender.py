import http.client
import json

def send_to_rae():
    conn = http.client.HTTPConnection("localhost", 8001)
    payload = {
        "project": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11_project",
        "layer": "episodic",
        "tag": "session_sync",
        "content": "TRIAL: Integration check from Screenwatcher to RAE API (Port 8001) to RAE via Tailscale. Current State: Iterations 1-9 completed. Missing: Gantt Chart. Mandate established: RAE usage is critical for drift prevention."
    }
    headers = {
        'X-Tenant-Id': 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
        'Content-Type': 'application/json'
    }
    try:
        conn.request("POST", "/v1/memory/store", json.dumps(payload), headers)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    send_to_rae()
