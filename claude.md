## 1. Krytyczne techniczne drobiazgi (do zrobienia najpierw)

### 1.1. Spójność Docker / entry pointów

- [ ] **Naprawić `infra/docker-compose.dev.yml`**:
  - Teraz jest:  
    `command: uvicorn apps.memory-api.main:app --reload ...`  
  - A moduł to: `apps.memory_api.main:app` (podkreślnik, nie myślnik).  
  - **Plan**:
    - Ujednolicić do `apps.memory_api.main:app` w dev compose.
    - Sprawdzić nazwę usług (`memory-api`, `memory-api-worker`) vs nazwy w Makefile/logs.

- [ ] **Ujednolicić historię z dwoma compose’ami**:
  - Root `docker-compose.yml` (usługa `rae-api`, `rae-postgres`, `rae-redis`, `rae-qdrant`, `celery-worker`, `celery-beat`).  
  - `infra/docker-compose.yml` (trochę inna nazwa usług / kontekst).  
  - **Decyzja**:
    - Albo root `docker-compose.yml` = „oficjalny” sposób,
    - a `infra/` opisane jako „advanced / infra-only”,
    - albo wszystko przenieść do `infra/` i w README jasno to napisać.
  - README/`docs/getting_started.md` powinny wskazywać **jeden kanoniczny** sposób startu.  

### 1.2. Zmienna środowiskowe – nazwy i przykłady

- [ ] **Spójność `RAE_VECTOR_BACKEND` vs `VECTOR_STORE_BACKEND`**:
  - W Docker Compose: `RAE_VECTOR_BACKEND=qdrant`.  
  - W docs: `VECTOR_STORE_BACKEND: qdrant | pgvector`.  
  - **Plan**:
    - Wybrać jedną nazwę (np. `RAE_VECTOR_BACKEND`),
    - w kodzie dodać prostą warstwę kompatybilności (czytanie starej nazwy jeśli nowa pusta),
    - w docs trzymać tylko jedną, docelową nazwę.

- [ ] **API keys – cudzysłowy vs brak cudzysłowów**:
  - W „troubleshooting” słusznie piszesz: `OPENAI_API_KEY=sk-...` (bez cudzysłowu) i wskazujesz `"sk-..."` jako zły przykład.  
  - W innym miejscu przykładowy `.env` ma `OPENAI_API_KEY="your-openai-api-key"` (z cudzysłowem).  
  - **Plan**:
    - Ujednolicić wszystkie przykłady na **bez cudzysłowów**,
    - dodać krótką uwagę „w .env nie używamy cudzysłowów” w jednym widocznym miejscu.

### 1.3. requirements – „lekko” vs „ciężko”

- [ ] Przejrzeć `apps/memory_api/requirements*.txt` i upewnić się, że:
  - `requirements.txt` = minimalny zestaw do odpalenia API,
  - rzeczy typu `spacy`, `sentence-transformers` i heavy ML lądują w czymś typu `requirements-ml.txt` / `requirements-extra.txt`,
  - CI instalujące `requirements-test.txt` wie, że to jest superset (nie dubluje).  

---

## 2. Porządki repo – „zewnętrzny odbiorca nie musi widzieć Twoich notatek”

Masz kilka bardzo wartościowych, ale jednak **wewnętrznych** plików:

- `PLAN_NAPRAWCZY.md` (stary plan optymalizacji v2.0)  
- Różne pliki w stylu `KIERUNEK_X`, `VERIFICATION_REPORT.md` – super jako dokumentacja procesu, ale mogą wyglądać chaotycznie dla kogoś z zewnątrz.  

Propozycja:

- [ ] Przenieść je do `docs/internal/` **albo**:
  - scalić ich treść z:
    - `ROADMAP.md` (rzeczy strategiczne),
    - `docs/concepts/architecture.md` (rzeczy techniczne),
    - `docs/examples/overview.md` (rzeczy „jak używać”).  
- [ ] W README/`docs/index.md` **nie linkować** do plików „internal”, żeby wchodzili tam tylko zainteresowani.

---

## 3. Spójność naming/branding i komunikatów

W repo przewija się kilka nazw:

- „RAE - Reflective Agentic Memory Engine”  
- „RAE Agentic Memory” (w docs, roadmap, index)  
- „Reflective Agentic-memory Engine” (z myślnikiem) tu i ówdzie.  

Plan:

- [ ] Wybrać **jedną oficjalną etykietę**, np.  
  **„RAE – Reflective Agentic Memory Engine”**
- [ ] Zrobić szybki search&replace w:
  - README,
  - `docs/index.md`,
  - `docs/architecture.md`,
  - `ROADMAP.md`,
  - dashboard README.
- [ ] W README dodać krótką sekcję „Naming” typu:
  > W dokumentacji używamy skrótów RAE / RAE Engine. Pełna nazwa: Reflective Agentic Memory Engine.

