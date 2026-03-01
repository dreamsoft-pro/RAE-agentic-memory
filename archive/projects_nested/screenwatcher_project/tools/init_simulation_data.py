import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.registry.models import Factory, Department, Line, Machine

def init_data():
    print("Initializing simulation data...")
    
    # Factory
    factory, created = Factory.objects.get_or_create(
        code="FACTORY-01",
        defaults={"name": "Main Factory", "address": "123 Ind. Blvd"}
    )
    if created: print(f"Created Factory: {factory}")

    # Shifts
    from apps.registry.models import Shift
    from datetime import time
    
    shifts_data = [
        ("Morning", time(6, 0), time(14, 0)),
        ("Afternoon", time(14, 0), time(22, 0)),
        ("Night", time(22, 0), time(6, 0))
    ]
    
    for name, start, end in shifts_data:
        Shift.objects.get_or_create(
            factory=factory,
            name=name,
            defaults={"start_time": start, "end_time": end}
        )
        print(f"Ensured Shift: {name}")

    # Department
    dept, created = Department.objects.get_or_create(
        factory=factory,
        code="DEPT-01",
        defaults={"name": "Assembly Dept"}
    )
    if created: print(f"Created Department: {dept}")

    # Line
    line, created = Line.objects.get_or_create(
        department=dept,
        code="LINE-01",
        defaults={"name": "Assembly Line 1"}
    )
    if created: print(f"Created Line: {line}")

    # Machine
    machine, created = Machine.objects.update_or_create(
        code="TM01",
        defaults={
            "line": line,
            "name": "Test Machine 01",
            "description": "Simulation Target",
            "cycle_time_ideal": 30.0,
            "is_active": True
        }
    )
    if created: 
        print(f"Created Machine: {machine}")
    else:
        print(f"Machine {machine} already exists.")

    # User & Token
    from django.contrib.auth.models import User
    from rest_framework.authtoken.models import Token
    
    user, created = User.objects.get_or_create(username='simulator')
    user.set_password('simulator123')
    user.save()
    if created:
        print("Created user 'simulator'")
    else:
        print("Updated user 'simulator'")
    
    token, created = Token.objects.get_or_create(user=user)
    print(f"TOKEN: {token.key}")

    # Casbin Role
    from apps.rbac.services import EnforcerService
    EnforcerService.add_role_for_user('simulator', 'role:operator')
    print("Assigned role:operator to simulator")

if __name__ == "__main__":
    init_data()
