import os
import sys
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from apps.registry.models import Machine, Factory, Line
from casbin_adapter.enforcer import enforcer

def run():
    print("--- FIXING SIMULATOR ACCESS ---")

    # 1. User & Token
    user, created = User.objects.get_or_create(username='simulator')
    if created:
        user.set_password('simulator_password')
        user.save()
        print("User 'simulator' created.")
    else:
        print("User 'simulator' exists.")

    token, _ = Token.objects.get_or_create(user=user)
    print("API TOKEN START")
    print(token.key)
    print("API TOKEN END")

    # 2. Machine TM01
    machine = Machine.objects.filter(code='TM01').first()
    if machine:
        print("Machine TM01: EXISTS")
    else:
        print("Machine TM01: MISSING. Creating...")
        factory, _ = Factory.objects.get_or_create(name="Default Factory", slug="default-factory")
        line, _ = Line.objects.get_or_create(name="Default Line", slug="default-line", factory=factory)
        Machine.objects.create(code='TM01', name='Test Machine 01', line=line, is_active=True)
        print("Machine TM01: CREATED")

    # 3. Casbin Permissions
    print("Checking permissions...")
    added = False
    
    # Check if user has role:admin or role:operator
    # Based on logs: simulator < (role:admin, role:operator)
    # It seems simulator ALREADY inherits roles.
    
    if not enforcer.enforce('simulator', 'registry.machine', 'write'):
        enforcer.add_policy('simulator', 'registry.machine', 'write')
        print("Added explicit: simulator -> registry.machine -> write")
        added = True
    else:
        print("Permission 'write' on 'registry.machine': OK")

    if added:
        enforcer.save_policy()

    print("--- DONE ---")

if __name__ == "__main__":
    run()