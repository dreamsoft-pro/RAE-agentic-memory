
import os
import django
import sys
import json
import re
from dateutil.parser import parse
from django.utils.timezone import make_aware, is_naive

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

def parse_pole_1(text):
    data = {}
    
    # 1. Speed Extraction
    # Format: "Speed: 297.82m?(193.77m)/h" -> speed=193.77, speed_instant=297.82
    try:
        # Primary Speed (in parens)
        m = re.search(r"\((\d+\.\d+)m\)/h", text)
        if m:
            data['speed'] = float(m.group(1))
        else:
            # Fallback for cutoff text
            m2 = re.search(r"(\d+\.\d+)m\)/h", text)
            if m2:
                data['speed'] = float(m2.group(1))

        # Instant Speed (before parens)
        m_inst = re.search(r"Speed:\s*(\d+\.\d+)", text)
        if m_inst:
            data['speed_instant'] = float(m_inst.group(1))
    except Exception as e:
        print(f"Regex Error (Speed): {e}")

    # 2. Area Extraction
    # Format: "Area: 256.7m?"
    try:
        m_area = re.search(r"Area:\s*(\d+\.\d+)", text)
        if m_area:
            data['area_m2'] = float(m_area.group(1))
    except Exception as e:
        print(f"Regex Error (Area): {e}")

    # 3. Length Extraction
    # Format: "Length: 114.51/167.02m"
    try:
        m_len = re.search(r"Length:\s*(\d+\.\d+)/(\d+\.\d+)", text)
        if m_len:
            data['length_current_m'] = float(m_len.group(1))
            data['length_total_m'] = float(m_len.group(2))
    except Exception as e:
        print(f"Regex Error (Length): {e}")

    # 4. Count Extraction
    # Format: "Count: 91.19/133.00"
    try:
        m_count = re.search(r"Count:\s*(\d+\.\d+)/(\d+\.\d+)", text)
        if m_count:
            data['count_current'] = float(m_count.group(1))
            data['count_total'] = float(m_count.group(2))
    except Exception as e:
        print(f"Regex Error (Count): {e}")

    # 5. Time Extraction
    # Format: "Time: 00:35:32"
    try:
        m_time = re.search(r"Time:\s*([\d:]+)", text)
        if m_time:
            data['run_time_str'] = m_time.group(1)
    except Exception as e:
        print(f"Regex Error (Time): {e}")

    # 6. Filename Extraction (Last line ending in .prn)
    try:
        lines = text.strip().split('\n')
        if lines and lines[-1].strip().endswith('.prn'):
            data['filename'] = lines[-1].strip()
    except Exception:
        pass

    return data

def import_and_parse():
    # ... (rest of the function remains similar, but mapping new fields)
    file_path = "docs/offline_data_19-01-2026.jsonl"
    machine_code = 'TJ02'
    machine = Machine.objects.filter(code=machine_code).first()
    if not machine:
        print(f"Machine {machine_code} not found")
        return

    print(f"Deleting existing points for {machine.code} on 2026-01-19...")
    TelemetryPoint.objects.filter(
        machine=machine,
        timestamp__date='2026-01-19'
    ).delete()
    
    points = []
    print("Reading from stdin...")
    
    last_known_state = {}

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            raw_data = json.loads(line)
            metrics = raw_data.get('metrics', {})
            pole_1 = metrics.get('pole_1', '')
            
            parsed = parse_pole_1(pole_1)
            
            # STATEFUL FILLING
            # 1. Update state with new valid values
            for k, v in parsed.items():
                if v is not None:
                    last_known_state[k] = v
            
            # 2. Backfill missing values from state
            # List of fields we want to persist
            persistent_fields = ['area_m2', 'length_current_m', 'length_total_m', 
                               'count_current', 'count_total', 'run_time_str', 'filename']
            
            full_metrics = parsed.copy()
            for k in persistent_fields:
                if k not in full_metrics and k in last_known_state:
                    full_metrics[k] = last_known_state[k]

            # Update metrics and raw_data with ALL fields (parsed + backfilled)
            for k, v in full_metrics.items():
                metrics[k] = v
                raw_data[k] = v # Top level for convenience
                
                # Special cases for legacy compatibility
                if k == 'area_m2':
                    metrics['Area'] = v
                    raw_data['Area'] = v
                if k == 'speed':
                    metrics['Speed'] = v
                    raw_data['Speed'] = v

            # Ensure Status
            status = metrics.get('status')
            if status:
                raw_data['status'] = status
            
            raw_data['metrics'] = metrics

            ts = parse(raw_data['timestamp'])
            if is_naive(ts): ts = make_aware(ts)

            p = TelemetryPoint(
                machine=machine,
                timestamp=ts,
                payload=raw_data
            )
            points.append(p)

        except Exception as e:
            print(f"Error line: {e}", file=sys.stderr)

    if points:
        TelemetryPoint.objects.bulk_create(points)
        print(f"Imported {len(points)} points with RICH parsed metrics (Stateful Fill).")
    else:
        print("No points imported.")

if __name__ == "__main__":
    import_and_parse()
