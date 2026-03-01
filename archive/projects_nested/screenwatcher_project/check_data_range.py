
import os
import django
import sys
from django.db.models import Min, Max, Count

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint

def check_range():
    try:
        m = Machine.objects.get(code='TJ02')
        print(f"Machine: {m.name} ({m.code})")
        
        agg = TelemetryPoint.objects.filter(machine=m).aggregate(
            min_ts=Min('timestamp'),
            max_ts=Max('timestamp'),
            count=Count('id')
        )
        
        # Count needs to be imported or done differently if aggregate fails
        count = TelemetryPoint.objects.filter(machine=m).count()

        print(f"Total Points: {count}")
        if agg['min_ts']:
            print(f"Start: {agg['min_ts']}")
            print(f"End:   {agg['max_ts']}")
        else:
            print("No data found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_range()
