from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.dashboards.models import Dashboard, Widget
from apps.registry.models import Machine
import uuid

class Command(BaseCommand):
    help = 'Seeds the database with default dashboards and widgets'

    def handle(self, *args, **options):
        users = User.objects.all()
        machines = Machine.objects.all()

        if not machines.exists():
            self.stdout.write(self.style.WARNING('No machines found in registry. Skipping widget creation.'))
            return

        for user in users:
            dashboard, created = Dashboard.objects.get_or_create(
                user=user,
                is_default=True,
                defaults={'name': 'My Main Dashboard'}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created default dashboard for user: {user.username}'))
            
            # Add default widgets for each machine if not present
            for machine in machines:
                self.ensure_widget(dashboard, 'oee_gauge', f'OEE - {machine.name}', machine.id)
                self.ensure_widget(dashboard, 'production_trend', f'Trend - {machine.name}', machine.id)
                self.ensure_widget(dashboard, 'machine_gantt', f'Status - {machine.name}', machine.id)

    def ensure_widget(self, dashboard, w_type, title, machine_id):
        exists = Widget.objects.filter(
            dashboard=dashboard,
            widget_type=w_type,
            config__machine_id=str(machine_id)
        ).exists()
        
        if not exists:
            Widget.objects.create(
                dashboard=dashboard,
                widget_type=w_type,
                title=title,
                config={'machine_id': str(machine_id)},
                pos_x=0,
                pos_y=0,
                width=4,
                height=3
            )
            self.stdout.write(self.style.SUCCESS(f'  Added widget: {title} ({w_type})'))
