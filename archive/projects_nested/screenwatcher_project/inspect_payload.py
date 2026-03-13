
import os
import django
import sys
import json

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.telemetry.models import TelemetryPoint
from datetime import datetime
from django.utils import timezone

def inspect_payload():
    machine_id = '224bf64a-d590-486f-8aee-9e4b5cedc198'
    start_time = timezone.make_aware(datetime(2026, 1, 9, 10, 0))
    end_time = timezone.make_aware(datetime(2026, 1, 9, 22, 0))

    p = TelemetryPoint.objects.filter(
        machine_id=machine_id,
        timestamp__range=(start_time, end_time)
    ).first()

    if p:
        print(f"PAYLOAD for {p.timestamp}:")
        print(json.dumps(p.payload, indent=2))
    else:
        print("No point found.")

if __name__ == "__main__":
    inspect_payload()
