Oto szczegółowy plan techniczny podzielony na trzy filary: Jakość Danych (Entity Resolution), Głębia Wnioskowania (Wisdom) oraz Optymalizacja Ekonomiczna (Cost/Speed).

FILAR 1: Eliminacja Duplikatów (Entity Resolution & Canonicalization)
Problem: System traktuje "Jan Kowalski", "Jan K." i "J. Kowalski" jako trzy osobne węzły. Rozwiązanie: Wdrożenie wieloetapowego potoku deduplikacji działającego w tle (background job).

Plan Implementacji:

Etap Normalizacji (Pre-processing):

Zanim encja trafi do bazy, przepuść ją przez prosty filtr tekstowy:

Lowercase, usunięcie znaków specjalnych.

Lemmatyzacja (sprowadzenie do formy podstawowej, np. "psami" -> "pies").

Koszt: Zerowy (biblioteki Python: spacy lub nltk).

Klasteryzacja Semantyczna (Vector-based Clustering):

Dla każdej nazwy węzła (Node Name) generuj mały embedding (np. modelem all-MiniLM-L6-v2 – jest darmowy, szybki i lokalny).

Użyj algorytmu klasteryzacji (np. DBSCAN lub Agglomerative Clustering), aby grupować węzły, które są semantycznie bliskie (np. odległość cosinusowa > 0.90).

Wykryjesz wtedy, że "Apple Inc." i "Apple Company" to to samo.

Agent "Konserwator" (The Janitor Agent):

Stwórz zadanie Celery uruchamiane np. raz na godzinę.

Prompt dla LLM: Podajesz mu listę kandydatów do scalenia wykrytą w kroku 2.

Zadanie: "Decyduj: czy 'Java' (wyspa) i 'Java' (język) to to samo? Jeśli tak -> Scal. Jeśli nie -> Oznacz jako różne".

To radykalnie zmniejsza liczbę zapytań do LLM – pytasz tylko o niejasne przypadki.

FILAR 2: Poprawa "Mądrości" (Od Faktów do Wniosków)
Problem: Obecnie graf to "Worek Faktów" (Memory Dump). Brakuje syntezy. Rozwiązanie: Wdrożenie Hierarchicznego GraphRAG (inspirowanego badaniami Microsoftu).

Plan Implementacji:

Wykrywanie Społeczności (Community Detection):

Użyj algorytmu Leiden lub Louvain na grafie wiedzy. Pozwoli to wykryć "skupiska" tematów (np. klaster węzłów związanych z "Projektem X", klaster węzłów "Preferencje Użytkownika").

Synteza Poziomu Wyższego (Summarization):

Zamiast pytać o poszczególne krawędzie, LLM generuje opis klastra.

Przykład: Zamiast pamiętać 50 faktów o tym, co lubisz jeść, system tworzy jeden "Węzeł Meta": "Użytkownik preferuje kuchnię azjatycką, unika nabiału i dba o niski indeks glikemiczny".

To jest ta "mądrość" – generalizacja na podstawie detali.

Refleksja Czasowa (Temporal Wisdom):

Wykorzystaj temporal_graph.py. Jeśli system widzi, że w każdy piątek pytasz o "status report", tworzy regułę proaktywną.

Kod: Dodanie atrybutu frequency i last_accessed do krawędzi grafu. Wygaszanie (decay) starych, nieistotnych wspomnień.

FILAR 3: Radykalna Optymalizacja Kosztów (Model Routing)
Problem: Używanie GPT-4/Claude 3.5 Opus do wszystkiego to palenie pieniędzmi. Rozwiązanie: Architektura Kaskadowa (Tiered Architecture).

Plan Implementacji:

Model "Robotnik" (Extraction Model):

Do prostego wyciągania encji z tekstu ("Kto? Co? Kiedy?") NIE używaj modeli flagowych.

Rekomendacja: Użyj Gemini 1.5 Flash (bardzo tani, ogromne okno kontekstowe) lub GPT-4o-mini.

Opcja darmowa (Radykalna): Użyj lokalnego modelu przez Ollama (np. Llama-3-8B-Instruct z wymuszonym formatem JSON). Jakość wystarczająca w 90% przypadków ekstrakcji.

Model "Mędrzec" (Reflection Model):

Drogiego modelu (Claude 3.5 Sonnet / GPT-4o) używaj TYLKO do etapu syntezy (Filar 2 - tworzenie podsumowań klastrów) oraz do pisania finalnej odpowiedzi dla użytkownika.

Proporcja zapytań powinna wynosić 10:1 (10 ekstrakcji tanim modelem na 1 refleksję drogim).

Agresywne Filtrowanie (The Gatekeeper):

Przed uruchomieniem pipeline'u RAE, mały model (lub nawet klasyfikator BERT) ocenia: "Czy to zdanie zawiera nowe fakty?".

Jeśli użytkownik pisze "Dzięki, super!" -> Ignoruj. Koszt 0$.

Jeśli użytkownik pisze "Mój pesel to..." -> Szyfruj i zapamiętaj.

PLAN DZIAŁANIA (Roadmap w pliku .md)
Zaktualizujmy Twój PLAN_NAPRAWCZY.md o te konkretne techniki.

Markdown

# PLAN OPTYMALIZACJI RAE v2.0 (Deep Wisdom & Low Cost)

## FAZA 1: Cięcie Kosztów (Tydzień 1)
- [ ] **Wdrożenie Model Routera:**
    - Zmiana w `config.py`: Dodanie `EXTRACTION_MODEL` (np. gpt-4o-mini/gemini-flash) i `SYNTHESIS_MODEL` (gpt-4o).
    - Refaktoring `graph_extraction.py`: Użycie taniego modelu do parsowania tekstu na JSON.
- [ ] **Bramka wejściowa (Gatekeeper):**
    - Dodanie prostego promptu sprawdzającego `is_factual_content(text) -> bool` przed uruchomieniem ciężkiej maszyny RAE.

## FAZA 2: Entity Resolution (Tydzień 2)
- [ ] **Normalizacja:** Zaimplementowanie funkcji czyszczących w `GraphExtractionService`.
- [ ] **Klasteryzacja:** Dodanie serwisu w tle (`cron`), który pobiera wszystkie węzły, liczy ich embeddingi (lokalnie!) i scala te o podobieństwie > 0.95 automatycznie.
- [ ] **Interfejs konfliktów:** (Opcjonalnie) Jeśli podobieństwo jest między 0.85 a 0.95, zapytaj taniego LLM o decyzję.

## FAZA 3: Implementacja "Mądrości" (Tydzień 3)
- [ ] **Community Summaries:**
    - Użycie biblioteki `networkx` lub procedur w Neo4j/Memgraph do wykrycia klastrów.
    - Generowanie opisów klastrów i zapisywanie ich jako "Super-Węzły" w bazie wektorowej.
- [ ] **Wyszukiwanie Hybrydowe:**
    - Przy pytaniu użytkownika, przeszukujemy najpierw "Super-Węzły" (kontekst ogólny), a dopiero potem wchodzimy w detale grafu.
