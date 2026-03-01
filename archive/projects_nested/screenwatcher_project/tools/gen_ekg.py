
import os
import django
import random
import datetime
from django.utils import timezone
import math

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint
from apps.oee.models import DailyOEE, ShiftOEE

def generate_ekg_data():
    machine = Machine.objects.first()
    if not machine:
        print("No machine found!")
        return

    print(f"Generowanie danych 'EKG' dla maszyny: {machine.code}")

    # Wyczyść stare dane z ostatnich 24h, żeby wykres był czysty
    now = timezone.now()
    start_time = now - datetime.timedelta(hours=24)
    TelemetryPoint.objects.filter(machine=machine, timestamp__gte=start_time).delete()

    points = []
    current_time = start_time
    
    # Generujemy 2000 punktów w ciągu 24h
    total_points = 2000
    
    # Bazowa prędkość i szum
    base_interval = 45 # średnio co 45 sekund zrzut
    
    for i in range(total_points):
        # Symulacja "EKG": Sinusoida + Szum
        # Sinusoida o okresie ~2h
        factor = (math.sin(i * 0.1) + 1) / 2 # 0..1
        
        # Zmienny odstęp czasu: im szybciej maszyna pracuje, tym mniejszy odstęp
        # Szybko: 10s, Wolno: 120s
        interval = 10 + (1.0 - factor) * 110 
        
        # Dodaj losowy szum (jitter)
        jitter = random.randint(-5, 5)
        interval += jitter
        if interval < 5: interval = 5
        
        current_time += datetime.timedelta(seconds=interval)
        
        if current_time > now:
            break

        # Czasami maszyna "produkuje" więcej niż 1 sztukę (np. pakiet)
        parts = 1
        if random.random() > 0.9: parts = random.randint(2, 5)
        
        # Czasami przestój (brak produkcji = 0)
        if random.random() > 0.95: parts = 0

        payload = {
            "status": "RUNNING" if parts > 0 else "IDLE",
            "metrics": {
                "temp": 60 + random.random() * 20,
                "parts_delta": parts,
                "speed_setpoint": 1000
            }
        }
        
        points.append(TelemetryPoint(
            machine=machine,
            timestamp=current_time,
            payload=payload,
            kind="telemetry"
        ))

    TelemetryPoint.objects.bulk_create(points)
    print(f"Wygenerowano {len(points)} punktów o zmiennej charakterystyce.")

if __name__ == "__main__":
    generate_ekg_data()
