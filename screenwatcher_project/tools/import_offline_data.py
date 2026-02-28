import json
import os
import django
import sys
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint
from apps.oee.services import OEECalculator, DowntimeManager

def import_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    print(f"Starting import from {file_path}...")
    success_count = 0
    error_count = 0

    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line)
                machine_code = data.get('machine_code')
                machine = Machine.objects.get(code=machine_code)
                
                # Create Telemetry Point
                tp = TelemetryPoint.objects.create(
                    machine=machine,
                    timestamp=data.get('timestamp'),
                    kind='telemetry_packet',
                    payload=data.get('metrics')
                )
                
                # Trigger OEE and Downtime logic
                OEECalculator.calculate_daily(machine, tp.timestamp.date())
                
                status_val = data.get('metrics', {}).get('status')
                if status_val:
                    DowntimeManager.process_status_change(machine, str(status_val), tp.timestamp)
                
                success_count += 1
                if success_count % 10 == 0:
                    print(f"Imported {success_count} points...")
                    
            except Exception as e:
                print(f"Error importing line: {e}")
                error_count += 1

    print(f"Import finished! Success: {success_count}, Errors: {error_count}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_offline_data.py <path_to_jsonl_file>")
    else:
        import_data(sys.argv[1])
