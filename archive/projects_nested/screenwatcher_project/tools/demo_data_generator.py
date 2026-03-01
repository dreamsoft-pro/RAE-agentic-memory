import os
import sys
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screenwatcher_project.settings')
django.setup()

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint
from apps.oee.models import DowntimeEvent, DailyOEE, ReasonCode
from apps.oee.services import OEECalculator

def generate_demo_data():
    machine_code = "TM01"
    days_back = 3
    cycle_time = 6.0 # seconds per part (billboard sheet)
    
    print(f"--- GENERATING DEMO DATA FOR {machine_code} ---")
    
    # 1. Get Machine
    try:
        machine = Machine.objects.get(code=machine_code)
    except Machine.DoesNotExist:
        print(f"Machine {machine_code} not found. Run init_simulation_data.py first.")
        return

    # 2. Clear old data for clean demo
    print("Cleaning old telemetry...")
    TelemetryPoint.objects.filter(machine=machine).delete()
    DowntimeEvent.objects.filter(machine=machine).delete()
    DailyOEE.objects.filter(machine=machine).delete()
    
    # 3. Setup Reasons
    reason_setup, _ = ReasonCode.objects.get_or_create(code="SETUP", defaults={"description": "Changeover / Setup", "category": "PLANNED"})
    reason_failure, _ = ReasonCode.objects.get_or_create(code="FAIL", defaults={"description": "Component Failure", "category": "UNPLANNED"})
    
    # 4. Generate Timeline
    end_time = timezone.now()
    start_time = end_time - timedelta(days=days_back)
    start_time = start_time.replace(hour=6, minute=0, second=0, microsecond=0) # Start from 1st shift
    
    current_time = start_time
    total_points = 0
    
    # Scheduled Changeovers (4 random times in the range)
    changeover_starts = []
    window = (end_time - start_time).total_seconds()
    for _ in range(4):
        offset = random.uniform(0, window)
        changeover_starts.append(start_time + timedelta(seconds=offset))
    changeover_starts.sort()
    
    # Simulation Loop
    while current_time < end_time:
        # Determine State
        state = "RUNNING"
        parts_delta = 1 # Default 1 part per cycle
        
        # Check for Changeover
        in_changeover = False
        for co_start in changeover_starts:
            co_end = co_start + timedelta(minutes=random.randint(30, 45))
            if co_start <= current_time <= co_end:
                state = "STOPPED"
                parts_delta = 0
                
                # Create Downtime Event if at start
                if current_time == co_start: # Approximation
                    DowntimeEvent.objects.create(
                        machine=machine,
                        start_time=co_start,
                        end_time=co_end,
                        reason=reason_setup
                    )
                in_changeover = True
                break
        
        if not in_changeover:
            # Random Failure (1% chance every minute -> approx 14 failures per day)
            # Reduced to 0.1% per 6s cycle -> ~14 failures per day
            if random.random() < 0.001: 
                fail_duration = timedelta(minutes=random.randint(5, 15))
                fail_end = current_time + fail_duration
                
                # Fast forward loop
                DowntimeEvent.objects.create(
                    machine=machine,
                    start_time=current_time,
                    end_time=fail_end,
                    reason=reason_failure
                )
                
                # Fill telemetry for failure
                fail_ptr = current_time
                while fail_ptr < fail_end:
                    TelemetryPoint.objects.create(
                        machine=machine,
                        timestamp=fail_ptr,
                        payload={
                            "status": "ERROR",
                            "metrics": {"temp": 85.0, "parts_delta": 0}
                        }
                    )
                    fail_ptr += timedelta(seconds=30) # coarser granularity for downtime
                
                current_time = fail_end
                continue
        
        # Microstops (random 2s delay)
        actual_cycle = cycle_time
        if random.random() < 0.05:
            actual_cycle += 2.0
            
        # Telemetry Point
        TelemetryPoint.objects.create(
            machine=machine,
            timestamp=current_time,
            payload={
                "status": state,
                "metrics": {
                    "temp": round(random.uniform(60, 75), 1),
                    "speed": 600 if state == "RUNNING" else 0, # sheets per hour
                    "parts_delta": parts_delta
                }
            }
        )
        total_points += 1
        
        if total_points % 1000 == 0:
            print(f"Generated {total_points} points... ({current_time})")
            
        current_time += timedelta(seconds=actual_cycle)

    print(f"DONE. Generated {total_points} telemetry points.")
    
    # 5. Recalculate OEE
    print("Recalculating Daily OEE...")
    # This might be slow for 3 days of raw data, but it's correct
    # For demo, we might skip full recalculation or run it for just the last day
    # Or rely on the nightly task. 
    # Let's trigger a simplified calc for the dashboard
    
    dates = [end_time.date() - timedelta(days=i) for i in range(days_back + 1)]
    for d in dates:
        print(f"Calculating for {d}...")
        try:
             OEECalculator.calculate_daily(machine, d)
        except Exception as e:
            print(f"Calc error for {d}: {e}")

if __name__ == "__main__":
    generate_demo_data()
