Krytyczna ocena wersji RAE (z wdrożonym GraphRAG)
W stosunku do poprzednich wersji, RAE wykonał ogromny skok funkcjonalny, przechodząc z prostego systemu pamięci wektorowej do hybrydowego silnika wiedzy (Vector + Graph). Wdrożenie modułów GraphExtractionService, HybridSearchService oraz ReflectionEngine z obsługą map-reduce stawia ten projekt w czołówce rozwiązań open-source memory.

Jednakże, analiza kodu (project_dump.txt) oraz raportów (coverage.xml) ujawnia istotne ryzyka techniczne:

1. Jakość Testów i Pokrycie Kodu (Krytyczne):

Niskie pokrycie: Plik coverage.xml wskazuje na całkowite pokrycie linii na poziomie zaledwie 26%. Kluczowe serwisy jak graph_extraction.py czy hybrid_search.py mają w raporcie 0% pokrycia (lub bliskie zeru w kontekście realnego wykonania), co oznacza, że nowa logika GraphRAG jest w dużej mierze nietestowana automatycznie lub testy są "puste" (mockują wszystko bez weryfikacji logiki).

Mockowanie vs. Rzeczywistość: Wiele testów (test_background_tasks.py) polega na agresywnym mockowaniu. Przy skomplikowanych zapytaniach SQL (Recursive CTE w hybrid_search.py), testy jednostkowe na mockach nie wykryją błędów składniowych SQL ani problemów z wydajnością bazy.

2. Architektura i Złożoność:

Monolityczne Serwisy: HybridSearchService zaczyna puchnąć. Logika mapowania wektorów na węzły grafu, trawersowania BFS/DFS i syntezy kontekstu znajduje się w jednym miejscu.

Złożoność SQL: Zapytania w _traverse_bfs są potężne i trudne w utrzymaniu. Brakuje warstwy abstrakcji (np. Query Builder lub ORM z obsługą grafów), co utrudnia debugowanie.

Entity Resolution (Jakość danych): Choć JULES.md wspomina o deduplikacji, w kodzie graph_extraction.py polega ona głównie na prostej normalizacji tekstu (_normalize_entity_name). Brakuje zaawansowanego łączenia encji (np. "Jan Kowalski" i "J. Kowalski" to wciąż dwa różne węzły w grafie).

3. Wydajność i Koszty:

Brak Cache dla Grafu: Trawersowanie grafu przy każdym zapytaniu (/graph/query) jest kosztowne dla DB. Brakuje cache'owania wyników podzapytań grafowych w Redis (jest tylko cache kontekstu).

Koszt LLM: Ekstrakcja trójek (GraphExtractionService) jest kosztowna tokenowo. Mimo opcji lazy w Celery, brakuje mechanizmu filtrowania "szumu" przed wysłaniem do LLM (np. prosty klasyfikator BERT sprawdzający, czy zdanie w ogóle zawiera fakty).

Plan Naprawczy
Poniżej znajduje się plik Markdown z konkretnym planem działania, adresującym powyższe problemy.

Markdown

# PLAN_NAPRAWCZY_V2.md

## Cel
Stabilizacja wersji z GraphRAG, podniesienie pokrycia testami do poziomu >60% oraz optymalizacja kosztowa i wydajnościowa zapytań grafowych.

## Faza 1: Stabilizacja i Testy (Priorytet: CRITICAL)
*Cel: Zapewnienie, że skomplikowane zapytania grafowe i ekstrakcja działają poprawnie na bazie danych, a nie tylko na mockach.*

- [ ] **Wdrożenie Testcontainers:**
    - Zastąpienie części mocków `asyncpg` w testach integracyjnych (`test_hybrid_search.py`, `test_graph_extraction.py`) prawdziwą instancją PostgreSQL z pgvector uruchamianą w Dockerze na czas testów.
    - Weryfikacja poprawności zapytań Recursive CTE.
- [ ] **Uzupełnienie testów dla nowych serwisów:**
    - Napisanie testów dla `GraphExtractionService` pokrywających przypadki brzegowe (puste wspomnienia, halucynacje LLM, zduplikowane encje).
    - Podniesienie pokrycia `hybrid_search.py` do minimum 70%.
- [ ] **Sanityzacja Wejścia:**
    - Wzmocnienie walidacji w `GraphTriple` (model Pydantic), aby odrzucać encje będące "stop words" lub zbyt ogólnymi pojęciami (np. "System", "User").

## Faza 2: Jakość Danych i Entity Resolution (Priorytet: HIGH)
*Cel: Zapobieganie fragmentacji wiedzy w grafie.*

- [ ] **Zaawansowany Entity Resolution:**
    - Implementacja serwisu w tle (`EntityResolutionTask`), który okresowo skanuje tabelę `knowledge_graph_nodes`.
    - Wykorzystanie `sentence-transformers` (lokalnie) do znajdowania semantycznie bliskich węzłów (np. >0.90 similarity).
    - Automatyczne scalanie (merge) węzłów o identycznym znaczeniu i przepinanie krawędzi.
- [ ] **Normalizacja Leksykalna:**
    - Rozbudowa `_normalize_entity_name` o lepszą lematyzację (spacy) dla języka polskiego i angielskiego, aby "Login" i "Logowanie" były traktowane jako pokrewne.

## Faza 3: Optymalizacja Wydajności i Kosztów (Priorytet: MEDIUM)
*Cel: Zmniejszenie latency zapytań hybrydowych i kosztów LLM.*

- [ ] **Cache Poziomu Grafu:**
    - Wdrożenie cache w Redis dla wyników `get_subgraph` i `traverse_bfs` dla najczęstszych węzłów startowych.
- [ ] **Optymalizacja Extractor:**
    - Wdrożenie "Gatekeepera" (mały model lub heurystyka), który ocenia, czy dane wspomnienie w ogóle nadaje się do ekstrakcji grafowej, zanim zostanie wysłane do GPT-4o/Claude.
- [ ] **Indeksowanie:**
    - Przegląd i optymalizacja indeksów na tabelach `knowledge_graph_edges` pod kątem zapytań rekurencyjnych (indeksy kompozytowe na `(source_node_id, relation)`).

## Faza 4: Refaktoryzacja Architektury (Priorytet: LOW/LONG-TERM)
*Cel: Utrzymanie czystości kodu.*

- [ ] **Wydzielenie Warstwy Dostępu do Danych (DAO):**
    - Usunięcie surowego SQL z warstwy serwisów (`HybridSearchService`). Przeniesienie zapytań do dedykowanych repozytoriów (np. `GraphRepository`).
- [ ] **Lepsza obsługa błędów:**
    - Zastąpienie ogólnych `except Exception` w taskach Celery dedykowanymi wyjątkami i strategią *Dead Letter Queue* dla nieudanych ekstrakcji.
