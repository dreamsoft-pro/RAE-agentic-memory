import random
import time
import json
from datetime import datetime
import urllib.request
import urllib.error

API_URL = "http://100.66.252.117:9000/api/collector/ingest/"
MACHINE_CODE = "TM01"
TOKEN = "3a1fcceca964deaeae60c32f9024a685bdc7f9c1"

def simulate_agent():
    print(f"Starting Agent OCR Simulator for {MACHINE_CODE}...")
    
    while True:
        try:
            # Simulate OCR noise and results
            current_status = "RUNNING" if random.random() < 0.9 else "PAUSED"
            temp = round(random.uniform(70.0, 85.0), 1)
            
            payload = {
                "machine_code": MACHINE_CODE,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "metrics": {
                    "status": current_status,
                    "temperature": temp,
                    "counter": random.randint(1000, 2000),
                    "operator_id": "OP_123"
                },
                "metadata": {
                    "status": {"name": "Machine Status", "type": "status", "category": "Core"},
                    "temperature": {"name": "Ambient Temp", "unit": "°C", "type": "number", "category": "Environment"},
                    "counter": {"name": "Total Parts", "unit": "pcs", "type": "number", "category": "Production"},
                    "operator_id": {"name": "Active Operator", "type": "text", "category": "Staff"}
                }
            }
            
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(API_URL, data=data, headers={
                "Authorization": f"Token {TOKEN}",
                "Content-Type": "application/json"
            })
            
            try:
                with urllib.request.urlopen(req) as response:
                    if response.getcode() == 201:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Agent Data Sent | Status: {current_status} | Temp: {temp}")
                    else:
                        print(f"Error: {response.getcode()}")
            except urllib.error.URLError as e:
                print(f"Connection Error: {e}")

        except KeyboardInterrupt:
            print("Stopping agent simulator...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            
        time.sleep(5)

if __name__ == "__main__":
    simulate_agent()
