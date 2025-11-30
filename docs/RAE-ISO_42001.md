# RAE–agentic-memory – opis zgodności i gotowości pod ISO/IEC 42001

## 1. Cel dokumentu

Celem niniejszego dokumentu jest:

- opisanie, w jaki sposób projekt **RAE–agentic-memory** wpisuje się w wymagania normy **ISO/IEC 42001** dotyczącej systemu zarządzania sztuczną inteligencją (AI Management System – AIMS),
- wskazanie istniejących mechanizmów kontrolnych i obszarów wymagających dopracowania,
- zdefiniowanie minimalnego zestawu praktyk, które należy utrzymywać i rozwijać w kodzie oraz procesach wokół RAE.

Dokument nie stanowi pełnej certyfikacji – jest punktem wyjścia („readiness & design doc”), który można rozbudowywać wraz z rozwojem projektu.

---

## 2. Zakres systemu i kontekst

### 2.1. Rola RAE w ekosystemie

RAE–agentic-memory jest:

- **silnikiem pamięci i wiedzy dla agentów AI** (LLM oraz innych komponentów),
- warstwą odpowiedzialną za:
  - gromadzenie, indeksowanie i wyszukiwanie wiedzy (RAG, wektory, graf wiedzy),
  - kontekstualizację odpowiedzi agentów,
  - prowadzenie historii interakcji, decyzji i wyników (telemetria kognitywna),
  - wspieranie pętli refleksji i samodoskonalenia agentów.

RAE jest projektowany jako **usługa backendowa** (API) obsługiwana np. przez FastAPI, bazę relacyjną (Postgres), wektorowy silnik wyszukiwawczy (Qdrant / pgvector) oraz kolejki/zadania asynchroniczne (Redis/Celery/Prefect – zależnie od aktualnej implementacji).

### 2.2. Interesariusze i scenariusze użycia

Główne grupy interesariuszy:

- **Właściciele systemu RAE** – zespół projektowy odpowiedzialny za architekturę, rozwój i utrzymanie.
- **Zespoły produktowe / biznesowe** – wykorzystują RAE jako moduł pamięci dla agentów (wewnętrzne projekty, klienci zewnętrzni).
- **Użytkownicy końcowi (pośrednio)** – rozmawiają z agentami, których „hipokampem” jest RAE.
- **Kontrahenci / integratorzy** – korzystają z API RAE w ramach własnych usług.

Typowe scenariusze:

- agent obsługi klienta korzysta z pamięci RAE, aby zachować ciągłość rozmów i wątki spraw,
- agent techniczny (DevOps/IT) analizuje logi, błędy i post-mortemy zapisane w RAE,
- pipeline refleksji/uczenia z doświadczenia (reflection loop) wykorzystuje dane z RAE do modyfikowania polityk lub planów działania agentów.

---

## 3. Powiązanie z ISO/IEC 42001 – widok wysokopoziomowy

Norma ISO/IEC 42001 opisuje system zarządzania AI w kategoriach:

- **kontekstu, przywództwa, planowania, wsparcia, operacji, ewaluacji i doskonalenia**,
- oraz **specyficznych aspektów AI**, takich jak:
  - zarządzanie ryzykiem,
  - zarządzanie danymi i modelami,
  - przejrzystość i wyjaśnialność,
  - nadzór człowieka,
  - bezpieczeństwo i prywatność.

RAE nie jest **samodzielnym systemem AI**, a **komponentem infrastruktury AI** – „hipokampem” dla agentów. Dlatego:

- **System zarządzania AI (AIMS)** obejmuje:
  - kod RAE,
  - infrastrukturę (bazy, kolejki, monitoring),
  - procesy wokół wdrażania i konfiguracji RAE,
  - integracje z agentami, które na nim polegają.
- Ten dokument definiuje **minimalne wymagania i wzorce**, które RAE musi spełniać, aby łatwo wpasować się w pełny AIMS zgodny z ISO 42001.

---

## 4. Governance i odpowiedzialności

### 4.1. Role

Minimalny zestaw ról wokół RAE:

- **Owner RAE (Product/Technical Owner)**  
  Odpowiedzialny za:
  - kierunek rozwoju,
  - zgodność z założeniami bezpieczeństwa, prywatności i ISO 42001,
  - akceptację zmian architektonicznych.

- **Maintainer / Lead Developer**  
  Odpowiedzialny za:
  - jakość kodu,
  - przestrzeganie standardów (lint, testy, code review),
  - implementację mechanizmów zgodnych z tym dokumentem.

