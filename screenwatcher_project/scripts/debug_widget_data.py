
import os
import sys
import django
from datetime import datetime
from pathlib import Path

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine
from apps.dashboards.models import Widget

def check():
    print("--- DIAGNOSTICS ---")
    
    # 1. Check Machine
    machine = Machine.objects.filter(name__icontains="TrueJet2").first()
    if not machine:
        print("Machine not found!")
        return
    print(f"Machine: {machine.name} ID: {machine.id}")

    # 2. Check Points count
    count = TelemetryPoint.objects.filter(machine=machine).count()
    print(f"Total Points: {count}")
    
    # 3. Check Range
    first = TelemetryPoint.objects.filter(machine=machine).order_by('timestamp').first()
    last = TelemetryPoint.objects.filter(machine=machine).order_by('-timestamp').first()
    if first:
        print(f"Range: {first.timestamp} <-> {last.timestamp}")
    else:
        print("No points found in range.")

    # 4. Check specific metric data (payload)
    sample = TelemetryPoint.objects.filter(machine=machine, kind='machine_log').last()
    if sample:
        print(f"Sample Log Payload: {sample.payload}")
    
    sample_job = TelemetryPoint.objects.filter(machine=machine, kind='job_finished').last()
    if sample_job:
        print(f"Sample Job Payload: {sample_job.payload}")

    # 5. Check Widget Configuration
    widget = Widget.objects.filter(title__contains="Wydajność Maszyny").last()
    if widget:
        print(f"Widget Found: {widget.title} (Type: {widget.widget_type})")
        print(f"Config: {widget.config}")
        print(f"Series Count: {widget.series.count()}")
        for s in widget.series.all():
            print(f" - Series: {s.label} Metric: {s.metric.code} JSON Key: {s.metric.json_key}")

if __name__ == "__main__":
    check()
