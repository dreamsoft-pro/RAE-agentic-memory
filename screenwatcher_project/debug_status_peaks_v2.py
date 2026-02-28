import os
import django
import sys
import re
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()
from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

m = Machine.objects.filter(code__icontains='TJ').first()
points = TelemetryPoint.objects.filter(
    machine=m, 
    timestamp__range=('2026-01-09 10:00', '2026-01-09 23:33')
).order_by('timestamp')

def extract_m2h(speed_raw):
    if speed_raw is None: return None
    if isinstance(speed_raw, (int, float)): return float(speed_raw)
    if not isinstance(speed_raw, str): return None
    m = re.search(r'\(([-+]?\d+(?:\.\d+)?)', speed_raw)
    if m: return float(m.group(1))
    m = re.search(r'[-+]?\d*\.\d+|\d+', speed_raw.replace(',', '.'))
    if m: return float(m.group(0))
    return None

print('--- HIGH SPEED PEAKS (>450) ---')
peaks_count = 0
for p in points:
    raw_speed = p.payload.get('Speed')
    val = extract_m2h(raw_speed)
    status = p.payload.get('status')
    
    if val and val > 450:
        print(f'TS: {p.timestamp} | Speed: {val} (Raw: {raw_speed}) | Status: {status}')
        peaks_count += 1
        if peaks_count > 10: 
            print('... more peaks truncated ...')
            break

print('\n--- STATUS CHECK FOR NORMAL SPEED (250-350) ---')
count = 0
for p in points:
    raw_speed = p.payload.get('Speed')
    val = extract_m2h(raw_speed)
    status = p.payload.get('status')
    
    if val and 250 < val < 350:
        print(f'TS: {p.timestamp} | Speed: {val} | Status: {status}')
        count += 1
        if count > 20: break
