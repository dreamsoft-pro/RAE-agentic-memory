# RAE – Universal Ingest & Content-Type Control (UICTC)
## Deterministic • Auditable • Model-Agnostic • Domain-Independent • Scalable

> Cel: zbudować **uniwersalny** (cross-domain) pipeline ingestu, który:
> - rozpoznaje rodzaj treści na wejściu,
> - zapisuje tę wiedzę jako metadane (sygnaturę),
> - wpływa na chunking/kompresję/indeksowanie **bez** magicznych wag i progów,
> - umożliwia kontrolowany rozwój w czasie (evolvable, testowalny).

---

## 0) Założenia i granice

### MUST (twarde wymagania)
- **Deterministyczność**: te same dane → ta sama sygnatura → ten sam ingest.
- **Audytowalność**: dla każdego bloku danych da się odtworzyć: *dlaczego* został tak pocięty i opisany.
- **Agnostyczność modeli**: zmiana embedding provider (ONNX / różne modele) nie zmienia logiki rozpoznania typu treści.
- **Domenowa niezależność**: brak słowników dziedzinowych jako krytycznej zależności.
- **Skalowalność**: ingest działa na 2GB logów MES oraz na dokumentach prawnych/korpo i danych naukowych.

### SHOULD (ważne)
- Minimalny koszt obliczeniowy na wejściu (O(n) po tekście, bez ciężkich modeli).
- Kontrakty I/O dla każdego etapu.
- Możliwość wdrożenia do CI: testy regresji sygnatur + segmentacji.

### MUST NOT
- Brak stałych wag łączących sygnały.
- Brak ręcznie dobranych progów typu `0.3`, `0.7` itd. (dopuszczalne: percentyle, ogony rozkładów).
- Brak uczenia online na produkcyjnych danych (możliwe: statystyki rozkładowe do progów adaptacyjnych).

---

## 1) Dlaczego rozpoznanie rodzaju treści jest kluczowe

RAE musi działać dla:
- logów przemysłowych (MES, awarie, telemetria, mikroprzestoje),
- księgowości/logistyki/sprzedaży,
- medycznych danych do publikacji,
- korpo-instrukcji i procedur (Q&A proceduralne),
- danych do eksperymentów naukowych.

Różnią się one:
- strukturą (linie vs akapity vs formularze),
- gęstością liczb i identyfikatorów,
- rytmem czasu,
- poziomem formalizacji,
- wymaganiami na cytowalność i ślad źródeł.

**Ten sam chunking i te same heurystyki dla wszystkich domen → degradacja jakości.**

Dlatego potrzebujemy **sygnatury wejścia**, która w kontrolowany sposób wpływa na ingest.

---

## 2) Architektura: Universal Ingest Pipeline (5 etapów)

Pipeline ingestu jest kaskadowy i lekki:

1. **Normalize** (normalizacja i czyszczenie)
2. **Detect** (wyznaczenie sygnatury treści)
3. **Segment** (chunking zależny od sygnatury)
4. **Compress/Dedup** (redukcja redundancji – opcjonalnie, zależnie od sygnatury)
5. **Encode & Persist** (embedding + zapis do warstw pamięci + metadane)

### Zasada nadrzędna
Sygnatura **nie jest etykietą domeny** (“prawo”, “medycyna”).
Sygnatura opisuje **strukturę i niejednoznaczność**.

---

## 3) Warstwy „Detect”: 3-warstwowy UICTC (Input Type Control)

### 3.1 Warstwa S – Structural (ultraszybka, model-agnostyczna)
**Wejście:** tekst surowy  
**Wyjście:** `STRUCT_PROFILE` (flagi + metryki)

#### Cechy (przykładowy minimalny zestaw)
- `token_count`
- `line_count`, `avg_line_len`, `line_break_density`
- `digit_ratio`, `special_char_ratio`, `uppercase_ratio`
- `punct_density` (gęstość znaków interpunkcyjnych)
- `identifier_density` (ERR_12, ID_ABC, GUID-ish)
- `time_marker_density` (wykrycie znaczników czasu regexem; bez domeny)
- `list_marker_density` (np. “- ”, “1.”, “a)”; regex)
- `table_like_density` (kolumny/sep, np. `|`, `;`, wielokrotne spacje)

#### Strukturalne „tryby” (nie domeny)
Tworzymy wewnętrzne tryby:
- `LINEAR_LOG_LIKE`
- `PROSE_PARAGRAPH_LIKE`
- `LIST_PROCEDURE_LIKE`
- `TABLE_RECORD_LIKE`
- `MIXED_STRUCTURE`

