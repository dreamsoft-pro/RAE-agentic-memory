# RAE System 3.4: Adaptacyjny Determinizm (Adaptive Determinism)
## Cel: Zwiększenie elastyczności Bandita bez utraty audytowalności oraz modernizacja warstwy wektorowej.

### 1. Problem (Context Drift & Model Quality)
- **Bandit:** Obecny System 3.3 zakłada statyczny świat. Przy zmianie charakteru danych (np. logi -> relacje handlowe) inercja blokuje adaptację.
- **Model:** Używany `all-MiniLM-L6-v2` jest szybki, ale przestarzały. `nomic-embed-text-v1.5` oferuje lepszą jakość (Matryoshka Embedding), ale wymaga obsługi prefixów (`search_query:`, `search_document:`).
- **Benchmark:** Test 100k wykazał stabilność infrastruktury, ale błędy w ocenie (MRR ~0.02) przez niedopasowanie ID/Modelu.

### 2. Rozwiązanie Matematyczne: Sliding Window UCB + Change Detection

#### A. Sliding Window UCB (SW-UCB)
- Sumowanie nagród tylko w oknie ostatnich $N$ zdarzeń (np. $N=100$).
- Wzór: $Q_t(a) = \frac{1}{N_t(a)} \sum_{k=t-N}^t r_k$
- System "zapomina" stare sukcesy, co pozwala na szybką adaptację.

#### B. Detektor Zmiany (CUSUM)
- Monitorowanie średniego MRR.
- Spadek poniżej progu (3 sigma) -> Reset statystyk okna (Change Point).
- Pełne logowanie zdarzeń (Audit Log).

### 3. Modernizacja Wektorowa (ONNX + Nomic)
- Wymiana `all-MiniLM-L6-v2` na `nomic-embed-text-v1.5.onnx`.
- Implementacja obsługi prefixów w `NativeEmbeddingProvider`.
- Obsługa zmiennej długości wektorów (Matryoshka) dla optymalizacji pamięci.

### 4. Harmonogram (Następna Sesja)
1.  **Bandit Upgrade:** Implementacja `SlidingWindowArm` i logiki wykrywania dryfu w `MathLayerController`.
2.  **ONNX Upgrade:** Pobranie i integracja modelu `nomic-embed-text-v1.5` (wymaga `tokenizers` z obsługą `bert-base-uncased` lub dedykowanego tokenizera).
3.  **Naprawa Benchmarku:** Ujednolicenie generowania ID w `run_benchmark.py` i `industrial_ultra.yaml`, aby MRR odzwierciedlał rzeczywistą jakość (która wg logów `DEBUG RESULTS` jest wysoka).
4.  **Test 3.4:** Uruchomienie scenariusza `industrial_mixed` (zmiana typu danych w locie) w celu weryfikacji adaptacji Bandita.

### 5. Wynik Biznesowy
System "Żywy", reagujący na zmiany kontekstu w czasie rzeczywistym, z nowoczesną warstwą semantyczną, gotowy na produkcyjne wdrożenie w środowiskach o zmiennej charakterystyce danych.