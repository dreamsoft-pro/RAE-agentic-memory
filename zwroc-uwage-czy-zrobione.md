# RAE_V1.1_PERFECTION_PLAN.md

## Cel
Podniesienie oceny architektury do **10/10** poprzez pełne odseparowanie warstw (Dependency Injection) oraz realizacja poprawek z zakresu bezpieczeństwa i operacyjności (logs management) wskazanych w audycie v1.0.0.

---

## Faza 1: Architektura 10/10 (Dependency Injection & Decoupling)
**Problem:** Obecnie serwisy (np. `GraphExtractionService`) same instancjonują repozytoria wewnątrz `__init__`, przyjmując obiekt `pool`. To tworzy ukryte zależności i utrudnia testowanie jednostkowe (wymaga mockowania poola DB zamiast repozytorium).
**Cel:** Serwisy mają przyjmować gotowe instancje repozytoriów w konstruktorze.

### Zadanie 1.1: Refaktoryzacja `GraphExtractionService`
* **Plik:** `apps/memory_api/services/graph_extraction.py`
* **Zmiana:**
    - Zmień sygnaturę `__init__`: zamiast `pool: asyncpg.Pool` przyjmij `graph_repo: GraphRepository, memory_repo: MemoryRepository`.
    - Usuń wewnętrzne tworzenie repozytoriów.
* **Zaleta:** 100% separacji. Możesz przetestować logikę ekstrakcji podając fałszywe repozytoria (InMemory), nie dotykając bazy danych.

### Zadanie 1.2: Refaktoryzacja `HybridSearchService`
* **Plik:** `apps/memory_api/services/hybrid_search.py`
* **Zmiana:**
    - Zmień sygnaturę `__init__`: przyjmij `graph_repo: GraphRepository` oraz `vector_store: VectorStore`.
    - Usuń zależność od `pool` w tej klasie.

### Zadanie 1.3: Wiring w `main.py` (Composition Root)
* **Plik:** `apps/memory_api/dependencies.py` (lub `main.py`)
* **Akcja:** Stwórz fabryki (dependencies) dla FastAPI, które "składają" obiekty:
    ```python
    # Pseudo-kod
    def get_graph_service(pool = Depends(get_db_pool)):
        repo = GraphRepository(pool)
        mem_repo = MemoryRepository(pool)
        return GraphExtractionService(repo, mem_repo)
    ```
* **Wstrzykiwanie:** Zaktualizuj endpointy API, aby korzystały z tych zależności, zamiast tworzyć serwisy ad-hoc.

---

## Faza 2: Operacyjność i Czystość Logów (Fix Point 4a)
**Problem:** Domyślny poziom logowania `INFO` dla bibliotek `uvicorn` i `celery` generuje zbyt dużo szumu na produkcji.

### Zadanie 2.1: Konfiguracja Logowania
* **Plik:** `.env.example`
* **Akcja:** Dodaj zmienną:
    ```env
    LOG_LEVEL=WARNING
    RAE_APP_LOG_LEVEL=INFO  # Logi aplikacji chcemy widzieć, bibliotek niekoniecznie
    ```

### Zadanie 2.2: Aktualizacja `logging_config.py`
* **Plik:** `apps/memory_api/logging_config.py`
* **Akcja:** Skonfiguruj `structlog` tak, aby:
    - Logery bibliotek zewnętrznych (`uvicorn`, `asyncpg`, `httpx`) respektowały poziom `LOG_LEVEL` (WARNING).
    - Loger aplikacji (`apps.memory_api`) respektował `RAE_APP_LOG_LEVEL` (INFO).

---

## Faza 3: Bezpieczeństwo Skryptów (Fix Point 4b)
**Problem:** Skrypt `quickstart.sh` wyświetla wpisywane klucze API w terminalu, co może zostać zapisane w historii powłoki lub być widoczne dla osób postronnych.

### Zadanie 3.1: Secure Input w `quickstart.sh`
* **Plik:** `scripts/quickstart.sh`
* **Akcja:** Zastąp komendy `read -p` wersją `read -s -p` (silent mode) dla wszystkich kluczy API.
* **Kod:**
    ```bash
    # Zamiast:
    # read -p "Enter your OpenAI API key: " api_key
    
    # Użyj:
    echo -n "Enter your OpenAI API key (input hidden): "
    read -s api_key
    echo "" # Nowa linia po enterze
    ```

### Zadanie 3.2: Weryfikacja uprawnień
* **Plik:** `scripts/quickstart.sh`
* **Akcja:** Upewnij się, że skrypt nadaje plikowi `.env` uprawnienia `600` (tylko odczyt dla właściciela) po jego utworzeniu, aby inne procesy w systemie nie mogły go czytać.

---

## Faza 4: Weryfikacja (Quality Assurance)

### Zadanie 4.1: Uruchomienie testów po refaktoryzacji DI
* **Akcja:** Uruchom `pytest`.
* **Cel:** Upewnij się, że zmiana sygnatur konstruktorów w Fazie 1 nie zepsuła istniejących testów (będą wymagały drobnych poprawek w `conftest.py` lub w samych testach, aby przekazywać mocki repozytoriów zamiast poola).

### Zadanie 4.2: Manualny test Quickstart
* **Akcja:** Uruchom `./scripts/quickstart.sh` w czystym środowisku.
* **Weryfikacja:** Czy klucze API są ukryte podczas wpisywania? Czy `.env` ma poprawne uprawnienia?