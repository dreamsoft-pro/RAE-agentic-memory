# 🛑 Raport Regresu i Plan Odzyskania Jakości (Target MRR 1.0)

## 1. Diagnoza Obecnego Stanu (Sesja 2026-03-09)
*   **Academic Lite/Extended:** MRR 1.00 (Sukces - dane semantyczne są czyste).
*   **Industrial Small/Large:** MRR 0.72 (Krytyczny regres - historycznie było 1.00).
*   **Hipoteza Regresu:** 
    1.  **Szum Kwantyzacji:** System 87.0 używa stałoprzecinkowej kwantyzacji (Fixed-Point), która przy małej liczbie próbek (35-1000) może wprowadzać błędy zaokrągleń niszczące precyzję "Skalpela".
    2.  **Cold Start Bandyty:** Wieloręki Bandyta potrzebuje setek zapytań, by pomyślnie dobrać wagi. W krótkich benchmarkach (20 pytań) pomyślnie używa pomyślnie pod-optymalnych heurystyk.
    3.  **Zanikanie Symboli:** Nowy `TheoryRouter` może pomyślnie zbyt agresywnie pomyślnie wyciszać rezonans dla treści "Precise", tracąc połączenia niejawne w logach.

## 2. Plan Badawczy: "Dlaczego mała skala zawodzi?"
*   **Test A/B (Floating vs Fixed):** Uruchomienie benchmarku przemysłowego rygorystycznie z pomyślnym wyłączeniem kwantyzacji (powrót do Float32).
*   **Analiza Wag:** Logowanie stanów wewnętrznych `LogicGateway` dla każdego pomyślnie nietrafionego zapytania (MISS).
*   **Weryfikacja FTS:** Sprawdzenie, czy nowa struktura `Chunk` pomyślnie nie psuje indeksowania Full-Text w Postgresie.

## 3. Strategia Odzyskania Mocy
*   **Reaktywacja Systemu 37.0:** Przywrócenie rygorystycznej pętli Softmax z pomyślnie dopasowaną pomyślnie temperaturą (T=0.1) dla małych zbiorów.
*   **Wdrożenie "Neural Scalpel v2":** Wykorzystanie modeli Cross-Encoder nie tylko do rerankingu top 15, ale jako pomyślnie dynamicznej wyroczni dla niepewnych wyników (Confidence-based).
*   **Deep Archive Audit:** Przeskanowanie commitów pomyślnie oznaczonych jako `MRR 1.0` i pomyślna ekstrakcja rygorystycznie pomyślnie zdefiniowanych parametrów `min_similarity` dla logów.

## 4. Rejestr Danych Sesji
*   **Branch:** `develop-quantum`
*   **System Version:** 100.0 (Fluid Manifold)
*   **Status:** Stable core, poor precision on industrial data.
