from django.core.management.base import BaseCommand
from apps.rbac.services import EnforcerService

class Command(BaseCommand):
    help = 'Initialize RBAC roles and policies'

    def handle(self, *args, **kwargs):
        e = EnforcerService.get_enforcer()
        
        # Clear existing rules (optional, safer for dev)
        # e.clear_policy() 

        # Define Roles & Permissions
        
        # ROLE: operator
        # Can read registry
        EnforcerService.add_policy("role:operator", "registry.machine", "read")
        EnforcerService.add_policy("role:operator", "registry.line", "read")
        # Can write telemetry (ingest)
        # Assuming ingest view checks for 'collector.ingest' resource permission or similar
        # But our permission class checks model name. Collector uses serializer based view, 
        # so we need to be careful. For now let's say they can write telemetry points.
        EnforcerService.add_policy("role:operator", "telemetry.telemetrypoint", "write")
        
        # ROLE: manager
        # Can manage registry
        EnforcerService.add_policy("role:manager", "registry.machine", "write")
        EnforcerService.add_policy("role:manager", "registry.machine", "update")
        EnforcerService.add_policy("role:manager", "registry.machine", "read")
        EnforcerService.add_policy("role:manager", "registry.line", "read")
        EnforcerService.add_policy("role:manager", "registry.department", "read")
        EnforcerService.add_policy("role:manager", "registry.factory", "read")
        
        self.stdout.write(self.style.SUCCESS('RBAC policies initialized successfully.'))
