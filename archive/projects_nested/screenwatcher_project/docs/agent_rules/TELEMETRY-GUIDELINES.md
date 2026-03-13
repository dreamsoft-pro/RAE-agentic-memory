📄 TELEMETRY-GUIDELINES.md
Unified Telemetry, Observability & Measurement Rules for Software Projects

Version: 1.0

1. Cel dokumentu

Dokument definiuje zasady telemetrii, obserwowalności i pomiarów, które mają obowiązywać w każdym projekcie korzystającym z Quality Pattern.

Celem jest zapewnienie:

pełnej obserwowalności dla programistów,

danych badawczych dla naukowców,

wskaźników procesowych dla przemysłu,

audytowalności i zgodności dla administracji publicznej.

Telemetria jest obowiązkowa we wszystkich miejscach, które:

są źródłem kosztu,

są źródłem ryzyka,

są źródłem złożoności,

mogą ulec regresji (Zero Drift),

są istotne dla użytkownika końcowego.

2. Podstawowe zasady telemetry
2.1. Wszystko, co istotne, musi być mierzone

Zasada nadrzędna:

Jeśli coś jest ważne, musi mieć telemetrię.

Dotyczy to:

API,

algorytmów,

warstwy biznesowej,

operacji I/O,

pracy z danymi,

komponentów UI (jeśli to projekt frontendowy),

operacji asynchronicznych.

2.2. Telemetria musi być jednolita

Wszystkie projekty używają tego samego modelu:

Traces – przepływ wykonania, analiza pętli i opóźnień, korelacja błędów.

Metrics – stałe pomiary (czas, pamięć, throughput, task count).

Logs – informacja diagnostyczna, ale bez danych wrażliwych.

Formaty:

OTel (OpenTelemetry) – preferowany,

JSON dla eksportu,

Prometheus/OpenMetrics dla integracji z przemysłem.

2.3. Zero Sensitive Data in Telemetry

Logi, metryki i trace NIE mogą zawierać:

danych osobowych,

kluczy API,

haseł,

tokenów JWT,

danych medycznych,

danych klasyfikowanych.

3. Gdzie dodawać telemetrię?
3.1. Dla developerów

czas wykonania funkcji,

liczba wywołań,

wyjątki,

retry/reconnect,

zużycie pamięci,

miejsca błędów logicznych.

3.2. Dla naukowców

metryki algorytmów (czas, iteracje, złożoność, Vram/Ram),

wyniki eksperymentów,

parametry wejściowe/wyjściowe algorytmu,

dane porównawcze baseline → nowa wersja.

3.3. Dla przemysłu

czas odpowiedzi API (p95/p99),

pojemność systemu (load),

szybkość przetwarzania (throughput),

awaryjność,

retry rate,

metryki procesowe definowane przez SLA.

3.4. Dla administracji / public sector

pełna audytowalność: trace ID dla każdego żądania,

czyste logi: INFO/ERROR bez warningów,

metryki zgodności (np. użycie AI, decyzje algorytmiczne),

statystyki ruchu i stabilności.

4. Standard telemetry points (TPL – Telemetry Placement List)

Każdy projekt powinien dodać telemetrię w:

4.1. API / Endpoints

liczba requestów,

latency p50/p95/p99,

status codes,

wyjątki,

error rate.

4.2. Warstwa biznesowa

kluczowe funkcje,

funkcje o złożoności O(n²) i wyższej,

elementy związane z kosztami.

4.3. Warstwa algorytmiczna

iteracje,

czas per krok,

zużycie pamięci per etap,

degradacja jakości vs baseline.

4.4. Warstwa danych

czas zapytań DB,

liczba zapytań,

cache hits/misses.

4.5. Asynchroniczne taski

czas w kolejce,

czas wykonania,

porażki, retry.

5. Telemetry & Zero Drift

Telemetria musi zasilać:

baseline,

porównanie wersji,

analizę driftu.

Metryki OTel są źródłem prawdy dla ZERO DRIFT.

6. Telemetry & Security

wszystkie zdarzenia logowania systemowego muszą mieć trace ID,

błędy bezpieczeństwa muszą być logowane na poziomie ERROR,

trace musi być możliwy do skorelowania z testami.

7. Telemetry Adoption Levels
Poziom	Opis
L0	brak telemetrii
L1	podstawowe metryki (czas, błędy)
L2	pełne OTel traces + metrics
L3	integracja z Zero Drift
L4	telemetria dla nauki + przemysłu + administracji
L5	telemetry-driven optimization (AI)

Zalecane minimum: L2 → L3.
! WAŻNE - w praktyce stosować L5 tam, gdzie to możliwe.