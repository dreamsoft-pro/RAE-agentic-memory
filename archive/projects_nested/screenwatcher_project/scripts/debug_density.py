import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.telemetry.models import TelemetryPoint
from apps.registry.models import Machine

def analyze():
    print("--- DENSITY ANALYSIS ---")
    machine = Machine.objects.filter(name__icontains="TrueJet2").first()
    
    # 1. Total Range
    qs = TelemetryPoint.objects.filter(machine=machine, kind='machine_log')
    total = qs.count()
    if total == 0:
        print("No logs found.")
        return

    first = qs.order_by('timestamp').first().timestamp
    last = qs.order_by('-timestamp').first().timestamp
    print(f"Total Logs: {total}")
    print(f"Global Range: {first} -> {last}")

    # 2. Configured Range Analysis (19.01 14:00 - 20.01 04:00)
    # Be careful with TZ. Script used naive strings in config, but Django uses TZ.
    # Assuming UTC in DB.
    # 19.01 14:00 UTC
    start_dt = first.replace(hour=14, minute=0, second=0, microsecond=0)
    end_dt = start_dt + timedelta(hours=14) # Until 04:00 next day
    
    in_range = qs.filter(timestamp__range=(start_dt, end_dt))
    count_in_range = in_range.count()
    print(f"\nIn Target Range ({start_dt} - {end_dt}): {count_in_range} points")
    
    # 3. Value Distribution
    # Check how many have clean_speed > 0
    positive_speed = in_range.filter(payload__clean_speed__gt=0).count()
    print(f"Points with Speed > 0: {positive_speed}")
    
    # Check Area parsing potential
    # Sample text
    sample = in_range.filter(payload__ocr_text__contains="Area:").first()
    if sample:
        print(f"Sample OCR: {repr(sample.payload.get('ocr_text'))}")
    else:
        print("No 'Area:' found in OCR text.")

    # 4. Check Gaps
    # Iterate and find largest gaps
    points = list(in_range.order_by('timestamp').values_list('timestamp', flat=True))
    if len(points) > 1:
        gaps = []
        for i in range(1, len(points)):
            diff = (points[i] - points[i-1]).total_seconds()
            if diff > 60: # Gap > 1 min
                gaps.append((points[i-1], points[i], diff))
        
        gaps.sort(key=lambda x: x[2], reverse=True)
        print(f"\nTop 5 Gaps (>60s):")
        for g in gaps[:5]:
            print(f"  {g[0]} -> {g[1]} ({int(g[2])}s)")
    
if __name__ == "__main__":
    analyze()
