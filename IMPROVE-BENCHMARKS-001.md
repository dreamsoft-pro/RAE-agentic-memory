# RAE – Plan poprawy benchmarków pamięci i rozumowania

Ten dokument opisuje, jak z poziomu obecnych wyników:

- **LECT:** 100% episodic consistency (1,000 cycles)  
- **MMIT:** 99.4% isolation (3 leaks / 500 ops)  
- **GRDT:** depth 10, 58.3% coherence  
- **RST:** 62.5% consistency under noise (stable to 60%)  
- **MPEB:** 95.7% adaptation  
- **ORB:** 3/6 Pareto-optimal configs  

dojść do bardziej „pro” poziomu, bez naruszania stabilności systemu.

---

## 1. Cele ilościowe

| Benchmark | Stan obecny                         | Cel „pro”                         |
|-----------|-------------------------------------|-----------------------------------|
| LECT      | 100% (1,000 cykli)                 | Utrzymać 100%, rozszerzyć do 10k |
| MMIT      | 99.4% (3/500 leaków)               | ≥ 99.8% (≤ 1 leak / 500 ops)     |
| GRDT      | depth = 10, 58.3% coherence        | depth ≥ 12, ≥ 70% coherence      |
| RST       | 62.5% consistency, noise do 60%    | ≥ 75% consistency, noise do 70%  |
| MPEB      | 95.7% adaptation                   | ≥ 97% + brak regresji w LECT/MMIT|
| ORB       | 3/6 konfiguracji Pareto-optimal    | ≥ 5/6 konfiguracji Pareto-optimal|

Dodatkowo: utrzymanie **healthy services** (Postgres, Redis, Qdrant) w docelowych progach opóźnień.

---

## 2. LECT – utrzymanie 100% konsystencji epizodycznej

LECT już ma wynik **idealny**. Celem jest **utrzymanie jakości** przy większej skali.

### 2.1. Działania

- [ ] Zwiększyć liczbę cykli testowych z **1,000 → 10,000** w trybie nightly.
- [ ] Dodać wariant testów z:
  - [ ] Różnymi rozmiarami epizodów (mikro / średnie / długie sekwencje).
  - [ ] Różnymi typami eventów (dialog, task, system, meta).
- [ ] Wprowadzić **„LECT regression suite”**:
  - [ ] Zestaw kanonicznych historii, które muszą być zawsze odtwarzane 1:1.
  - [ ] Oznaczyć je jako krytyczne w CI (przerwanie pipeline przy regresji).
- [ ] Dodać metrykę:
  - [ ] `% driftu czasowego` (czy kolejność zdarzeń jest zachowana).
  - [ ] `% utraconych eventów` (should remain 0).

### 2.2. Warunek zaliczenia

- [ ] 10,000 cykli testowych LECT, 0 błędów, brak regresji w kolejnych 5 uruchomieniach CI.

---

## 3. MMIT – poprawa izolacji pamięci (99.4% → 99.8%+)

Celem jest redukcja leaków między:

- różnymi agentami,
- różnymi sesjami,
- różnymi warstwami pamięci.

### 3.1. Zmiany architektoniczne

- [ ] Wprowadzić **twardą separację namespace’ów**:
  - [ ] jawny `agent_id` + `session_id` w każdej operacji pamięci,
  - [ ] odseparowane klucze w Redis (prefiks per agent + session),
  - [ ] odseparowane kolekcje / payload tags w Qdrant.
- [ ] Dodać warstwę **„memory isolation guard”**:
  - [ ] Funkcje, które sprawdzają, czy wynik wyszukiwania:
    - nie zawiera obcych `agent_id`,
    - nie zawiera obcych `session_id`.
  - [ ] Logowanie każdej operacji oznaczonej jako potencjalny leak.

### 3.2. Zmiany w testach

- [ ] Rozszerzyć MMIT do np. **2,000 operacji** per run.
- [ ] Wprowadzić testy:
  - [ ] „agent A” i „agent B” z konfliktującymi epizodami – brak krzyżowego dostępu.
  - [ ] równoległe operacje (concurrency) z wysokim obciążeniem.
- [ ] Wprowadzić metrykę:
  - [ ] `leaks_per_1000_ops` (docelowo < 2).

### 3.3. Warunek zaliczenia

- [ ] ≤ 1 leak / 500 operacji w 10 kolejnych runach.  
- [ ] Brak leaków w testach z agresywną równoległością (przynajmniej 3 różne scenariusze).