- **Data/Knowledge Steward (dla poszczególnych tenantów)**  
  Odpowiada za:
  - polityki danych (co może trafić do RAE, na jakich zasadach jest przechowywane),
  - oznaczanie źródeł wiedzy, poziomów zaufania, retencji.

- **Security & Compliance Contact**  
  Odpowiada za:
  - reagowanie na incydenty bezpieczeństwa,
  - współpracę przy audytach,
  - przegląd polityk retencji, anonimizacji i dostępu.

### 4.2. Decyzje i audytowalność

RAE powinien zapewniać:

- mechanizm **logowania decyzji systemu** w miejscach, gdzie:
  - wybierane są źródła wiedzy (RAG),
  - modyfikowany jest kontekst przekazywany do modelu LLM,
  - modyfikowane są polityki zachowania agentów (policy packs),
- możliwość powiązania:
  - żądania (request ID),
  - kontekstu (źródeł wiedzy, wersji polityk),
  - wyniku (odpowiedź, podjęte decyzje),
  - oraz osoby/systemu wywołującego (tenant, user, API key).

---

## 5. Zarządzanie ryzykiem AI w RAE

### 5.1. Kategorie ryzyk

Kluczowe ryzyka związane z RAE:

1. **Ryzyka dotyczące danych**
   - wyciek danych wrażliwych,
   - nieuprawniony dostęp do historii interakcji,
   - brak kontroli retencji i usuwania danych.

2. **Ryzyka dotyczące jakości wiedzy**
   - błędne, przestarzałe lub stronnicze źródła,
   - brak śledzenia pochodzenia (provenance),
   - mieszanie wiedzy z wielu tenantów.

3. **Ryzyka dotyczące decyzji agentów**
   - halucynacje wspierane przez „złe” konteksty,
   - brak możliwości odtworzenia, dlaczego agent podjął daną decyzję,
   - brak nadzoru człowieka w obszarach wysokiego ryzyka.

4. **Ryzyka operacyjne i bezpieczeństwa**
   - niedostępność RAE → agent działa bez pamięci (degradacja zachowania),
   - błędy w pipeline’ach asynchronicznych,
   - brak obsługi sytuacji awaryjnych (fallback, tryb „degraded”).

### 5.2. Mechanizmy kontrolne (docelowy stan)

W projekcie RAE powinny istnieć lub zostać dodane następujące mechanizmy:

- **Risk Register (rejestr ryzyk) dla RAE**  
  - trzymany w repo (np. `docs/RAE-Risk-Register.md`),
  - aktualizowany przy istotnych zmianach architektury/kodu,
  - opisujący ryzyka, ich skutki, prawdopodobieństwa i działania mitygujące.

- **Tagowanie źródeł wiedzy i scoring zaufania**
  - każde źródło ma:
    - właściciela (odpowiedzialna osoba / system),
    - poziom zaufania (`high/medium/low`),
    - datę aktualizacji,
    - politykę retencji.

- **Guardrails / Policy Packs**
  - zestawy reguł dla agentów zasilanych przez RAE,
  - np. zakazy podejmowania określonych decyzji bez zgody człowieka,
  - reguły weryfikacji źródeł i sanity-checków odpowiedzi.

- **Mechanizmy degradacji (graceful degradation)**
  - jeśli RAE jest niedostępny:
    - agent działa w trybie ograniczonym / fallback,
    - logowane jest zdarzenie „brak pamięci”,
    - sygnał dla operatora o konieczności interwencji.

---

## 6. Zarządzanie danymi i prywatnością

### 6.1. Klasy danych

W RAE należy rozróżniać co najmniej:

- **Dane operacyjne** (logi, telemetria, trace’y),
- **Dane wiedzy** (dokumenty, embeddingi, graf pamięci),
- **Dane użytkowników** (interakcje, identyfikatory, metadane).

Każda klasa powinna mieć:

- opis dopuszczalnych źródeł,
- zasady retencji,
- zasady anonimizacji / pseudonimizacji (jeśli dotyczy),
- zasady eksportu i usunięcia (right to be forgotten – jeśli tożsamość osób fizycznych jest w grze).

### 6.2. Mechanizmy w kodzie

W RAE powinny być zaimplementowane (lub zaplanowane):

- **warstwa anonimizacji / maskowania danych**:
  - możliwość włączenia polityki: „loguj treść zanonimizowaną” vs. „loguj tylko metadane”,
- **multi-tenant isolation**:
  - rozdzielenie przestrzeni danych na poziomie bazy (schema, namespace, tenant_id),
  - kontrola dostępu do API oparta o klucze lub tokeny przypisane do tenantów,
