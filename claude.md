# RAE_V2_OPTIMIZATION_PLAN.md

## 1. Kontekst i Cel
Celem tego planu jest modernizacja architektury projektu RAE (Reflective Agentic-mode Engine). Projekt osiągnął stabilność funkcjonalną (GraphRAG), ale wymaga refaktoryzacji pod kątem skalowalności, czystości kodu (DAO) i wiarygodności testów.

**Główne cele:**
1. **Separacja odpowiedzialności:** Wydzielenie warstwy dostępu do danych (DAO/Repositories).
2. **Mikroserwisyzacja:** Wyniesienie ciężkich zależności ML (torch, transformers) do osobnego serwisu.
3. **Wiarygodność testów:** Wdrożenie `testcontainers` dla testów integracyjnych.

---

## Faza 1: Warstwa Dostępu do Danych (DAO Pattern)
**Cel:** Usunięcie surowego SQL z warstwy serwisów biznesowych.
**Status obecny:** Zapytania SQL są zaszyte w `HybridSearchService` i `GraphExtractionService`.

### Zadanie 1.1: Utworzenie `GraphRepository`
* **Pliki do utworzenia:** `apps/memory_api/repositories/graph_repository.py`
* **Pliki do modyfikacji:** `apps/memory_api/services/hybrid_search.py`
* **Instrukcje dla Agenta:**
    1.  Stwórz klasę `GraphRepository` przyjmującą w `__init__` poolę połączeń asyncpg.
    2.  Przenieś metodę `get_subgraph` (i jej zapytanie SQL) z `HybridSearchService` do repozytorium.
    3.  Przenieś logikę trawersowania BFS (zapytanie Recursive CTE) do metody `traverse_graph_bfs` w repozytorium.
    4.  W `HybridSearchService` wstrzyknij `GraphRepository` i używaj jego metod zamiast wołać `self.db_pool.fetch`.
* **Kryteria akceptacji:**
    * `HybridSearchService` nie zawiera żadnego ciągu znaków zaczynającego się od `SELECT`, `WITH RECURSIVE` etc.
    * Testy w `apps/memory_api/tests/test_hybrid_search.py` przechodzą bez zmian (refactor).

### Zadanie 1.2: Utworzenie `MemoryRepository`
* **Pliki do utworzenia:** `apps/memory_api/repositories/memory_repository.py`
* **Pliki do modyfikacji:** `apps/memory_api/services/memory_service.py`, `apps/memory_api/services/graph_extraction.py`
* **Instrukcje dla Agenta:**
    1.  Wydziel operacje CRUD na tabeli `memories` (insert, select by id, vector search) do `MemoryRepository`.
    2.  Zaktualizuj `MemoryService` oraz `GraphExtractionService` (tam gdzie pobiera wspomnienia do ekstrakcji), aby korzystały z repozytorium.
* **Kryteria akceptacji:**
    * Brak surowego SQL w `MemoryService`.

---

## Faza 2: Wydzielenie ML Service (Microservice Extraction)
**Cel:** Odciążenie głównego obrazu Dockera. Główny serwis nie powinien zawierać `sentence-transformers` ani `spacy`.

### Zadanie 2.1: Szkielet ML Service
* **Ścieżka:** `apps/ml_service/`
* **Instrukcje dla Agenta:**
    1.  Stwórz nową aplikację FastAPI w folderze `apps/ml_service`.
    2.  Skopiuj `requirements.txt` z głównego serwisu, ale zostaw TYLKO biblioteki ML: `torch`, `sentence-transformers`, `spacy`, `scikit-learn`, `numpy`.
    3.  Usuń te biblioteki z `apps/memory_api/requirements.txt` (główny serwis ma być lekki).
    4.  Stwórz `Dockerfile` dla `apps/ml_service`.

### Zadanie 2.2: Przeniesienie logiki Entity Resolution
* **Przenieś:** `apps/memory_api/services/entity_resolution.py` -> `apps/ml_service/services/entity_resolution.py`
* **Przenieś:** `apps/memory_api/services/graph_extraction.py` (tylko część używającą Spacy/NLP) -> `apps/ml_service/services/nlp.py`
* **Instrukcje dla Agenta:**
    1.  W `apps/ml_service` wystaw endpointy:
        * `POST /resolve-entities` (przyjmuje listę węzłów, zwraca grupy do scalenia).
        * `POST /extract-triples` (opcjonalnie, jeśli lokalne NLP jest używane).
    2.  W głównym serwisie (`memory_api`) stwórz klienta HTTP `MLServiceClient`, który łączy się z `http://ml-service:8000`.
* **Kryteria akceptacji:**
    * Test `apps/memory_api/tests/test_entity_resolution.py` musi zostać zaktualizowany, aby mockować odpowiedzi HTTP od `MLServiceClient` zamiast wołać lokalną klasę.
    * `docker-compose.yml` zawiera nową usługę `ml-service`.

---

## Faza 3: Hardening Testów (Testcontainers)
**Cel:** Zastąpienie mocków prawdziwą bazą danych w testach integracyjnych.

### Zadanie 3.1: Konfiguracja Testcontainers
* **Pliki do modyfikacji:** `apps/memory_api/tests/conftest.py`, `apps/memory_api/requirements-dev.txt`
* **Instrukcje dla Agenta:**
    1.  Dodaj `testcontainers[postgres]` do `requirements-dev.txt`.
    2.  W `conftest.py` stwórz fixture `postgres_container` (scope session).
    3.  Skonfiguruj kontener tak, aby używał obrazu `ankane/pgvector`.
    4.  Nadpisz fixture `db_pool` tak, aby łączył się z dynamicznym portem kontenera, a nie mockiem.
    5.  Upewnij się, że migracje Alembic uruchamiają się na starcie kontenera testowego.

### Zadanie 3.2: Aktualizacja Testów Hybrydowych
* **Pliki do modyfikacji:** `apps/memory_api/tests/test_hybrid_search.py`
* **Instrukcje dla Agenta:**
    1.  Usuń mockowanie `pool.fetch` i `pool.execute`.
    2.  Testy mają zapisywać prawdziwe dane do bazy testowej (INSERT), a następnie wołać `HybridSearchService`.
    3.  Zweryfikuj, czy testy rekurencyjnego CTE przechodzą na prawdziwej bazie.
* **Kryteria akceptacji:**
    * Uruchomienie `pytest apps/memory_api/tests/test_hybrid_search.py` nie zwraca błędów połączenia ani błędów SQL syntax error.

---

## Faza 4: Dokumentacja i Porządki
**Cel:** Ułatwienie pracy deweloperom (ludziom).

### Zadanie 4.1: Aktualizacja OpenAPI
* **Pliki do modyfikacji:** Modele Pydantic w `apps/memory_api/models/`.
* **Instrukcje dla Agenta:**
    1.  Dodaj klasę `Config` z polem `json_schema_extra` (przykłady) do wszystkich modeli requestów/response (np. `GraphQueryRequest`, `AddMemoryRequest`).
    2.  Sprawdź, czy endpointy mają poprawne `response_model` i opisy (`summary`, `description`).

### Zadanie 4.2: Update README
* **Plik:** `README.md`
* **Instrukcje dla Agenta:**
    1.  Zaktualizuj instrukcję uruchomienia (dodanie `ml-service` do docker-compose).
    2.  Opisz architekturę (podział na Memory API i ML Service).