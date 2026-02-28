
import os
import django
import sys
import re

# In-container path is /app
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard, Widget
from apps.telemetry.models import TelemetryPoint
from datetime import datetime
from django.utils import timezone

def debug_production():
    machine_id = '224bf64a-d590-486f-8aee-9e4b5cedc198'
    start_time = timezone.make_aware(datetime(2026, 1, 9, 10, 0))
    end_time = timezone.make_aware(datetime(2026, 1, 9, 22, 0))

    print(f"DEBUG Machine: {machine_id}")
    print(f"DEBUG Range: {start_time} to {end_time}")

    points = TelemetryPoint.objects.filter(
        machine_id=machine_id,
        timestamp__range=(start_time, end_time)
    ).order_by('timestamp')

    print(f"DEBUG Points Found: {points.count()}")

    if points.count() == 0:
        print("!!! NO DATA IN RANGE !!!")
        # Check ANY data for this machine
        last = TelemetryPoint.objects.filter(machine_id=machine_id).order_by('-timestamp').first()
        if last:
            print(f"Latest data for this machine is at: {last.timestamp}")
        else:
            print("No data at all for this machine.")
        return

    # Helper from widget_data.py
    def table_to_dict(table):
        if not table or not isinstance(table, list): return {}
        rows = [r[0] for r in table if r and isinstance(r, list)]
        n = len(rows) // 2
        return dict(zip(rows[:n], rows[n:])) if n > 0 else {}

    def extract_m2h(speed_raw):
        if not speed_raw: return None
        if isinstance(speed_raw, (int, float)): return float(speed_raw)
        if not isinstance(speed_raw, str): return None
        m = re.search(r"\(([-+]?\d+(?:\.\d+)?)", speed_raw)
        if m: return float(m.group(1))
        m = re.search(r"[-+]?\d*\.\d+|\d+", speed_raw.replace(',', '.'))
        if m: return float(m.group(0))
        return None

    raw_data = []
    for p in points:
        metrics = p.payload.get('metrics', {})
        table = metrics.get('table', [])
        tbl_dict = table_to_dict(table)
        speed = extract_m2h(tbl_dict.get('Speed'))
        status = metrics.get('status') or p.payload.get('status')
        if speed is not None:
            raw_data.append({'ts': p.timestamp, 'speed': speed, 'status': status})

    print(f"DEBUG Points with Speed: {len(raw_data)}")
    
    # Check sample statuses
    statuses = set(str(d['status']).upper() for d in raw_data if d['status'])
    print(f"DEBUG Unique Statuses: {statuses}")

    valid = [d for d in raw_data if str(d['status']).upper() == 'RUNNING' and d['speed'] > 0]
    print(f"DEBUG Points after filter (RUNNING & >0): {len(valid)}")

    if valid:
        # Check first few speeds
        print(f"DEBUG Sample Speeds: {[d['speed'] for d in valid[:5]]}")

if __name__ == "__main__":
    debug_production()