---

## 4. GRDT – głębokość i spójność rozumowania

Chcemy:
- zwiększyć **maksymalną głębokość reasoning** (10 → 12+),
- podnieść **spójność** (58.3% → ≥ 70%).

### 4.1. Sterownik warstwy „math”

- [ ] Wyodrębnić **„reasoning controller”** jako osobny moduł:
  - [ ] z parametrami:
    - maksymalna głębokość,
    - dopuszczalny poziom niepewności,
    - „budget tokenów / krok”.
  - [ ] dodać heurystyki:
    - wcześniejsze ucinanie ścieżek ewidentnie sprzecznych,
    - nagradzanie spójności między warstwami pamięci (episodic/semantic/reflective).

### 4.2. Curriculum zadań reasoning

- [ ] Przygotować zestaw benchmarków:
  - [ ] proste łańcuchy przyczynowo-skutkowe (depth 3–5),
  - [ ] scenariusze planowania (depth 5–8),
  - [ ] złożone scenariusze wieloetapowe (depth 8–12).
- [ ] Dla każdego zadania:
  - [ ] zdefiniować **złoty standard** (idealny przebieg reasoning),
  - [ ] mierzyć:
    - **coherence score** (porównanie przebiegu vs wzorzec),
    - **deviation score** (liczba zbędnych kroków / sprzeczności).

### 4.3. Telemetria reasoning

- [ ] Logować:
  - [ ] liczbę kroków reasoning per zadanie,
  - [ ] punkty, w których reasoning „odjeżdża” od wzorca,
  - [ ] wpływ głębokości na koszty i czas.
- [ ] Na tej podstawie:
  - [ ] dostroić parametry kontrolera (np. różne profile: „strict”, „balanced”, „fast”).

### 4.4. Warunek zaliczenia

- [ ] Średnia spójność ≥ 70% w 3 kolejnych runach benchmarku.  
- [ ] Brak spadku LECT/MMIT w wyniku zmian w warstwie math.

---

## 5. RST – odporność na szum (62.5% → 75%+)

Celem jest:

- podniesienie stabilności odpowiedzi przy zakłóconych danych,
- zwiększenie tolerowanego poziomu szumu z 60% do 70%.

### 5.1. Pipeline szumu

- [ ] Zaimplementować moduł dodawania szumu:
  - [ ] losowe usuwanie fragmentów promptów,
  - [ ] semantyczne parafrazy,
  - [ ] wtrącenia mylących informacji.
- [ ] Testować 3 poziomy:
  - [ ] niski (20–30%),
  - [ ] średni (40–50%),
  - [ ] wysoki (60–70%).

### 5.2. Strategie obronne

- [ ] Dodać „noise-aware retrieval”:
  - [ ] zwiększenie wagi ostatnich wiarygodnych epizodów,
  - [ ] penalizacja sprzecznych wektorów w Qdrant.
- [ ] Dodać „sanity checks” przed reasoning:
  - [ ] wykrywanie oczywistych sprzeczności w wejściu,
  - [ ] fallback: dopytanie (jeśli w trybie interaktywnym) lub ostrożniejsza odpowiedź.

### 5.3. Warunek zaliczenia

- [ ] ≥ 75% stabilnych odpowiedzi przy szumie 60–70%.  
- [ ] Brak istotnego wzrostu błędów w testach bez szumu.

---

## 6. MPEB – adaptacja (95.7% → 97%+)

Chcemy wzmocnić adaptację bez rozbijania stabilności.

### 6.1. Multi-episode adaptation runs

- [ ] Projekt testów, gdzie:
  - [ ] system dostaje serię zadań z tą samą domeną, ale zmieniającymi się regułami,
  - [ ] mierzymy, jak szybko adaptuje się do nowych reguł.
- [ ] Dodać metryki:
  - [ ] liczba epizodów do pełnej adaptacji,
  - [ ] wpływ adaptacji na inne zadania (czy nie degraduje wcześniejszych umiejętności).

### 6.2. „Safe adaptation guard”

- [ ] Wprowadzić warstwę, która:
  - [ ] odróżnia „tymczasową adaptację” (sandbox) od „permanentnej zmiany”,
  - [ ] nie pozwala na nadpisanie kluczowych reguł bez wielokrotnej walidacji.

### 6.3. Warunek zaliczenia

- [ ] ≥ 97% adaptation score w 3 runach.  
- [ ] Brak regresji w LECT / MMIT po długich sekwencjach adaptacji.

