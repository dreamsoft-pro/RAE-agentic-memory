from celery import shared_task
from django.utils import timezone
from apps.registry.models import Machine
from .services import OEECalculator
import datetime

@shared_task
def calculate_daily_oee_task(machine_id, date_str=None):
    """
    Task to calculate OEE for a specific machine and date.
    date_str: ISO format date (YYYY-MM-DD). Defaults to yesterday.
    """
    machine = Machine.objects.get(id=machine_id)
    if date_str:
        date = datetime.date.fromisoformat(date_str)
    else:
        date = (timezone.now() - datetime.timedelta(days=1)).date()
    
    OEECalculator.calculate_daily(machine, date)
    return f"OEE calculated for {machine.code} on {date}"

@shared_task
def calculate_all_machines_oee_task(date_str=None):
    """
    Task to trigger OEE calculation for all active machines.
    """
    machines = Machine.objects.filter(is_active=True)
    count = 0
    for machine in machines:
        calculate_daily_oee_task.delay(str(machine.id), date_str)
        count += 1
    return f"Triggered OEE calculation for {count} machines"
