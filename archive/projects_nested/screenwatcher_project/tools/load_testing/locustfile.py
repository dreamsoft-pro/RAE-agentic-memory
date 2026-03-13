from locust import HttpUser, task, between
import random
import json
import datetime

class MachineSimulator(HttpUser):
    wait_time = between(1, 5)  # Simulate 1-5 seconds between events

    def on_start(self):
        # Setup: Authenticate or register machine
        # For simplicity, assuming existing machine codes M-001 to M-010
        self.machine_code = f"M-{random.randint(1, 10):03d}"
        self.token = "Token 12345" # Placeholder, real test would get token

    @task
    def send_telemetry(self):
        payload = {
            "machine_code": self.machine_code,
            "timestamp": datetime.datetime.now().isoformat(),
            "metrics": {
                "temperature": random.uniform(20.0, 90.0),
                "vibration": random.uniform(0.1, 5.0),
                "status": random.choice(["RUNNING", "RUNNING", "RUNNING", "STOPPED"]),
                "production_count": random.randint(100, 500)
            }
        }
        
        # In a real scenario, use correct Authorization header
        # headers = {"Authorization": self.token}
        
        self.client.post("/api/collector/ingest/", json=payload)
