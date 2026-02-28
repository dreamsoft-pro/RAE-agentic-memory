import os
import django
from uuid import uuid4

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.registry.models import Factory, Department, Line, Machine
from apps.dashboards.models import Dashboard
from django.contrib.auth.models import User

def init_data():
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        user = User.objects.create_superuser("admin", "admin@example.com", "admin")

    factory, _ = Factory.objects.get_or_create(name="Print&Display Factory")
    print(f"Factory: {factory.name}")

    dept, _ = Department.objects.get_or_create(name="Print&Display", factory=factory)
    print(f"Department: {dept.name}")

    line, _ = Line.objects.get_or_create(name="Dział druku wielkoformatowego", department=dept)
    print(f"Line: {line.name}")

    machine, created = Machine.objects.get_or_create(name="TrueJet2", line=line, defaults={"id": uuid4()})
    print(f"Machine: {machine.name} (Created: {created})")

    test_dash, _ = Dashboard.objects.get_or_create(name="Test Dashboard (Simulated)", defaults={"is_public": True, "is_default": True, "user": user})
    real_dash, _ = Dashboard.objects.get_or_create(name="Real Dashboard (Print&Display)", defaults={"is_public": True, "is_default": False, "user": user})
    print(f"Dashboards ensured: {test_dash.name}, {real_dash.name}")

if __name__ == "__main__":
    init_data()
