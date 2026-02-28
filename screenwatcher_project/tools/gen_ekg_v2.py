
import os
import django
import random
import datetime
from django.utils import timezone
import math

# Setup Django context (needed when running as script)
import sys
from pathlib import Path

# Add project root to sys.path if not present
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "screenwatcher_project.settings")
django.setup()

from apps.registry.models import Machine
from apps.telemetry.models import TelemetryPoint

def generate_ekg_data_v2():
    machine = Machine.objects.first()
    if not machine:
        print("No machine found!")
        return

    print(f"Generowanie danych 'EKG v2' (mikro-przestoje, stabilniejsza prędkość) dla: {machine.code}")

    # Wyczyść stare dane z ostatnich 24h
    now = timezone.now()
    start_time = now - datetime.timedelta(hours=24)
    TelemetryPoint.objects.filter(machine=machine, timestamp__gte=start_time).delete()

    points = []
    current_time = start_time
    
    # Parametry symulacji
    # Chcemy ok. 10 sekund między punktami, żeby mieć dobrą rozdzielczość wykresu
    step_seconds = 10 
    
    # Stan maszyny
    is_running = True
    downtime_counter = 0
    
    # Sinusoida prędkości (powolne falowanie wydajności)
    phase = 0.0

    while current_time < now:
        # 1. Logika Przestojów (Mikro-przestoje)
        if is_running:
            # 2% szans na wystąpienie mikro-przestoju w każdym kroku (co 10s)
            # Średnio raz na 500s (8 minut)
            if random.random() < 0.02:
                is_running = False
                # Przestój trwa losowo od 30s do 120s (3 do 12 cykli)
                downtime_counter = random.randint(3, 12)
        else:
            downtime_counter -= 1
            if downtime_counter <= 0:
                is_running = True

        # 2. Logika Produkcji
        parts = 0
        status = "IDLE"
        
        if is_running:
            status = "RUNNING"
            
            # Modulacja prędkości (2x - 3x różnicy)
            # Używamy sinusoidy do płynnej zmiany "tempa" operatora
            # Okres fali: ok. 1 godzina (360 kroków po 10s)
            phase += 0.017 
            efficiency = (math.sin(phase) + 1.5) / 2.5 # Waha się od 0.2 do 1.0 (znormalizowane)
            
            # Bazowo produkujemy 1 sztukę co X sekund.
            # Tutaj symulujemy to prawdopodobieństwem wyprodukowania sztuki w oknie 10s.
            # Max prędkość: 360 szt/h (1 szt co 10s) -> prob = 1.0
            # Min prędkość: 120 szt/h (1 szt co 30s) -> prob = 0.33
            
            # Skalujemy efficiency do zakresu 0.33 ... 0.9
            prob = 0.33 + (efficiency * 0.57) 
            
            if random.random() < prob:
                parts = 1
                # Rzadko (1%) zrobiono 2 sztuki na raz (szybki ruch)
                if random.random() < 0.01: parts = 2

        # 3. Tworzenie punktu
        payload = {
            "status": status,
            "metrics": {
                "temp": 65 + random.random() * 5,
                "parts_delta": parts, # 0 lub 1 (czasem 2)
                "speed_setpoint": 1000
            }
        }
        
        points.append(TelemetryPoint(
            machine=machine,
            timestamp=current_time,
            payload=payload,
            kind="telemetry"
        ))
        
        # Przesuń czas
        current_time += datetime.timedelta(seconds=step_seconds)
        
        # Batch save co 5000 punktów, żeby nie zjeść RAMu
        if len(points) >= 5000:
            TelemetryPoint.objects.bulk_create(points)
            points = []
            print(f"Zapisano partię danych do {current_time}")

    if points:
        TelemetryPoint.objects.bulk_create(points)
    
    print("Zakończono generowanie danych v2.")

if __name__ == "__main__":
    generate_ekg_data_v2()
