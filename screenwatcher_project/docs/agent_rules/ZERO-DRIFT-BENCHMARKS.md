📄 4. ZERO-DRIFT-BENCHMARKS.md
Benchmarking Rules & Drift Detection Methodology

Version: 1.0

1. Cel dokumentu

Dokument opisuje, jak wykrywać i zapobiegać regresji jakości i wydajności w projektach stosujących Quality Pattern.

2. Zakres benchmarków

Każdy projekt powinien mieć co najmniej:

baseline (wersję odniesienia),

zestaw benchmarków,

mechanizm porównania,

progi akceptacji (SLO).

3. Kategorie driftu
3.1. Drift wydajnościowy

czas wykonania testów,

czas działania funkcji/algorytmów,

latency API (p95/p99),

throughput.

3.2. Drift zasobów

zużycie pamięci,

footprint CPU/GPU,

I/O operations.

3.3. Drift jakości

liczba warningów,

błędy lintera,

flaky tests,

naruszenia bezpieczeństwa.

3.4. Drift semantic/behavioral

Zmiany zachowania API, ale testy nadal przechodzą (bardzo groźne).
Wykrywamy przez:

contract tests,

golden files,

snapshot tests.

4. Jak obliczać drift?
4.1. Przykład metody:

Drift = (nowa_metryka - baseline) / baseline * 100%

Przykład:

baseline: 120ms

nowa wersja: 135ms

drift = (135 - 120) / 120 * 100% = 12.5%
→ przekroczony próg 10% → CI blokuje merge.

5. Przykładowe progi (SLO)
Moduły krytyczne:

czas testów: ≤ 5%

pamięć: ≤ 5%

logi WARNING: 0

drift semantyczny: 0

Moduły niekrytyczne:

czas testów: ≤ 15%

pamięć: ≤ 10%

warningi: 0 (ciągle obowiązuje Zero Warnings)

6. Benchmark tools

W zależności od języka:

Python: pytest-benchmark, perf, tracemalloc, memory-profiler

JS: autocannon, lighthouse, node:perf_hooks

PHP: phpbench, xhprof

Go: built-in testing benchmarks

Java: JMH

7. Raportowanie

Każdy commit do main powinien generować:

wykres trendu,

raport baseline.json,

raport current.json,

wynik porównania.

8. Drift Review

W przypadku przekroczenia progów:

PR jest blokowany,

tworzony jest ticket,

przydzielany odpowiedzialny maintainer.

9. Rozszerzenie: Adaptive SLO

Możesz zmieniać progi dynamicznie, jeśli projekt rośnie.
Np. enlarge threshold for non-critical modules.