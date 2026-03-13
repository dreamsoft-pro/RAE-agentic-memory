#!/usr/bin/env python3
import os

def bootstrap():
    print('🚀 BOOTSTRAP: Inicjalizacja kontekstu Cloud...')
    
    # Kluczowe fakty infrastrukturalne
    print('\n--- KRYTYCZNE INFORMACJE (ALWAYS ON) ---')
    print('📍 Laptop MySQL Port: 3307')
    print('📍 Node 1 (Lumina): 100.68.166.117')
    print('📍 Factory Version: v2.2 (Orchestrated by RAE-Feniks)')
    print('📍 Observability: OpenTelemetry + Jaeger (OFFLINE)')
    print('📍 Security Mode: HARD FRAMES Active')
    print('📍 Output Dir (TS): /mnt/extra_storage/RAE-agentic-memory/apps/memory_api/services/')
    print('📍 Final Session Progress: 1424 files fully modernized')
    print('----------------------------------------\n')

    plan_path = '/home/grzegorz-lesniowski/cloud/docs/modernization/DREAMSOFT_MASTER_PLAN_2026.md'
    if os.path.exists(plan_path):
        print('--- AKTUALNY STATUS MODERNIZACJI (DREAMSOFT PRO 2.0) ---')
        with open(plan_path, 'r') as f:
            # Pokaż tylko pierwsze 30 linii dla czytelności
            lines = f.readlines()
            for line in lines[:35]:
                print(line.strip())
        print('--------------------------------------------------------\n')
    
    # Strategia Oracle V2.0
    oracle_plan = '/home/grzegorz-lesniowski/cloud/docs/modernization/STRATEGIC_ORACLE_PLAN_V2.md'
    if os.path.exists(oracle_plan):
        print('👑 STRATEGIA ORACLE V2.0 (THE AGENTIC BOARD):')
        with open(oracle_plan, 'r') as f:
            print(f.read())
        print('--------------------------------------------------------\n')
    
    # Mission Briefing Feniks
    mission_path = '/home/grzegorz-lesniowski/cloud/docs/modernization/MISSION_BRIEFING_FENIKS.md'
    if os.path.exists(mission_path):
        print('🎯 MISSION BRIEFING (PHASE 2 STRATEGY):')
        with open(mission_path, 'r') as f:
            print(f.read())
        print('--------------------------------------------------------\n')

    # Cele operacyjne
    next_goals = '/home/grzegorz-lesniowski/cloud/docs/modernization/NEXT_SESSION_GOALS.md'
    if os.path.exists(next_goals):
        print('🗓️ CELE NA RANO (AGENTIC FACTORY 2.0):')
        with open(next_goals, 'r') as f:
            print(f.read())
        print('--------------------------------------------------------\n')
    
    print('✅ KONTEKST ZAŁADOWANY. Gotowy do pracy nad Modernizacją Dreamsoft.')

if __name__ == "__main__":
    bootstrap()
