# 🎯 Plan "Mądrego Montażu" (Smart Assembly) - Dreamsoft Pro 2.0
**Status:** Inicjalizacja Fazy 3 (Assembly & Validation)
**Data:** 2026-03-02 (Sesja Wieczorna)

## 🏗️ 1. Konsolidacja Symboli (The Final Stitching) - PRIORYTET 1
*   **Cel:** Połączyć 153 pliki `*.symbols_raw.json` (pobrane z Node 1) w ostateczne mapy `master_symbols.json`.
*   **Zadanie:** Uruchomić `SymbolStitcher.py` na laptopie. Usunąć duplikaty, zunifikować nazewnictwo metod i typów.

## 🗺️ 2. Mapa Kolejności Montażu (Bottom-Up Strategy)
*   **Cel:** Wyznaczyć kolejność uruchamiania serwisów na podstawie Grafu Zależności.
*   **Zadanie:** Wyciągnąć z Node 1 (tabela `knowledge_graph_edges`) listę importów i wykonać sortowanie topologiczne. Najpierw serwisy "liście" (np. `TaxService`), na końcu Giganci (`CalcCtrl`).

## 🛠️ 3. Inteligentny Import-Fixer
*   **Cel:** Naprawić "ślepe" importy w 760 plikach TSX.
*   **Zadanie:** Automat musi zamienić `import { ... } from '@/lib/api'` na realne ścieżki do zmodernizowanych plików w `src/services/`.

## 🪞 4. Piaskownica Lustrzana (The Mirror Sandbox)
*   **Cel:** Udowodnić parzystość zgodnie z ISO 42001.
*   **Zadanie:** Konfiguracja `docker-compose` do równoległego uruchomienia:
    *   Legacy (AngularJS): port 8081
    *   Candidate (Next.js): port 3005
*   **Validation:** Uruchomienie `UIRunner` (Playwright) do automatycznych testów porównawczych.

## 🧪 5. Generator Testów Parzystości (Vitest Factory)
*   **Cel:** Automatyczne testy jednostkowe dla 1278 serwisów.
*   **Zadanie:** Dla każdej metody w `master_symbols.json` wygenerować test `vitest`, który sprawdza zgodność danych wejściowych/wyjściowych z oryginałem.

---
**Materiały gotowe na laptopie:**
- Fundament Next.js 14 (Zustand, React Query, Vitest).
- 1278 serwisów TS w `src/services/`.
- 760 plików TSX w `src/components/`.
- 153 surowe pliki symboli w `src/components/`.

**Zadania działające w tle na Node 1:**
- Kontynuacja ekstrakcji symboli ( scripts.js ).
- Budowanie Grafu Zależności ( Turbo Mode ).
