
import os
import django
import sys
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()
from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

m = Machine.objects.filter(code__icontains='TJ').first()
pts = TelemetryPoint.objects.filter(machine=m, timestamp__startswith='2026-01-09 22:20').order_by('timestamp')

print('TS | Speed | Area')
for p in pts[:20]:
    print(f"{p.timestamp.strftime('%H:%M:%S')} | {p.payload.get('Speed')} | {p.payload.get('Area')}")

