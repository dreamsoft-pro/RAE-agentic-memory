# Plan kontynuacji - Stabilizacja Testów

## Stan na 2026-01-29
- **Testy:** 1079 passed, 0 failed, 7 skipped.
- **Kluczowe poprawki:**
    - `rae_adapters/postgres.py`: Mapowanie `episodic` <-> `em` we wszystkich metodach (store, query, count, delete).
    - `apps/memory_api/security/auth.py`: Odporność na brak `app.state.pool` w trybie `ignore`.
    - `apps/memory_api/observability/health_checks.py`: Naprawiony `NameError` (brak importu `os`).
    - `tests/integration/test_dreaming_worker.py`: Synchronizacja manualnych insertów SQL z mapowaniem adaptera (`em`).

## Do zrobienia w następnej sesji
1. **Weryfikacja pominiętych testów (7):**
    - Sprawdzić, czy testy wymagające `spacy`, `sentence-transformers` i `presidio` powinny zostać przeniesione do testów integracyjnych/benchmarków na klastrze, czy wymagają lżejszych mocków.
    - Zweryfikować testy `hard_frames` (wymagają działającego kontenera `rae-agent-secure`).
2. **Push i monitoring CI:**
    - Wykonać `make pre-push` i wypchnąć zmiany na branch deweloperski.

## Polecenie startowe
`python3 scripts/bootstrap_session.py`