- **retencja**:
  - mechanizm cleanup’ów (zadania cykliczne),
  - konfiguracja retencji per-tenant.

---

## 7. Przejrzystość, wyjaśnialność i śledzenie decyzji

RAE powinien umożliwiać:

- **ścieżkę audytu dla każdego requestu**:
  - request ID,
  - powiązane dokumenty / wektory / nody grafu użyte do wygenerowania kontekstu,
  - polityki, które zostały zastosowane,
  - jak zmienił się stan pamięci (czy coś dopisano/zmodyfikowano).

- **mechanizmy „why this answer?”** (dla warstwy agentów):
  - możliwość zwrócenia wraz z odpowiedzią:
    - listy cytowanych źródeł,
    - krótkiego opisu kryteriów wyboru,
  - interfejs API, pozwalający pobrać szczegółowy raport (np. do panelu operatora).

---

## 8. Nadzór człowieka i obszary wysokiego ryzyka

ISO 42001 wymaga, aby w obszarach o podwyższonym ryzyku:

- decyzje były objęte **nadzorem człowieka**,
- istniały jasne zasady, kiedy człowiek musi „wejść w pętlę”.

RAE jako warstwa pamięci powinien:

- wspierać **oznaczanie scenariuszy / polityk jako „high-risk”**,
- umożliwić:
  - logowanie decyzji wymagających późniejszego przeglądu przez człowieka,
  - powiązanie takiej decyzji z konkretną osobą akceptującą (np. brygadzista, kierownik projektu),
- udostępniać interfejs (API/GUI), z którego:
  - operator może przejrzeć historię ważnych decyzji,
  - oznaczyć je jako zaakceptowane/odrzucone,
  - dodać komentarz lub wprowadzić zmianę w polityce.

---

## 9. Operacje, monitoring i telemetria

### 9.1. Monitoring techniczny

RAE powinien być objęty:

- monitoringiem dostępności, opóźnień, błędów (np. Prometheus + Grafana / inny stack),
- **observability**:
  - metryki,
  - logi,
  - trace’y (np. OpenTelemetry).

### 9.2. Telemetria kognitywna

Specyficzne dla RAE:

- **metryki jakości odpowiedzi agentów** (z perspektywy pamięci):
  - liczba zapytań, w których kontekst pochodził z RAE,
  - liczba przypadków, gdzie brakowało trafnych dokumentów („no good context”),
  - wskaźniki jakości (np. score’y z evaluatorów lub feedback użytkowników),
- **historia zmian polityk**:
  - kiedy i przez kogo zmodyfikowano policy pack,
  - jakie były konsekwencje (np. spadek/wzrost skarg, poprawa/psucie odpowiedzi).

---

## 10. Ewaluacja i ciągłe doskonalenie

Zgodnie z ISO 42001, system AI musi być:

- **regularnie ewaluowany**,
- **doskonalony w oparciu o dane i incydenty**.

Dla RAE oznacza to:

- **cykliczne przeglądy** (np. kwartalne) obejmujące:
  - ryzyka w rejestrze,
  - incydenty bezpieczeństwa i prywatności,
  - metryki jakości pamięci (precision/recall, coverage dokumentów),
  - feedback użytkowników i zespołów produktowych.

- **pętle refleksji technicznej**:
  - analiza błędnych odpowiedzi agentów, gdzie przyczyną była pamięć / kontekst,
  - wnioski przekładane na:
    - poprawę ingestu,
    - modyfikacje modeli/parametrów wyszukiwania,
    - zmiany w politykach.

- **dokumentowanie zmian**:
  - każda większa zmiana architektury pamięci / polityki bezpieczeństwa powinna mieć:
    - krótki opis (ADR – Architecture Decision Record),
    - ocenę wpływu na ryzyko,
    - plan monitorowania efektów.

---

## 11. Podsumowanie i status wdrożenia

Status wdrożenia (aktualizacja: 2025-11-30):

