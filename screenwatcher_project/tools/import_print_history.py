import sys
import os
import struct
import django
from datetime import datetime
from django.utils.timezone import make_aware

# Setup Django
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.registry.models import Machine, Factory, Department, Line
from apps.telemetry.models import TelemetryPoint

# Constants
RECORD_SIZE = 392
FILE_PATH = 'docs/PrintHistory'
MACHINE_CODE = 'printer_01' 

def parse_record(chunk):
    # Parse Date (0-19)
    try:
        date_str = chunk[0:19].decode('utf-8')
        # Naive to Aware
        dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        timestamp = make_aware(dt)
    except Exception as e:
        return None

    # Parse Filename (20-?)
    # Find null terminator after offset 20
    try:
        filename_part = chunk[20:200]
        filename_bytes = filename_part.split(b'\x00')[0]
        filename = filename_bytes.decode('utf-8', errors='ignore')
    except:
        filename = "unknown"

    # Parse Doubles (Starting at 280)
    # Based on reverse engineering:
    # 280: FinishArea (confirmed)
    # 288: FinishCount
    # 296: PrintLength (confirmed)
    # 304: BigPoints (confirmed)
    # 312: MiddlePoints
    # 320: SmallPoints
    # 328: TotalCount
    try:
        doubles = struct.unpack('<ddddddd', chunk[280:336])
    except:
        return None

    return {
        'timestamp': timestamp,
        'filename': filename,
        'finish_area_m2': doubles[0],
        'print_length_m': doubles[2],
        'ink_big': doubles[3],
        'ink_middle': doubles[4],
        'ink_small': doubles[5],
        'total_count': doubles[6]
    }

def run():
    print(f"Importing from {FILE_PATH}...")
    
    # Ensure Hierarchy
    factory, _ = Factory.objects.get_or_create(code='FAC-01', defaults={'name': 'Main Factory'})
    dept, _ = Department.objects.get_or_create(code='DEPT-PRINT', factory=factory, defaults={'name': 'Printing Dept'})
    line, _ = Line.objects.get_or_create(code='LINE-PRINT-01', department=dept, defaults={'name': 'Print Line 1'})

    machine, _ = Machine.objects.get_or_create(
        code=MACHINE_CODE, 
        defaults={'name': 'Industrial Printer', 'is_active': True, 'line': line}
    )
    
    if not os.path.exists(FILE_PATH):
        print("File not found!")
        return

    with open(FILE_PATH, 'rb') as f:
        count = 0
        new_count = 0
        while True:
            chunk = f.read(RECORD_SIZE)
            if len(chunk) < RECORD_SIZE:
                break
            
            data = parse_record(chunk)
            if data:
                payload = {
                    'job_file': data['filename'],
                    'metrics': {
                        'area_m2': round(data['finish_area_m2'], 4),
                        'length_m': round(data['print_length_m'], 4),
                        'ink_drops': int(data['total_count']),
                        'ink_big': int(data['ink_big'])
                    }
                }
                
                # Check for duplication to allow re-runs
                obj, created = TelemetryPoint.objects.get_or_create(
                    machine=machine,
                    timestamp=data['timestamp'],
                    defaults={'payload': payload}
                )
                if created:
                    new_count += 1
                count += 1
                if count % 500 == 0:
                    print(f"Processed {count} records...")

    print(f"Done. Processed {count} records. Created {new_count} new points.")

if __name__ == '__main__':
    run()