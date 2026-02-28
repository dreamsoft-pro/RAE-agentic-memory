📄 1. SECURITY-GUIDELINES.md
Security & Compliance Requirements for All Projects

Version: 1.0

1. Cel dokumentu

Dokument definiuje zasady bezpieczeństwa obowiązujące w każdym repozytorium, które wykorzystuje Quality Pattern.
Zakres obejmuje:

bezpieczeństwo kodu,

bezpieczeństwo CI/CD,

ochronę sekretów,

zależności (supply chain),

zasady dla kontrybutorów, devów i agentów AI.

2. Zasady bezpieczeństwa (High-Level)
2.1. Zero Secrets in Repo

Żadne klucze, tokeny, certyfikaty, hasła nie mogą znajdować się w repo.

Sekrety przechowywane wyłącznie w:

GitHub Secrets,

Hashicorp Vault,

AWS/GCP/Azure Secret Manager,

lub lokalne .env ignorowane przez git.

2.2. Wymóg skanowania zależności

Każdy projekt musi w CI wykonywać:

skanowanie CVE,

skanowanie podatności w dependencies,

sprawdzanie licencji (np. licencje niekompatybilne z Apache/MIT).

2.3. Zero Hardcoded Paths

Zakaz używania stałych ścieżek do:

danych użytkowników,

katalogów systemowych,

prywatnych zasobów.

2.4. Zagrożenia w logach

Logi nie mogą zawierać:

sekretów,

tokenów,

danych osobowych,

danych medycznych,

danych z kategorii „sensitive”.

3. Zasady dla developerów i kontrybutorów
3.1. PR Safety Review

Każdy PR musi być zatwierdzony przez osobę z prawami:

Security Reviewer,
lub

Project Maintainer przeszkolony w secure coding.

3.2. Observability jako element bezpieczeństwa

brak telemetry = brak możliwości wykrycia incydentów,

każde krytyczne API musi generować zdarzenia auditowe.

3.3. Zgłaszanie luk

Kontrybutorzy mogą zgłaszać problemy bezpieczeństwa:

w prywatnym repo (nie w public issues),

poprzez e-mail security@…,

poprzez specjalny kanał w firmie.

4. Zasady bezpieczeństwa dla agentów AI

(integracja z AGENT-GUIDELINES.md)

Agent AI:

NIE może zmieniać logiki autoryzacji,

NIE może zmieniać konfiguracji security,

NIE może stale „ulepszać” kryptografii (bez review człowieka),

NIE może usuwać walidacji danych,

NIE może wyciszać błędów krytycznych.

Agent może:

poprawiać testy,

poprawiać lintery,

poprawiać dokumentację,

poprawiać wydajność (jeśli testy przechodzą).

5. Zasady compliance

Projekty muszą potencjalnie spełniać:

ISO 42001,

ISO 27001,

RODO / GDPR,

lokalne przepisy branżowe,

zasady OSS (Apache 2.0, MIT).

6. Skanowanie przed release

Każda wersja musi przejść:

testy bezpieczeństwa,

dependency audit,

static application security testing (SAST),

dynamic application security testing (DAST) — jeśli dotyczy.