Tryb wynika z cech, ale nie jest „prawdą” – to wskazówka do segmentacji.

> **Bez progów stałych**: używamy percentyli i porównań do rozkładów referencyjnych.

---

### 3.2 Warstwa D – Distributional (niejednoznaczność i mieszanie)
**Wejście:** tekst + `STRUCT_PROFILE`  
**Wyjście:** `DIST_PROFILE` (miary niejednoznaczności)

#### Miary
- `token_entropy` (Shannon) – różnorodność vs powtarzalność
- `repeatability_score` – powtarzalność linii/prefiksów/separatorów
- `internal_variance` – wariancja cech w segmentach (np. co 200–500 tokenów)
- `mixedness_flag` – jeśli segmenty różnią się profilem strukturalnym

> Interpretacja: wysoka `internal_variance` i niski overlap profili → **dane mieszane** (np. log + komentarz operatora + tabela).

---

### 3.3 Warstwa O – Order & Conflict (stabilność decyzji)
**Wejście:** `STRUCT_PROFILE` + segmentacja próbna  
**Wyjście:** `STABILITY_PROFILE`

#### Testy bez wag:
- **Order sensitivity**: porównaj profil/segmentację przy dwóch kolejnościach:
  - A: detect → segment
  - B: segment → detect
  Jeśli różnią się istotnie → tekst jest trudny / mieszany → wymaga ostrożniejszego ingestu.
- **Conflict**: jeśli różne bloki mają rozbieżne profile (np. jedne log-like, inne prose-like) → `conflict=true`

> Tu nie potrzeba progów. Konflikt to własność logiczna (występuje / nie występuje).

---

## 4) Sygnatura wejścia (jedyny kontrakt dla downstream)

### 4.1 Format sygnatury
`INPUT_CONTENT_SIGNATURE`:

