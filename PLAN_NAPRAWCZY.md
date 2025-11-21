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
