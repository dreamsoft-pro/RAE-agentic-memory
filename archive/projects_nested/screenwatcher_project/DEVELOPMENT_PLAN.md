# ScreenWatcher Development Plan

## Status Obecny (Current State)
- **Branch:** develop
- **Technologia:** Django 5.2 (LTS), Python 3.13, Django Channels (WebSockets), Celery, Redis, MariaDB/SQLite.
- **Testy:** 31 testów (Rules, API, OEE, Serializers, Reports, Operator Panel).
- **Architektura:** Modularny monolit z dynamicznym routerem bazy danych i mechanizmem Rollupu.

## Cel Główny
Dostarczenie stabilnego, skalowalnego systemu OEE z obsługą czasu rzeczywistego i analityką przemysłową.

## Faza 1: Stabilizacja i Dokumentacja (ZAKOŃCZONA)
1. **Podniesienie pokrycia testami (Target: 80%)**
   - [x] Coverage osiągnięty: 86% (wszystkie moduły kluczowe).
   - [x] Rules Engine (Logic + Hits)
   - [x] Registry API
   - [x] Collector Ingestion
   - [x] Operator Panel & Reports
2. **Dokumentacja API**
   - [x] Konfiguracja drf-spectacular (Swagger)
   - [x] Schema OpenAPI 3.0
3. **Konfiguracja CI/CD**
   - [x] GitHub Actions (dodanie brancha develop i Python 3.13)
   - [ ] Weryfikacja docker-compose.yml pod Django 5.2

## Faza 2: Real-time i Dashboard (ZAKOŃCZONA)
1. **WebSockets (Kluczowe)**
   - [x] Implementacja Consumers dla Telemetrii.
   - [x] Rozgłaszanie (Broadcast) zmian przez Django Signals.
2. **Dynamiczny Frontend**
   - [x] Integracja dashboard.html z WebSockets.
   - [x] Pełne odświeżanie wykresów ECharts bez przeładowania (Event-driven OEE updates).

## Faza 3: Weryfikacja Przepływu Danych (ZAKOŃCZONA)
1. [x] Symulacja: Użycie `tools/simulator.py` do testów (zweryfikowano Ingestion API).
2. [x] Inicjalizacja: Skrypt `tools/init_simulation_data.py` konfigurujący środowisko testowe.

## Faza 4: Industrial Excellence (ZAKOŃCZONA)
1. [x] Obsługa Zmian (Shifts): Modele `Shift` i `ShiftOEE` zaimplementowane.
2. [x] Logika OEE: `OEECalculator` wspiera teraz obliczenia per zmiana.
3. [x] Kategoryzacja Przestojów: Model `DowntimeEvent` gotowy.
4. [x] Interfejs dla operatora do oznaczania powodów zatrzymań (API ViewSets).
5. [x] Mechanizm Rollupu: Automatyczna agregacja danych surowych (Hourly Rollup).
6. [x] Dynamic Dashboard: System widgetowy z obsługą Gridstack.js.
7. [x] Historyczne Porównania: API agregujące dane (dzień/tydzień/miesiąc).
8. [x] Zaawansowane KPI: Implementacja MTBF, MTTR oraz Scrap Rate.
9. [x] Nowe Widgety: Heatmapa OEE oraz Karta Niezawodności.

## Roadmapa (Next Steps)
1. [x] Faza 1: Weryfikacja docker-compose.yml pod Django 5.2.
2. [x] Faza 5: Finalne testy end-to-end (E2E) (Zaimplementowano podstawowy flow).
3. [x] Dokumentacja zmian API (Downtime).
4. [x] Zero Drift: Automatyczna weryfikacja migracji w CI.
5. [x] Load Testing: Skrypt `locustfile.py` do testów obciążeniowych.
6. [x] Zaawansowane filtry Casbin dla Dashboardów (filtrowanie maszyn per user).
7. [x] System powiadomień (Rules Action -> Dashboard Alert).
