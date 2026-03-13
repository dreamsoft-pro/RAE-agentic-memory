
import os
import django
import sys
import json
from dateutil.parser import parse
from django.utils.timezone import make_aware, is_naive

# Setup Django environment
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

def import_data():
    file_path = "/host_mnt/offline_data_16_01_2025.jsonl" # Mapped path
    
    # 1. Find Machine
    try:
        # Try finding by code 'TJ02' first as seen before, or map 'Truejet2' to it
        machine = Machine.objects.filter(code='TJ02').first()
        if not machine:
             machine = Machine.objects.filter(name__icontains='TrueJet2').first()
        
        if not machine:
            print("Error: Machine TrueJet2 (TJ02) not found!")
            return

        print(f"Importing for Machine: {machine.name} ({machine.code}) ID: {machine.id}")

    except Exception as e:
        print(f"Error finding machine: {e}")
        return

    # 2. Read and Insert
    points = []
    count = 0
    
    # We need to access the file. Since we run in docker, we must mount the file or cat it.
    # Actually, the user path is on HOST. I cannot access it directly from container unless mounted.
    # STRATEGY: I will read the file in the Python script running in container by passing data via stdin 
    # OR (easier) I will assume I run this script via `docker exec -i ... < file`
    
    import sys
    # Read from stdin if file doesn't exist (streaming mode)
    # But wait, I am creating the script file first.
    
    # Alternative: I'll read the file from the path provided IF I can access it. 
    # Since I am "Gemini CLI" running on host, I can read the file.
    # But I need to insert into DB which is in Docker (MariaDB).
    # So I must run the script INSIDE the container.
    # The container CANNOT access /home/grzegorz... unless mounted.
    
    # SOLUTION: I will read the file on HOST using `cat`, pipe it to `docker exec -i ... python import_script.py`
    
    print("Reading from stdin...")
    for line in sys.stdin:
        if not line.strip(): continue
        try:
            data = json.loads(line)
            
            # Timestamp parsing
            ts_str = data.get('timestamp')
            if not ts_str: continue
            
            ts = parse(ts_str)
            if is_naive(ts):
                ts = make_aware(ts)

            # Create object
            p = TelemetryPoint(
                machine=machine,
                timestamp=ts,
                payload=data  # Store the whole JSON structure including 'metrics'
            )
            points.append(p)
            
            if len(points) >= 1000:
                TelemetryPoint.objects.bulk_create(points)
                count += len(points)
                points = []
                print(f"Imported {count} points...", file=sys.stderr)
                
        except Exception as e:
            print(f"Skipping bad line: {e}", file=sys.stderr)

    if points:
        TelemetryPoint.objects.bulk_create(points)
        count += len(points)
    
    print(f"DONE. Total imported: {count}")

if __name__ == "__main__":
    import_data()
