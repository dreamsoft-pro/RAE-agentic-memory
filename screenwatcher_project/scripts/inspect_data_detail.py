
import os
import sys
import django
from datetime import datetime
import json

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

def inspect():
    print("--- DEEP INSPECTION ---")
    machine = Machine.objects.filter(name__icontains="TrueJet2").first()
    if not machine:
        print("Machine not found")
        return

    # 1. Check Jobs (CSV Data)
    print("\n[JOBS - CSV Data]")
    jobs = TelemetryPoint.objects.filter(machine=machine, kind='job_finished').order_by('-timestamp')[:5]
    if not jobs.exists():
        print("NO JOBS FOUND!")
    for j in jobs:
        print(f"TS: {j.timestamp} | Payload: {json.dumps(j.payload)}")

    # 2. Check Logs (Machine Data)
    print("\n[LOGS - Machine Data]")
    logs = TelemetryPoint.objects.filter(machine=machine, kind='machine_log', payload__clean_speed__gt=0).order_by('-timestamp')[:5]
    if not logs.exists():
        print("NO LOGS WITH SPEED > 0 FOUND! Checking zeros...")
        logs = TelemetryPoint.objects.filter(machine=machine, kind='machine_log').order_by('-timestamp')[:5]
    
    for l in logs:
        print(f"TS: {l.timestamp} | Payload: {json.dumps(l.payload)}")

if __name__ == "__main__":
    inspect()