| Obszar                             | Status       | Komentarz / plan działań                          |
|------------------------------------|-------------|--------------------------------------------------|
| Role i odpowiedzialności           | ✅ Zaimplementowane | `docs/RAE-Roles.md` - pełna macierz RACI, 6 ról |
| Rejestr ryzyk (Risk Register)      | ✅ Zaimplementowane | `docs/RAE-Risk-Register.md` - 10 ryzyk z mitygacją |
| Tagowanie źródeł i scoring         | ✅ Zaimplementowane | `SourceTrustService` - automatic trust assessment |
| Source provenance tracking         | ✅ Zaimplementowane | `source_owner`, `trust_level`, `last_verified_at` |
| Multi-tenant isolation             | ✅ Zaimplementowane | TenantContextMiddleware + tenant_id filtering     |
| Retencja danych                    | ✅ Zaimplementowane | `RetentionService` + cleanup workers (daily at 1 AM) |
| GDPR "right to be forgotten"       | ✅ Zaimplementowane | `gdpr_delete_user_data_task` - cascade deletion  |
| Deletion audit trail               | ✅ Zaimplementowane | `deletion_audit_log` table with full tracking    |
| Telemetria techniczna              | ✅ Zaimplementowane | OpenTelemetry + structured logging (structlog)   |
| Telemetria kognitywna              | W trakcie   | Drift detection + semantic quality metrics (częściowo) |
| Policy Packs / Guardrails          | W trakcie   | RulesEngine istnieje, uporządkować format        |
| High-risk scenario marking         | W trakcie   | Zaprojektować oznaczanie + approval workflow     |
| Audytowalność decyzji              | Częściowo   | Audit logs + context tracking (wzmocnić provenance) |
| Graceful degradation               | Do zrobienia| Circuit breaker + fallback mode dla agentów      |
| Procedury ewaluacji i przeglądów   | ✅ Zaimplementowane | Quarterly review process w dokumentacji          |

**Legenda:**
- ✅ Zaimplementowane - Feature gotowy do użycia, pokryty testami
- Częściowo - Podstawowa implementacja istnieje, wymaga wzmocnienia
- W trakcie - Rozpoczęte prace, wymaga dokończenia
- Do zrobienia - Planowane, nie rozpoczęte

### 11.1. Najważniejsze osiągnięcia (2025-11-30)

**Zgodność z ISO/IEC 42001:**
- ✅ **Rejestr ryzyk** - 10 zidentyfikowanych ryzyk z mitygacją (RISK-001 do RISK-010)
- ✅ **Source Trust Scoring** - Automatyczna ocena wiarygodności źródeł wiedzy
- ✅ **Data Retention & GDPR** - Pełna zgodność z GDPR Article 17 (right to erasure)
- ✅ **Role i odpowiedzialności** - Macierz RACI dla 6 ról organizacyjnych
- ✅ **Audit trail** - Śledzenie wszystkich operacji deletion z metadata

**Mitygacja ryzyk o wysokim priorytecie:**
- ✅ **RISK-002** (Brak kontroli retencji) - RetentionService + cleanup workers
- ✅ **RISK-003** (Halucynacje z błędnych kontekstów) - Source trust scoring
- 🟡 **RISK-001** (Wyciek danych) - Multi-tenant isolation + audit logging (RLS planowany)
- 🟡 **RISK-010** (Brak nadzoru człowieka) - High-risk marking (w planach)

### 11.2. Następne kroki (priorytet)

**Q4 2025:**
1. PostgreSQL Row-Level Security (RLS) dla tenant isolation (RISK-001, RISK-006)
2. High-risk scenario marking + human approval workflow (RISK-010)
3. Context provenance linking - pełna ścieżka: query → context → decision (RISK-005)

**Q1 2026:**
4. Graceful degradation - circuit breaker + fallback mode (RISK-004)
5. Telemetria kognitywna - memory quality metrics dashboard (RISK-009)
6. Policy Packs - wersjonowanie i enforcement engine (RISK-003)

### 11.3. Dokumenty i artifakty

**Dokumentacja compliance:**
- `docs/RAE-ISO_42001.md` - Ten dokument (readiness assessment)
- `docs/RAE-Risk-Register.md` - Rejestr ryzyk z mitygacją
- `docs/RAE-Roles.md` - Role i odpowiedzialności (RACI matrix)
- `docs/SECURITY.md` - Security assessment

**Implementacja w kodzie:**
- `apps/memory_api/models.py` - Modele z polami ISO 42001 (trust_level, source_owner)
- `apps/memory_api/services/source_trust_service.py` - Source trust scoring
- `apps/memory_api/services/retention_service.py` - Data retention & GDPR compliance
- `apps/memory_api/tasks/background_tasks.py` - Cleanup workers & GDPR deletion tasks
- `apps/memory_api/models/tenant.py` - TenantConfig z retention policies

Ten dokument jest **żywy** – należy go aktualizować wraz z:

- rozwojem kodu RAE–agentic-memory,
- pojawianiem się nowych scenariuszy użycia,
- wymaganiami klientów i audytorów.