

target_path = "/home/grzegorz-lesniowski/cloud/screenwatcher_project/tools/simulator.py"

new_content = """import random
import time
import json
import os
import sys
from datetime import datetime
import urllib.request
import urllib.error

# CONFIGURATION
# Inside container, we talk to localhost on port 8000 (gunicorn/daphne)
API_URL = "http://127.0.0.1:8000/api/collector/ingest/"
MACHINE_CODE = "TM01"
# Hardcoded token from container DB
TOKEN = "3a1fcceca964deaeae60c32f9024a685bdc7f9c1"

def simulate():
    print(f"Starting machine simulator for {MACHINE_CODE}...")
    print(f"Target URL: {API_URL}")
    print(f"Using Token: {TOKEN[:5]}...{TOKEN[-5:]}")

    count = 0
    while True: # Run indefinitely until Ctrl+C
        count += 1
        try:
            # Simulate some metrics - tuned for DEMO visuals
            temp = round(random.uniform(50.0, 95.0), 2)

            # Status distribution for nice Gantt chart
            r = random.random()
            if r < 0.85: current_status = "RUNNING"
            elif r < 0.95: current_status = "IDLE"
            else: current_status = "STOPPED"

            payload = {
                "machine_code": MACHINE_CODE,
                "timestamp": datetime.now().isoformat(),
                "metrics": {
                    "temp": temp,
                    "speed": random.randint(500, 700) if current_status == "RUNNING" else 0,
                    "vibration": round(random.uniform(0.1, 0.8), 3),
                    "pressure": round(random.uniform(1.0, 5.0), 2),
                    "status": current_status,
                    "parts_delta": random.randint(0, 5) if current_status == "RUNNING" else 0,
                    "good_parts_delta": 0
                }
            }

            if payload["metrics"]["parts_delta"] > 0:
                is_bad = random.random() < 0.1
                total = payload["metrics"]["parts_delta"]
                good = total - 1 if is_bad else total
                payload["metrics"]["good_parts_delta"] = max(0, good)

            # print(f"[{datetime.now().strftime('%H:%M:%S')}] {current_status} | Temp: {temp}C | Prod: {payload['metrics']['parts_delta']}")

            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(API_URL, data=data, headers={
                "Authorization": f"Token {TOKEN}",
                "Content-Type": "application/json"
            })

            try:
                with urllib.request.urlopen(req) as response:
                    if response.getcode() == 201:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent OK | {current_status} | Temp: {temp}")
                    else:
                        print(f"Error: {response.getcode()}")
            except urllib.error.URLError as e:
                print(f"Connection Error: {e}")

        except KeyboardInterrupt:
            print("Stopping simulator...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

        time.sleep(2)

if __name__ == "__main__":
    simulate()
"""

with open(target_path, "w") as f:
    f.write(new_content)

print(f"Overwritten {target_path}")
