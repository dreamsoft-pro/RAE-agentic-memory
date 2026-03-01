📄 AUTO-TESTING-CI-SPEC.md
Automated Testing Specification & “Main Always Green” Rules

Version: 1.0

1. Cel dokumentu

Dokument opisuje zasady testowania, które gwarantują:

stabilność głównej gałęzi (main),

powtarzalność wyników,

automatyczną walidację jakości,

zgodność z Quality Pattern.

Kluczowa zasada:

Gałąź main musi być zawsze zielona.
Każdy commit przechodzi testy, bez wyjątku.

2. Filar jakości — Main Always Green
2.1. Co to oznacza?

main musi zawsze:

przechodzić testy,

przechodzić lintery,

mieć ZERO WARNINGS,

mieć zero flaky tests,

nie mieć drift regression.

2.2. Konsekwencje

bezpośredni push na main – zabroniony,

PR → CI → review → merge,

CI pełni rolę strażnika jakości.

3. Rodzaje testów wymagane w każdym projekcie
3.1. Testy jednostkowe

szybkie,

deterministyczne,

niezależne od sieci, I/O, zewnętrznych systemów.

3.2. Testy integracyjne

testują warstwy i interakcje,

mogą używać środowisk mock lub dockerowych.

3.3. Testy kontraktów

testują API, struktury danych i zachowanie,

zapewniają brak driftu semantycznego.

3.4. Testy wydajności / benchmarki

wymagane dla ZERO DRIFT.

3.5. Testy bezpieczeństwa

static analysis (SAST),

dependency audit,

sprawdzenie błędów konfiguracyjnych.

4. Reguły automatycznego testowania w CI
4.1. Każdy PR musi uruchomić pełny pipeline

Pipeline musi zawierać:

lintery,

typowanie (jeśli dotyczy),

testy jednostkowe,

testy integracyjne,

testy kontraktów,

testy drift benchmark,

skanowanie bezpieczeństwa.

4.2. Każdy krok pipeline musi być blokujący

Żaden z poniższych nie może być „soft fail”:

linter,

warning,

flaky detection,

drift regression,

security scan.

4.3. Testy nie mogą zależeć od Internetu

wszystkie zewnętrzne dane muszą być mockowane,

wszystkie API external → stub/mocker.

4.4. Testy muszą być deterministyczne

Jeśli test raz nie przechodzi → idzie do kwarantanny.

5. Testy Nightly

Dla modułów ciężkich (AI, algorytmy, API):

pełne benchmarki,

testy obciążeniowe,

long-run stability tests.

6. Zasady dla developerów

PR bez testów dot. zmienionego kodu → odrzucony,

PR zwiększający liczbę flaky tests → odrzucony,

PR ze zmianą logiki bezpieczeństwa → wymaga dwóch reviewerów.

7. Integracja z Auto-Healing CI

Jeśli pipeline wykryje problem:

CI generuje kontekst,

agent AI tworzy PR naprawczy,

człowiek dokonuje ostatecznej oceny.

8. Diagram “Main Always Green”
PR → CI → (lint + test + contract + drift + security)
     ↓
   OK? → merge → main stays green
   NO → block → auto-heal PR → review → merge