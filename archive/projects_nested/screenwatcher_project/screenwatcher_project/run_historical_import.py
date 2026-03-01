import os
import sys
import django
from django.utils import timezone
from django.core.files import File

# Setup Django
# Root is one level up from this script (in /home/print/cloud)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from apps.registry.models import Machine, Factory, Department, Line
from apps.collector.models import DataImport
from apps.collector.services.ingestion import DataIngestionService

def run_import():
    print("--- STARTING HISTORICAL DATA IMPORT ---")
    
    # 1. Ensure Machine M01 exists (for JSONL data)
    factory, _ = Factory.objects.get_or_create(code='FAC-01', defaults={'name': 'Main Factory'})
    dept, _ = Department.objects.get_or_create(code='DEPT-01', factory=factory, defaults={'name': 'Assembly Dept'})
    line, _ = Line.objects.get_or_create(code='LINE-01', department=dept, defaults={'name': 'Assembly Line 1'})
    
    machine_m01, created = Machine.objects.get_or_create(
        code='M01', 
        defaults={'name': 'TrueJet M01', 'is_active': True, 'line': line}
    )
    if created: print("Created Machine M01")

    # 2. Files to import
    files = [
        ('/app/docs/offline_data_19-01-2026.jsonl', DataImport.ImportType.SCREENWATCHER_JSONL),
        ('/app/docs/data-for-charts/_2026_01_21_offline_data.jsonl', DataImport.ImportType.SCREENWATCHER_JSONL),
        ('/app/docs/data-for-charts/_2026_01_22-10-47-33offline_data.jsonl', DataImport.ImportType.SCREENWATCHER_JSONL),
    ]

    for file_path, import_type in files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        print(f"Importing {file_path}...")
        
        with open(file_path, 'rb') as f:
            di = DataImport.objects.create(
                machine=machine_m01,
                import_type=import_type,
                status=DataImport.Status.PENDING
            )
            di.import_file.save(os.path.basename(file_path), File(f))
            
            # Process immediately
            DataIngestionService.process_import(di)
            print(f"Finished {file_path}. Status: {di.status}")
            if di.status == DataImport.Status.FAILED:
                print(f"Error Log: {di.log}")

    print("--- IMPORT COMPLETE ---")

if __name__ == "__main__":
    run_import()