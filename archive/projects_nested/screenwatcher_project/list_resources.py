import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.dashboards.models import Dashboard
from apps.registry.models import Machine

def list_resources():
    print("--- Dashboards ---")
    for d in Dashboard.objects.all():
        print(f"ID: {d.id} | Title: {d.title}")
    
    print("\n--- Machines ---")
    for m in Machine.objects.all():
        print(f"ID: {m.id} | Name: {m.name} | Code: {m.code}")

if __name__ == "__main__":
    list_resources()
