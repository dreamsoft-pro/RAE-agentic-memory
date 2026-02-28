
import os
import sys
import django
from django.db.models import Min, Max, Count, Avg

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.telemetry.models import TelemetryPoint
from apps.oee.models import ProductionJob
from apps.registry.models import Machine

def report():
    print("=== FINAL DATA REPORT ===")
    machine = Machine.objects.filter(name__icontains="TrueJet2").first()
    
    # 1. Logs (OCR Data)
    logs = TelemetryPoint.objects.filter(machine=machine, kind='machine_log')
    logs_count = logs.count()
    if logs_count > 0:
        r = logs.aggregate(Min('timestamp'), Max('timestamp'))
        print(f"\n[LOGS - OCR] Source: Screen Text Parsing")
        print(f"Count: {logs_count} points")
        print(f"Range: {r['timestamp__min']} -> {r['timestamp__max']}")
        
        # Check content sample
        sample = logs.filter(payload__clean_speed__gt=0).first()
        if sample:
            print(f"Sample Speed: {sample.payload.get('clean_speed')} m2/h (Parsed from: {repr(sample.payload.get('ocr_text')[:30])}...)")
    else:
        print("\n[LOGS] No data found.")

    # 2. Jobs (CSV Data)
    jobs = ProductionJob.objects.filter(machine=machine)
    jobs_count = jobs.count()
    if jobs_count > 0:
        r = jobs.aggregate(Min('timestamp'), Max('timestamp'), Avg('print_area'))
        print(f"\n[JOBS - CSV] Source: Digital Report File")
        print(f"Count: {jobs_count} jobs")
        print(f"Range: {r['timestamp__min']} -> {r['timestamp__max']}")
        print(f"Avg Area/Job: {r['print_area__avg']:.2f} m2")
    else:
        print("\n[JOBS] No data found.")

    # 3. Correlation
    print("\n[SUMMARY]")
    print("Wydajność Maszyny (Niebieska linia): Pochodzi z LOGÓW (OCR).")
    print("Oś Czasu (Gantt): Pochodzi z LOGÓW (OCR) - status wyliczany z prędkości.")
    print("Średnia Wydajność (KPI) / Lista Zadań: Pochodzi z CSV (Digital Report).")

if __name__ == "__main__":
    report()
