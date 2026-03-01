
import os
import sys
import django
sys.path.append('/app')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()
from apps.dashboards.models import Widget

def update():
    w = Widget.objects.filter(title__contains="Wydajność Maszyny").last()
    if w:
        print(f"Updating Widget {w.id} config...")
        w.config['date_to'] = "2026-01-22T00:00:00"
        # Ensure connectNulls is boolean
        w.config['connectNulls'] = False
        w.save()
        print("Updated.")

if __name__ == "__main__":
    update()
