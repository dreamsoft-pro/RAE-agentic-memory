# Plan Kolejnej Sesji: Optymalizacja Wyszukiwania RAE-Windows

## Cel Główny
Podniesienie precyzji wyszukiwania w wersji Lite do poziomu Enterprise poprzez wymianę mechanizmu `LIKE` na natywne rozwiązanie **SQLite FTS5**.

## Zadania Techniczne

### 1. Migracja na FTS5 (Full-Text Search)
- **Aktualizacja Schematu**: Dodanie wirtualnej tabeli FTS5 w `SQLiteStorage`.
- **Indeksowanie**: Automatyczna synchronizacja tabeli `memories` z indeksem FTS5.
- **Optymalizacja zapytań**: Wykorzystanie operatora `MATCH` zamiast `LIKE` w metodzie `search_full_text`.

### 2. Kalibracja Hybrydowa (Rank Fusion)
- **Dostrojenie wag**: Zwiększenie priorytetu dopasowań tekstowych (FTS) dla krótkich zapytań (1-2 słowa).
- **Testy precyzji**: Weryfikacja wyszukiwania słów kluczowych takich jak "oskarżony", "dieta", "Erasmus" w dokumentach PDF.

### 3. Parser i Ingest
- **Parser OneNote**: Przygotowanie fundamentów pod import danych z OneNote (zgodnie z koncepcją Marcela).
- **Ulepszony Chunking**: Dodanie opcjonalnego podziału semantycznego (opartego na embeddingach zdań) dla bardzo długich sekcji.

### 4. Integracja z RAE-Mesh
- **Multi-tenancy**: Przygotowanie mechanizmu zmiany `tenant_id` w locie z poziomu GUI, aby umożliwić logiczne separowanie i późniejsze łączenie pamięci różnych użytkowników.

---
**Status:** Gotowe do wdrożenia w następnej sesji.