```json
{
  "struct": { ... cechy + tryb ... },
  "dist":   { ... entropia, wariancja, repeatability ... },
  "stab":   { "order_sensitive": true/false, "conflict": true/false }
}
4.2 Zasada audytu

Każde pole w sygnaturze musi mieć:

wartość liczbową/flagę,

źródło obliczenia (np. nazwa funkcji),

dane wejściowe (np. zakres znaków lub segment).

5) Jak sygnatura wpływa na ingest (bez „magii”)

Sygnatura nie zmienia architektury.
Sygnatura wybiera politykę ingestu (policy) z ograniczonej listy.

5.1 Policy (IngestPolicy)

Przykład:

POLICY_LOG_STREAM

POLICY_PROCEDURE_DOC

POLICY_LEGAL_FORMAL

POLICY_SCIENCE_NOTES

POLICY_MIXED_SAFE

Uwaga: nazwy mogą być domenowe jako aliasy, ale decyzja opiera się na strukturze.

5.2 Reguły dominacji (bez wag)

Przykład reguł:

Jeśli stab.conflict=true lub stab.order_sensitive=true → POLICY_MIXED_SAFE

Else jeśli struct.mode=LINEAR_LOG_LIKE i dist.repeatability w górnym ogonie → POLICY_LOG_STREAM

Else jeśli struct.mode=LIST_PROCEDURE_LIKE i list_marker_density wysoka → POLICY_PROCEDURE_DOC

Else jeśli struct.mode=PROSE_PARAGRAPH_LIKE i avg_sentence_len wysoka → POLICY_LEGAL_FORMAL (alias)

Else → POLICY_SCIENCE_NOTES (alias) / domyślna

Ogony rozkładów: percentyle liczone offline per indeks lub per źródło.

6) Segmentacja (chunking) per policy
6.1 Wspólne zasady

Chunking ma być deterministyczny i stabilny.

Granice chunków preferują naturalne separatory (nagłówki, linie, punkty listy, znaczniki czasu).

Chunk powinien być “self-contained” (minimalizujemy urwane jednostki logiczne).

6.2 Przykładowe strategie

POLICY_LOG_STREAM: okna czasowe / okna linii + grupowanie po identyfikatorze

POLICY_PROCEDURE_DOC: zachowanie numeracji kroków i sekcji

POLICY_LEGAL_FORMAL: sekcje/artykuły/ustępy (nagłówki, formatowanie)

POLICY_SCIENCE_NOTES: akapity + nagłówki + cytowania/odnośniki

POLICY_MIXED_SAFE: najpierw podział na segmenty jednolite strukturalnie, dopiero potem chunking w każdym segmencie

7) Kompresja/Deduplikacja (opcjonalna, ale kluczowa dla logów)
7.1 Kiedy uruchamiać?

tylko gdy POLICY_LOG_STREAM lub dist.repeatability bardzo wysoka (ogon rozkładu),

nigdy „z automatu” dla tekstów formalnych (prawo/medycyna) bez jawnej potrzeby.

7.2 Co kompresować?

identyczne linie (heartbeat),

powtarzalne prefiksy z drobną zmiennością (parametry liczbowe),

serie telemetryczne → agregacja (min/max/avg) per okno + zachowanie surowych wyjątków.

Każda kompresja musi zapisać:

mapowanie “skompresowane → oryginalne zakresy” (audyt!)

8) Encode & Persist (embedding + zapis)
8.1 Zasada

Embedding liczymy po:

segmentacji,

deduplikacji (jeśli dotyczy),

z dodatkiem INPUT_CONTENT_SIGNATURE jako metadanych.

8.2 Agnostyczność embeddingów

embedding jest „jednym sygnałem”

sygnatura i policy są niezależne od modelu embeddingów

zmiana modelu embeddingów nie zmienia segmentacji i policy

9) Kontrakty (interfaces) – co kod ma implementować
9.1 Normalizer

IN: raw bytes/text + metadata źródła
OUT: normalized text + normalization report (audyt)

9.2 ContentSignatureDetector

IN: normalized text
OUT: INPUT_CONTENT_SIGNATURE + trace

9.3 IngestPolicySelector

IN: signature
OUT: policy + trace (reguły dominacji)

9.4 Segmenter

IN: text + policy + signature
OUT: chunks[] + chunk-metadata + segment trace

9.5 Compressor (opcjonalny)

IN: chunks + policy
OUT: compressed chunks + provenance map

9.6 Encoder

IN: chunks
OUT: embeddings + encoder report

9.7 Persistor

IN: chunks + embeddings + metadata
OUT: memory records (episodic/semantic/reflective) + audit record

10) Testowanie i rozwój kontrolowany
10.1 Zasada „signature regression”

Dla zestawu wejść referencyjnych zapisujemy oczekiwane sygnatury (lub ich stabilne fragmenty).

Zmiana kodu detectora → testy mówią: co się zmieniło.

10.2 Zasada „segmentation regression”

Dla wejść referencyjnych zapisujemy:

liczbę chunków,

granice (offsety),

podstawowe metadane chunków.

10.3 Zasada „no magic”

Każda nowa miara musi:

mieć definicję,

być logowana,

mieć uzasadnienie w audycie,

nie wprowadzać stałych progów.

11) Minimalny plan wdrożenia (kolejność prac)

Implementacja Normalizer + audyt normalizacji

Implementacja ContentSignatureDetector (Structural + Distributional)

PolicySelector regułami dominacji

Segmenter z 2–3 politykami (LOG_STREAM / PROCEDURE / MIXED_SAFE)

Segmentation regression tests

Dopiero potem: Compressor dla logów + provenance map

Integracja z embedding (ONNX) i zapis metadanych do pamięci

12) Co jest sukcesem?

Sukces nie jest “lepszy benchmark o +2%”.

Sukces jest:

stabilniejszy ingest (mniej losowych chunków),

mniej mieszania warstw pamięci,

mniej redundancji w logach,

lepsza audytowalność,

mniejsza wariancja wyników między domenami.

13) Checklist dla implementacji (szybko)

 Żadnych stałych wag

 Żadnych stałych progów (tylko percentyle/ogony)

 Sygnatura oparta o strukturę, nie o słowniki domenowe

 Policy wybierane regułami dominacji

 Chunking deterministyczny i zależny od policy

 Kompresja tylko z provenance map

 Regression tests: sygnatura + segmentacja

 Pełny audit trail per chunk

14) Notatka o perceptronie (opcjonalnie)

Perceptron ma sens tylko jako czujnik, jeśli:

wejściem są cechy strukturalne (nie embedding),

wagi są zamrożone,

wynik nie steruje architekturą, tylko dodaje metadane.

W innym wypadku niszczy agnostyczność i audyt.

Koniec

Ten dokument definiuje minimalny, uniwersalny i kontrolowalny sposób
rozpoznawania typu treści na wejściu i sterowania ingestem w RAE,
dla logów przemysłowych, dokumentów formalnych, medycznych i naukowych.

::contentReference[oaicite:0]{index=0}