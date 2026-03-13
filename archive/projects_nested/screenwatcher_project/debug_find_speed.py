
import os
import django
import sys
import json
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()
from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

m = Machine.objects.filter(code__icontains='TJ').first()
pts = TelemetryPoint.objects.filter(machine=m, timestamp__startswith='2026-01-09')

for p in pts:
    s = json.dumps(p.payload)
    if 'Speed' in s or 'speed' in s:
        print(f'FOUND SPEED: {p.payload}')
        break
else:
    print('NO SPEED FOUND')