---

## 4. Dopełnienie dokumentacji „production-grade”

Masz świetny opis idei i feature’ów, ale kilka drobiazgów „enterprise-owych”, które podnosisz w tekstach, jeszcze nie jest spiętych w jednym miejscu.

### 4.1. Security & auth

W różnych miejscach pojawiają się:

- API Key auth,
- OAuth / JWT (Auth0 / domena, audience)  
- multi-tenancy, RBAC, tiers, quotas (testy `TestRBACModels`, `TestTenantModels`).  

Plan:

- [ ] Osobny plik: `docs/guides/security-and-multi-tenancy.md`, w którym opiszesz:
  - konfigurację API Key vs OAuth (kiedy co),
  - model tenantów i ról (z mapką do modeli w kodzie),
  - domyślne zabezpieczenia (CORS, rate limiting),
  - rekomendowane ustawienia dla produkcji.
- [ ] Dodać `SECURITY.md` w root, z linkiem do tego guida (GitHub to lubi).

### 4.2. Cost Controller & Context Cache

W `docs/index.md` już wspominasz o **Cost Controllerze**, context cache, PII scrubber, reflection hook itp.  

Plan:

- [ ] Krótki technical spec w `docs/concepts/cost-controller.md`:
  - jakie sygnały bierzesz pod uwagę (budżet tokenów, typ zadania, priorytet),
  - jak decydujesz model (lokalny vs zewnętrzny),
  - jak integruje się z LLM backendem.
- [ ] Analogicznie `docs/concepts/context-cache.md`:
  - różnica między RAE pamięcią a cachem LLM,
  - kiedy cache jest odświeżany, kiedy inval,
  - jak to w praktyce wykorzystać (np. „semantic + reflective” → Gemini Context Cache).

---

## 5. UX dla dewelopera: examples, SDK, MCP

### 5.1. SDK Python

- README pokazuje proste użycie `MemoryClient` (hybrid_search itd.).  
- W ROADMAP masz plan SDK dla Go/Node.  

Plan:

- [ ] Upewnić się, że:
  - `sdk/python/rae_memory_sdk` ma krótki `README.md` z:
    - instalacją (na razie `pip install -e sdk/python/rae_memory_sdk`),
    - kilkoma snippetami (store, query, hybrid_search, reflection).
- [ ] Dodać sekcję „Python SDK” w głównym README z linkiem do tego pliku.

### 5.2. Examples – smoke test

Masz w dokumentach referencje do:

- `examples/quickstart.py`  
- `examples/graphrag_examples.py`  

Plan:

- [ ] Przelecieć wszystkie pliki z `docs/examples/*.md` i:
  - potwierdzić, że każdy podany path istnieje,
  - każda komenda shellowa działa z aktualnym `docker-compose`/Makefile.
- [ ] Dodać jedno „złote” E2E:
  - `make start`
  - `python examples/quickstart.py`
  - oczekiwany output (krótko opisany w docs).

### 5.3. MCP / edytor

Masz fajnie opisaną integrację MCP w README (konfiguracja mcpServers dla edytora).  

- [ ] Dodać `docs/integrations/mcp.md` z:
  - minimalnym configiem dla Cursor/VSCode,
  - jednym scenariuszem: „zapamiętaj decyzję architektoniczną” → „odtwórz ją”.

---

## 6. Komunikat na starcie: „Beta, ale poważne”

Na koniec – kosmetycznie, ale ważne dla zaufania:

- [ ] W README dodać małą sekcję np. **Project Status**:
  - „RAE is currently in **public beta**.”
  - Co działa stabilnie (core memory/store/query, GraphRAG, SDK, dashboard).
  - Czego nie obiecujesz (HA/geo-replication/SLAs).
- [ ] W `ROADMAP.md` dopisać, które punkty z „Near-Term” są już zrobione, żeby nie wyglądało jak czysta teoria.  

---

## 7. Kolejność działań (sugerowany sprint)

1. **Techniczne fixy blokujące**:
   - docker compose dev (moduł `apps.memory_api.main:app`),
   - env names + przykładowe `.env`,
   - sanity check requirements (core vs extra).

2. **Porządki repo i nazewnictwo**:
   - przeniesienie wewnętrznych plików do `docs/internal/`,
   - ujednolicenie nazwy projektu i prefixów RAE\_*.

3. **Security + Cost/Cache docs**:
   - `SECURITY.md` + guide w `docs/guides/`,
   - cost controller + context cache w `docs/concepts/`.

4. **Developer UX**:
   - README dla SDK,
   - przetestowane examples, mały E2E flow,
   - MCP integration guide.

5. **Tag i release**:
   - oznaczyć repo jako publiczne (jeśli jeszcze nie),
   - dodać tag, np. `v0.9.0-beta`,
   - opcjonalnie: przygotować krótkie „Release Notes” w `RELEASE_NOTES.md`.