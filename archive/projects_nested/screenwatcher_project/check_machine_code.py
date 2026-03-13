
import os
import django
import sys

sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.registry.models import Machine

def check_machine():
    machine_id = '224bf64a-d590-486f-8aee-9e4b5cedc198'
    try:
        m = Machine.objects.get(id=machine_id)
        print(f"MACHINE: {m.name} | CODE: {m.code}")
    except:
        print("Machine not found")

if __name__ == "__main__":
    check_machine()
