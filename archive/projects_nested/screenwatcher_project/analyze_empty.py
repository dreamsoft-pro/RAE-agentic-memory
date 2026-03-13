
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

def analyze_empty_records():
    machine_id = '224bf64a-d590-486f-8aee-9e4b5cedc198' # TJ02
    start_time = timezone.make_aware(datetime(2026, 1, 9, 10, 0))
    end_time = timezone.make_aware(datetime(2026, 1, 16, 15, 0))

    points = TelemetryPoint.objects.filter(
        machine_id=machine_id,
        timestamp__range=(start_time, end_time)
    )

    total_count = points.count()
    print(f"Analiza okresu: {start_time} - {end_time}")
    print(f"Suma wszystkich rekordów: {total_count}")

    # Definicje "pustych" rekordów
    missing_speed = 0
    zero_speed = 0
    not_running = 0
    empty_area_field = 0 # Pole payload["Area"] == ""

    def get_speed(p):
        payload = p.payload
        val = payload.get('Speed')
        if val is None:
            val = payload.get('metrics', {}).get('table', [])
            # Skip full table to dict for speed
        return val

    for p in points:
        payload = p.payload
        
        # 1. Sprawdzanie statusu
        status = str(payload.get('status') or payload.get('metrics', {}).get('status') or "").upper()
        if status != 'RUNNING':
            not_running += 1

        # 2. Sprawdzanie pola Area (częsty objaw w Twoim OCR)
        area = payload.get('Area')
        if area == "":
            empty_area_field += 1

        # 3. Sprawdzanie prędkości
        # Szybka ekstrakcja
        speed_raw = payload.get('Speed')
        if speed_raw is None:
             # Look in metrics.table - very simplified check
             metrics = payload.get('metrics', {})
             if not metrics.get('table'):
                 missing_speed += 1
             else:
                 # If table exists but no Speed found later
                 pass
        else:
            try:
                if float(speed_raw) == 0:
                    zero_speed += 1
            except: pass

    print("-" * 30)
    print(f"Rekordy ze statusem innym niż RUNNING: {not_running} ({not_running/total_count*100:.1f}%)")
    print(f"Rekordy z pustością w polu 'Area':     {empty_area_field} ({empty_area_field/total_count*100:.1f}%)")
    print(f"Rekordy z brakiem/zerową prędkością:    {missing_speed + zero_speed} ({(missing_speed+zero_speed)/total_count*100:.1f}%)")

if __name__ == "__main__":
    analyze_empty_records()
