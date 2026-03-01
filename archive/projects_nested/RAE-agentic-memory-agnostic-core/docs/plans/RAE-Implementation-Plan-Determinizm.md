# Plan Wdrożenia: Silicon Oracle - Deterministyczny Architektura Pamięci RAE (System 87.0)

## 🎯 Cel Strategiczny
Osiągnięcie wskaźnika **MRR (Mean Reciprocal Rank) = 1.0** we wszystkich benchmarkach przemysłowych poprzez eliminację stochastyczności, wprowadzenie rygorystycznego determinizmu matematycznego oraz audytowalnej proweniencji (Merkle-DAG).

---

## 🏗️ Faza 1: Fundamenty Deterministycznego Storage'u (The "Arena")
**Cel:** Eliminacja wpływu niedeterminizmu sprzętowego (FPU) i fragmentacji pamięci.

1.  **Implementacja Contiguous Memory Arenas:**
    *   Refaktoryzacja `InMemoryStorage` w `rae-core/rae_core/adapters/memory/storage.py`.
    *   Wykorzystanie `numpy.ndarray` (jeśli dostępny) lub `bytearray` do przechowywania wektorów w ciągłych blokach.
    *   Zastąpienie raw-pointers (referencji Pythonowych) indeksowaniem opartym na offsetach (`uint32`).
2.  **Kwantyzacja Stałoprzecinkowa (Fixed-Point):**
    *   Wdrożenie `QuantizationService` do transformacji wektorów `float32` -> `int32` (mnożnik $2^{32}$).
    *   Wszystkie obliczenia podobieństwa (Cosine/Dot) muszą używać wyłącznie arytmetyki całkowitoliczbowej.
3.  **Wirtualny Zegar (Deterministic Clock):**
    *   Wprowadzenie `IDeterministicClock` do zarządzania czasem w testach i benchmarkach (zamiast `datetime.now()`).

---

## 🔍 Faza 2: Ortogonalne Partycjonowanie Wyszukiwania (The "Scalpel")
**Cel:** Redukcja szumu semantycznego poprzez bezwzględne filtry ontologiczne.

1.  **FKS Perfect Hashing:**
    *   Implementacja algorytmu Fredman-Knot-Szemerédi dla kluczowych identyfikatorów (agent_id, project_id, tags).
    *   Gwarancja dostępu $O(1)$ bez kolizji dla "krytycznych trafień".
2.  **Filtry Blooma dla Tagów:**
    *   Dodanie bitowego filtra Blooma do każdego artefaktu pamięci.
    *   Błyskawiczne odrzucanie kandydatów niespełniających rygorystycznych kryteriów tagowych przed uruchomieniem wektorowego silnika matematycznego.
3.  **Logika Tie-Breakingu:**
    *   W przypadku identycznych wyników podobieństwa, wymuszenie determinizmu poprzez sortowanie po skrócie kryptograficznym (Hash) artefaktu.

---

## 🔄 Faza 3: Deterministyczna Konsolidacja i Proweniencja (The "Chain")
**Cel:** Pełna odtwarzalność cyklu życia wspomnień i ścieżek wnioskowania.

1.  **Maszyna Stanów Konsolidacji (FSM):**
    *   Przeniesienie logiki z `rae-core/rae_core/services/consolidation.py` do formalnej FSM.
    *   Stany: `WORKING` -> `EPISODIC` -> `SEMANTIC_PENDING` -> `SEMANTIC`.
    *   Przejścia sterowane wyłącznie przez parametryczne równania progowe i bayesowskie aktualizacje wag.
2.  **Struktura Merkle-DAG:**
    *   Implementacja `Hash(S_n) = SHA256(Data || Hash(Sources))` dla każdego węzła semantycznego.
    *   Zapewnienie, że każda odpowiedź z pamięci zawiera weryfikowalny łańcuch dowodowy (Provenance Path).
3.  **Bayesowskie Aktualizacje Wag:**
    *   Dynamiczne przeliczanie zaufania do faktów na podstawie wzoru Bayesa przy każdej próbie potwierdzenia (nowy epizod).

---

## 🧪 Faza 4: Benchmarki Antagonistyczne i Weryfikacja
**Cel:** Matematyczny dowód skuteczności Systemu 87.0.

1.  **Zestaw "Silicon Oracle 1M":**
    *   Stworzenie benchmarku z $10^6$ semantycznie zbliżonych dystraktorów.
    *   Weryfikacja, czy filtry ontologiczne i FKS utrzymują $MRR=1$ przy ekstremalnym szumie.
2.  **Testy Bit-to-Bit:**
    *   Weryfikacja, czy identyczny stan wejściowy generuje identyczny stan binarny pamięci (dzięki Arenas i Fixed-Point).
3.  **Metryka Provenance Accuracy (PA):**
    *   Wprowadzenie PA jako obowiązkowego KPI obok MRR.

---

## 📅 Harmonogram Wdrożenia (Kamienie Milowe)
*   **M1 (F1):** Stabilny Core In-Memory (Areny + Kwantyzacja).
*   **M2 (F2):** Integracja FKS i filtrów Blooma w `HybridSearchEngine`.
*   **M3 (F3):** Wdrożenie Merkle-DAG i FSM Konsolidacji.
*   **M4 (F4):** Certyfikacja Silicon Oracle (MRR=1.0 na 100k+).

---
*Plan opracowany na podstawie dokumentacji RAE-poprawa-determinizmu.txt oraz założeń branchu perf-optimize-in-memory-storage.*
