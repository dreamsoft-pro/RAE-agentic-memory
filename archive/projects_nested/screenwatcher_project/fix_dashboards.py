
import django
import os
import sys
import random
from django.utils import timezone
from datetime import timedelta

sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.dashboards.models import Dashboard, Widget
from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint

def fix_dashboards():
    # 1. Fix "Real Dashboard (Print&Display)"
    try:
        real_dashboard = Dashboard.objects.get(name="Real Dashboard (Print&Display)")
        truejet = Machine.objects.get(name="TrueJet2")
        
        print(f"Fixing Dashboard: {real_dashboard.name}")
        
        # Clear existing widgets to be safe (though it was empty)
        real_dashboard.widgets.all().delete()
        
        # Add Status Card
        Widget.objects.create(
            dashboard=real_dashboard,
            title=f"Status - {truejet.name}",
            widget_type="status_card",
            config={"machine_id": str(truejet.id)},
            pos_x=0, pos_y=0, width=4, height=2
        )
        
        # Add OEE Gauge
        Widget.objects.create(
            dashboard=real_dashboard,
            title=f"OEE - {truejet.name}",
            widget_type="oee_gauge",
            config={"machine_id": str(truejet.id)},
            pos_x=4, pos_y=0, width=4, height=4
        )
        
        # Add Production Trend
        Widget.objects.create(
            dashboard=real_dashboard,
            title=f"Production - {truejet.name}",
            widget_type="production_trend",
            config={"machine_id": str(truejet.id)},
            pos_x=0, pos_y=2, width=8, height=4
        )

        print("  -> Added 3 widgets for TrueJet2.")
        
        # Generate Sample Data for TrueJet2 if empty
        if TelemetryPoint.objects.filter(machine=truejet).count() == 0:
            print(f"  -> Generating sample telemetry for {truejet.name}...")
            now = timezone.now()
            points = []
            for i in range(60): # Last 60 minutes
                t = now - timedelta(minutes=i)
                payload = {
                    "status": "running" if random.random() > 0.1 else "idle",
                    "production_count": 1000 + (60-i)*10,
                    "speed": random.randint(80, 120),
                    "temperature": random.randint(50, 70)
                }
                points.append(TelemetryPoint(
                    machine=truejet,
                    timestamp=t,
                    kind="raw",
                    payload=payload
                ))
            TelemetryPoint.objects.bulk_create(points)
            print(f"  -> Created {len(points)} telemetry points.")

    except Dashboard.DoesNotExist:
        print("Dashboard 'Real Dashboard (Print&Display)' not found.")
    except Machine.DoesNotExist:
        print("Machine 'TrueJet2' not found.")

    # 2. Cleanup "Test Dashboard (Simulated)"
    try:
        test_dashboard = Dashboard.objects.get(name="Test Dashboard (Simulated)")
        if test_dashboard.widgets.count() == 0:
            print(f"Deleting empty dashboard: {test_dashboard.name}")
            test_dashboard.delete()
    except Dashboard.DoesNotExist:
        pass

if __name__ == "__main__":
    fix_dashboards()