---

## 7. ORB – więcej konfiguracji Pareto-optymalnych (3/6 → 5/6)

Chcemy znaleźć i utrwalić więcej konfiguracji:

- **tanie + szybkie**,
- **dokładne + stabilne**,
- **zbalansowane**.

### 7.1. Auto-tuner konfiguracji

- [ ] Zdefiniować przestrzeń parametrów:
  - [ ] rozmiar kontekstu,
  - [ ] strategia buforowania w Redis,
  - [ ] głębokość reasoning,
  - [ ] progi podobieństwa w Qdrant,
  - [ ] wagi warstw pamięci.
- [ ] Uruchomić:
  - [ ] grid search / random search,
  - [ ] opcjonalnie prosty Bayesian search.
- [ ] Dla każdej konfiguracji:
  - [ ] mierzyć: koszty, czas, jakość (benchmarki LECT/MMIT/GRDT/RST/MPEB).

### 7.2. Budowa frontu Pareto

- [ ] Zdefiniować:
  - [ ] cel „quality” (łączny score benchmarków),
  - [ ] cel „cost” (czas + tokeny),
  - [ ] cel „stability” (liczba regresji).
- [ ] Wyliczyć front Pareto i zapisać:
  - [ ] min. 5 konfiguracji w katalogu `profiles/` jako:
    - `profile_research.yaml`,
    - `profile_enterprise_safe.yaml`,
    - `profile_fast_dev.yaml`,
    - `profile_mobile_lite.yaml` (jeśli dotyczy),
    - `profile_balanced_default.yaml`.

### 7.3. Warunek zaliczenia

- [ ] ≥ 5/6 konfiguracji wchodzących do frontu Pareto.  
- [ ] Udokumentowane profile + opis użycia w README.

---

## 8. Telemetria i CI – spinanie wszystkiego w jeden system

### 8.1. Telemetria benchmarków

- [ ] Wysłać metryki do systemu telemetrycznego:
  - [ ] LECT/MMIT/GRDT/RST/MPEB/ORB w formie „time series”.
- [ ] Zbudować dashboard:
  - [ ] trendy wyników w czasie,
  - [ ] wykrywanie regresji (alerty).

### 8.2. CI / CD jako strażnik jakości

- [ ] Dodać „Benchmark Gate” do CI:
  - [ ] jeśli którykolwiek benchmark spada poniżej ustalonego progu:
    - CI czerwony,
    - blokada merge do `main`.
- [ ] Dodać job „nightly full benchmarks”:
  - [ ] pełny pakiet testów (dłuższe runy, większa liczba cykli),
  - [ ] archiwizacja wyników do analizy.

---

## 9. Harmonogram wdrożenia

Propozycja w ujęciu iteracyjnym (może być tygodniami lub sprintami):

### Iteracja 1 – Szybkie wygrane

- [ ] Rozszerzenie LECT do 10,000 cykli.  
- [ ] Namespace’y w pamięci (MMIT), podstawowy guard izolacji.  
- [ ] Telemetria dla wszystkich benchmarków.

### Iteracja 2 – Reasoning i noise

- [ ] Wyodrębnienie „reasoning controller” (GRDT).  
- [ ] Pipeline szumu + noise-aware retrieval (RST).  
- [ ] Pierwsza wersja auto-tunera konfiguracji (ORB).

### Iteracja 3 – Adaptacja i Pareto

- [ ] Multi-episode adaptation runs (MPEB).  
- [ ] Budowa profili `profiles/*.yaml` i frontu Pareto (ORB).  
- [ ] Spinanie wszystkiego z CI / Benchmark Gate.

---

## 10. Definicja „DONE” dla planu

Plan można uznać za zrealizowany, gdy:

- [ ] LECT stabilnie 100% na 10,000 cykli.  
- [ ] MMIT ≤ 1 leak / 500 ops w 10 runach.  
- [ ] GRDT: depth ≥ 12, coherence ≥ 70%.  
- [ ] RST: ≥ 75% consistency przy noise 60–70%.  
- [ ] MPEB: ≥ 97% adaptation bez regresji w innych benchmarkach.  
- [ ] ORB: ≥ 5/6 konfiguracji Pareto-optymalnych + opisane profile.  
- [ ] CI blokuje merge przy regresji benchmarków.  
- [ ] Telemetria i dashboard pozwalają śledzić trendy jakości w czasie.

