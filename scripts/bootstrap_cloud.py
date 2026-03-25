#!/usr/bin/env python3
import os
from pathlib import Path

# Dynamic Project Root Resolution
PROJECT_ROOT = Path(os.environ.get('RAE_PROJECT_ROOT', Path(__file__).resolve().parent.parent))
CLOUD_ROOT = PROJECT_ROOT.parent

def bootstrap():
    print('🚀 BOOTSTRAP: Inicjalizacja kontekstu Cloud...')
    
    # Kluczowe fakty infrastrukturalne
    print('\n--- KRYTYCZNE INFORMACJE (ALWAYS ON) ---')
    print('📍 Laptop MySQL Port: 3307')
    print('📍 Node 1 (Lumina): 100.68.166.117')
    print('📍 Factory Version: v2.2 (Orchestrated by RAE-Feniks)')
    print('📍 Observability: OpenTelemetry + Jaeger (OFFLINE)')
    print('📍 Security Mode: HARD FRAMES Active')
    print(f'📍 Output Dir (TS): {PROJECT_ROOT / "apps/memory_api/services/"}')
    print('📍 Final Session Progress: 1424 files fully modernized')
    print('----------------------------------------\n')

    plan_path = CLOUD_ROOT / 'docs/modernization/DREAMSOFT_MASTER_PLAN_2026.md'
    if plan_path.exists():
        print('--- AKTUALNY STATUS MODERNIZACJI (DREAMSOFT PRO 2.0) ---')
        with open(plan_path, 'r') as f:
            # Pokaż tylko pierwsze 30 linii dla czytelności
            lines = f.readlines()
            for line in lines[:35]:
                print(line.strip())
        print('--------------------------------------------------------\n')
    
    # Strategia Oracle V2.0
    oracle_plan = CLOUD_ROOT / 'docs/modernization/STRATEGIC_ORACLE_PLAN_V2.md'
    if oracle_plan.exists():
        print('👑 STRATEGIA ORACLE V2.0 (THE AGENTIC BOARD):')
        with open(oracle_plan, 'r') as f:
            print(f.read())
        print('--------------------------------------------------------\n')
    
    # Mission Briefing Feniks
    mission_path = CLOUD_ROOT / 'docs/modernization/MISSION_BRIEFING_FENIKS.md'
    if mission_path.exists():
        print('🎯 MISSION BRIEFING (PHASE 2 STRATEGY):')
        with open(mission_path, 'r') as f:
            print(f.read())
        print('--------------------------------------------------------\n')

    # Cele operacyjne
    next_goals = CLOUD_ROOT / 'docs/modernization/NEXT_SESSION_GOALS.md'
    if next_goals.exists():
        print('🗓️ CELE NA RANO (AGENTIC FACTORY 2.0):')
        with open(next_goals, 'r') as f:
            print(f.read())
        print('--------------------------------------------------------\n')
    
    print('✅ KONTEKST ZAŁADOWANY. Gotowy do pracy nad Modernizacją Dreamsoft.')

if __name__ == "__main__":
    bootstrap()
