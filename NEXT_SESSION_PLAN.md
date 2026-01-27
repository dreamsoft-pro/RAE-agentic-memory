# Plan Następnej Sesji - Stabilizacja Core (2026-01-27)

## Status Sesji
Zakończono naprawę kilkunastu regresji po refaktoryzacji na Luminie. Wdrożono zasadę "Fail Fast".

## Co zostało zrobione:
1.  **AGENT_CORE_PROTOCOL.md**: Dodano zasadę przerywania testów na pierwszym błędzie.
2.  **Fixy Importów/Klas**: Naprawiono `test_stability_fusion.py` oraz `MultiVectorSearchStrategy` (migracja na klasę `RRFFusion`).
3.  **Cleanup**: Usunięto przestarzałe testy (`test_engine_extended.py`, `test_engine_extra.py`).
4.  **Przywrócenie poprawek**: Re-aplikowano poprawki `agent_id` w Postgresie i `ttl` w InMemoryStorage, które zostały nadpisane przez rsync.
5.  **Maki i Telemetria**: Naprawiono mocki w `test_background_tasks.py` (async) oraz `test_opentelemetry.py` (`AsyncQdrantClient`).
6.  **Math & Logic**: Naprawiono błąd `timedelta` w `math/controller.py` oraz uwzględnianie wag strategii w `HybridSearchEngine`.
7.  **RRF Logic**: Zaktualizowano testy hybrydowe do logiki rankingu 0-indexed.

## Do zrobienia w następnej sesji:
1.  **Weryfikacja**: Kontynuacja uruchamiania pełnego suite: `.venv/bin/python -m pytest -x apps/memory_api/tests rae-core/tests`.
2.  **Naprawa kolejnych błędów**: Systematyczne usuwanie przeszkód aż do osiągnięcia 100% PASS (obecnie około 1640/1736 testów przechodzi).
3.  **Zero Drift**: Po przejściu testów, wykonanie `make pre-push` i commit dokumentacji.

## Komenda na start:
`python3 scripts/bootstrap_session.py && .venv/bin/python -m pytest -x apps/memory_api/tests rae-core/tests`