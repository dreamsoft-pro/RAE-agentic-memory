
import os
import django
import sys
import re
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()
from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

def extract_m2h(speed_raw):
    if speed_raw is None: return None
    if isinstance(speed_raw, (int, float)): return float(speed_raw)
    if not isinstance(speed_raw, str): return None
    m = re.search(r'\(([-+]?\d+(?:\.\d+)?)', speed_raw)
    if m: return float(m.group(1))
    m = re.search(r'[-+]?\d*\.\d+|\d+', speed_raw.replace(',', '.'))
    if m: return float(m.group(0))
    return None

m = Machine.objects.filter(code__icontains='TJ').first()
pts = TelemetryPoint.objects.filter(machine=m, timestamp__startswith='2026-01-09')

count = 0
for p in pts:
    val = extract_m2h(p.payload.get('Speed'))
    if val and val > 0:
        print(f'SPEED FOUND: {val} at {p.timestamp} Payload: {p.payload}')
        count += 1
        if count > 5: break
if count == 0: print('NO POSITIVE SPEED FOUND')

