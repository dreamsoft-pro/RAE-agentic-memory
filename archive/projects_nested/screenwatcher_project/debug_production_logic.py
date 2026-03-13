import os
import django
import sys
import re
from datetime import timedelta

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine
from django.utils import timezone

from apps.dashboards.models import Dashboard, Widget

def debug_truejet_data():
    # 1. Find the machine via Dashboard
    dashboard_id = 'eb07f0f9-f65f-4298-a50d-fce6d00aebb0'
    try:
        dashboard = Dashboard.objects.get(id=dashboard_id)
        print(f"Found Dashboard: {dashboard.title} ({dashboard.id})")
        
        # Find a widget with machine_id
        widget = dashboard.widgets.filter(config__has_key='machine_id').first()
        if widget:
            machine_id = widget.config.get('machine_id')
            machine = Machine.objects.get(id=machine_id)
            print(f"Debugging Machine from Widget: {machine.name} ({machine.code}) ID: {machine.id}")
        else:
            print("No widget with machine_id found in this dashboard. Falling back to TJ search.")
            machine = Machine.objects.filter(code__icontains='TJ').first()
    except Exception as e:
        print(f"Dashboard lookup failed: {e}")
        machine = Machine.objects.filter(code__icontains='TJ').first()

    if not machine:
        print("No suitable machine found.")
        return

    # 2. Fetch Data (Last 24h or a specific known range if empty)
    # User said "offline_data.jsonl", usually this implies old data.
    # Let's look for ANY data first.
    last_point = TelemetryPoint.objects.filter(machine_id=machine.id).order_by('-timestamp').first()
    
    if not last_point:
        print("No telemetry points found for this machine.")
        return

    print(f"Latest point timestamp: {last_point.timestamp}")
    
    # Define range around the last point (e.g., 12 hours before)
    end_time = last_point.timestamp
    start_time = end_time - timedelta(hours=12)
    
    points = TelemetryPoint.objects.filter(
        machine_id=machine.id, 
        timestamp__range=(start_time, end_time)
    ).order_by('timestamp')
    
    count = points.count()
    print(f"Found {count} points in the last 12h ending at {end_time}")

    if count == 0:
        return

    # 3. Simulate Logic
    print("\n--- Simulating Extraction & Logic ---")
    
    def table_to_dict(table):
        if not table or not isinstance(table, list):
            return {}
        rows = [r[0] for r in table if r and isinstance(r, list)]
        n = len(rows) // 2
        return dict(zip(rows[:n], rows[n:])) if n > 0 else {}

    def extract_m2h(speed_raw):
        # Logic from widget_data.py
        if not speed_raw or not isinstance(speed_raw, str):
            return None
        # User provided regex: r"\(([-+]?\d+(?:\.\d+)?)"
        m = re.search(r"\(([-+]?\d+(?:\.\d+)?)", speed_raw)
        return float(m.group(1)) if m else None

    raw_data = []
    statuses_seen = set()
    
    for p in points[:50]: # Inspect first 50
        metrics = p.payload.get('metrics', {})
        table = metrics.get('table', [])
        tbl_dict = table_to_dict(table)
        
        # Check raw values
        raw_speed_table = tbl_dict.get('Speed')
        raw_speed_flat = p.payload.get('Speed')
        
        speed_val = extract_m2h(raw_speed_table)
        status = metrics.get('status') or p.payload.get('status')
        
        if status: statuses_seen.add(status)

        # Fallback check
        if speed_val is None:
             # Try simple parsing if the regex failed
             if isinstance(raw_speed_table, str):
                 # Maybe it's just a number string "123.5" without parens?
                 try:
                     speed_val = float(raw_speed_table)
                 except:
                     pass
        
        print(f"[{p.timestamp}] Status: {status} | Raw Table: '{raw_speed_table}' | Parsed: {speed_val}")

    print(f"\nUnique Statuses Found: {statuses_seen}")
    
    # 4. Run Full Algorithm on all points
    valid_data = []
    
    for p in points:
        metrics = p.payload.get('metrics', {})
        table = metrics.get('table', [])
        tbl_dict = table_to_dict(table)
        
        speed_val = extract_m2h(tbl_dict.get('Speed'))
        
        # Try fallback extraction if regex failed (maybe data format changed?)
        if speed_val is None:
             raw = tbl_dict.get('Speed')
             if isinstance(raw, str):
                 try:
                     # Try finding ANY float
                     m = re.search(r"[-+]?\d*\.\d+|\d+", raw)
                     if m:
                         speed_val = float(m.group(0))
                 except:
                     pass

        status = metrics.get('status') or p.payload.get('status')
        
        if speed_val is not None:
             valid_data.append({
                'ts': p.timestamp,
                'speed': speed_val,
                'status': status
            })

    # Filter
    # Check if 'RUNNING' is the correct case
    filtered_run = [d for d in valid_data if str(d['status']).upper() == 'RUNNING']
    filtered_run_pos = [d for d in filtered_run if d['speed'] > 0]
    
    print(f"\nTotal Points: {len(points)}")
    print(f"Points with Speed extracted: {len(valid_data)}")
    print(f"Points with Status=RUNNING (case-insensitive): {len(filtered_run)}")
    print(f"Points with Speed > 0: {len(filtered_run_pos)}")

    if not filtered_run_pos:
        print("!!! ZERO VALID POINTS FOR INTEGRATION !!!")
        return

    # Integration
    total_production = 0.0
    speeds = [d['speed'] for d in filtered_run_pos]
    
    # Simple integration without smoothing for baseline
    for i in range(len(filtered_run_pos) - 1):
        t1 = filtered_run_pos[i]['ts']
        t2 = filtered_run_pos[i+1]['ts']
        dt_hours = (t2 - t1).total_seconds() / 3600.0
        m2_inc = filtered_run_pos[i]['speed'] * dt_hours
        total_production += m2_inc
        
    print(f"\nBaseline Integration (No Filter/Smooth): {total_production:.2f} m2")

if __name__ == "__main__":
    debug_truejet_data()
