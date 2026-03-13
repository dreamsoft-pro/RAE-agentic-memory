
import os
import django
import sys
import re
from datetime import datetime
from django.utils import timezone

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.telemetry.models import TelemetryPoint

def analyze_jan9():
    machine_id = '224bf64a-d590-486f-8aee-9e4b5cedc198' # TJ02
    
    # Range: Jan 9th 10:00 to 14:00 (Zooming in on the active printing time)
    start_time = timezone.make_aware(datetime(2026, 1, 9, 10, 0))
    end_time = timezone.make_aware(datetime(2026, 1, 9, 14, 0))

    points = TelemetryPoint.objects.filter(
        machine_id=machine_id,
        timestamp__range=(start_time, end_time)
    ).order_by('timestamp')

    print(f"Analyzing Jan 9th ({start_time.time()} - {end_time.time()})...")
    print(f"Total points: {points.count()}")

    def extract_speed(p):
        payload = p.payload
        # Helper to get speed from flat or nested
        val = payload.get('Speed')
        if not val:
            metrics = payload.get('metrics', {})
            table = metrics.get('table', [])
            # Table logic copy
            if isinstance(table, list):
                rows = [r[0] for r in table if r and isinstance(r, list)]
                n = len(rows) // 2
                tbl = dict(zip(rows[:n], rows[n:])) if n > 0 else {}
                val = tbl.get('Speed')
        
        if not val: return None
        
        # Parse
        if isinstance(val, (int, float)): return float(val)
        if isinstance(val, str):
            m = re.search(r"\(([-+]?\d+(?:\.\d+)?)", val)
            if m: return float(m.group(1))
            m = re.search(r"[-+]?\d*\.\d+|\d+", val.replace(',', '.'))
            if m: return float(m.group(0))
        return None

    valid_points = []
    for p in points:
        s = extract_speed(p)
        status = p.payload.get('status') or p.payload.get('metrics', {}).get('status')
        if s is not None and str(status).upper() == 'RUNNING':
            valid_points.append({'ts': p.timestamp, 'speed': s})

    print(f"Valid RUNNING points: {len(valid_points)}")
    
    # Filter for requested range 280-330
    target_range_points = [p for p in valid_points if 280 <= p['speed'] <= 330]
    print(f"Points in range 280-330 m2/h: {len(target_range_points)}")

    if not target_range_points:
        print("No points in that specific speed range found. Showing general stats:")
        target_range_points = valid_points[:20]

    print("\n--- DETAILED INCREMENTS (Sample) ---")
    print(f"{ 'Time':<12} | { 'Speed':<10} | { 'dt (sec)':<8} | { 'Inc (m2)':<10}")
    print("-" * 50)
    
    # Calculate increments for a sample of the target points
    # We need to find these points in the original timeline to get correct dt
    # So let's iterate the main valid_points list and only print if speed matches
    
    for i in range(len(valid_points) - 1):
        curr = valid_points[i]
        next_p = valid_points[i+1]
        
        # Only show if current speed is in target range (or close to it)
        if 280 <= curr['speed'] <= 330:
            dt = (next_p['ts'] - curr['ts']).total_seconds()
            
            # Skip if dt is huge (gap in data)
            if dt > 60: continue
            
            # Area = Speed (m2/h) * (dt / 3600)
            inc = curr['speed'] * (dt / 3600.0)
            
            print(f"{curr['ts'].strftime('%H:%M:%S') :<12} | {curr['speed']:<10.2f} | {dt:<8.2f} | {inc:<10.4f}")
            
            # Limit output
            if i > 200: # Scan a bit but don't print forever
                if i % 100 == 0: continue # Skip some
                if i > 1000: break

if __name__ == "__main__":
    analyze_jan9()
