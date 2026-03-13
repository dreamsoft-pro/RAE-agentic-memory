import os
import django
from django.conf import settings
from datetime import datetime, timedelta
import sys
import re

# Setup Django
sys.path.append('/home/grzegorz-lesniowski/cloud/screenwatcher_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint
from django.utils import timezone

def analyze():
    # Find machine
    try:
        machine = Machine.objects.filter(code__icontains='TJ').first()
        if not machine:
            print('No TrueJet machine found')
            return
        
        print(f'Machine: {machine.code} ({machine.id})')
        
        # Time range: Jan 9 2026, 10:00 - 23:33
        start_date = datetime(2026, 1, 9, 10, 0, 0)
        end_date = datetime(2026, 1, 9, 23, 33, 0)
        
        # Make timezone aware if settings use TZ
        if settings.USE_TZ:
            start_date = timezone.make_aware(start_date)
            end_date = timezone.make_aware(end_date)
            
        print(f'Querying range: {start_date} to {end_date}')
        
        points = TelemetryPoint.objects.filter(
            machine=machine,
            timestamp__range=(start_date, end_date)
        ).order_by('timestamp')
        
        count = points.count()
        print(f'Found {count} points')
        
        if count == 0:
            return

        # Sample data
        print('
--- SAMPLE DATA (First 5) ---')
        for p in points[:5]:
            print(f'{p.timestamp}: {p.payload}')
            
        # Analyze values
        raw_speeds = []
        statuses = []
        
        for p in points:
            # Logic from ProductionTrendProvider
            payload = p.payload
            val = payload.get('Speed')
            status = payload.get('status')
            
            if not val:
                metrics = payload.get('metrics', {})
                table = metrics.get('table', [])
                if isinstance(table, list) and table:
                    rows = [r[0] for r in table if r]
                    n = len(rows)//2
                    if n > 0:
                        d = dict(zip(rows[:n], rows[n:]))
                        val = d.get('Speed')
                
                if not status:
                    status = metrics.get('status')
            
            raw_speeds.append(val)
            statuses.append(status)

        # Unique values
        print('
--- UNIQUE STATUSES ---')
        print(set(statuses))
        
        print('
--- SAMPLE RAW SPEEDS (Unique, First 20) ---')
        unique_speeds = list(set([str(s) for s in raw_speeds if s]))
        print(unique_speeds[:20])

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    analyze()
