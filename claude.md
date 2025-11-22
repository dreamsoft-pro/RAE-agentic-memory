# RAE – Polishing Before Public Release (Release Candidate Plan)

Ten dokument zawiera precyzyjną listę tego, co warto poprawić przed dużą publiczną publikacją RAE Reflective Agentic-Memory Engine.

Repozytorium jest już **stabilne, czyste i technicznie wartościowe**, jednak ostatni polishing zwiększy wiarygodność i odbiór przez społeczność Open Source.

---

# 1. Wyrównać jakość dokumentacji (READMEs + OpenAPI)
### Status: 80% kompletne — wymaga finalnej synchronizacji

**Do zrobienia:**
- [ ] Dodać komplet przykładów OpenAPI dla wszystkich modeli (część już jest, część jeszcze bez examples).
- [ ] Ujednolicić nazewnictwo:
  - „RAE Reflective Agentic-Memory Engine”
  - „memory-api”, „ml-service”
  - „GraphRAG”, „Hybrid Search”
- [ ] Dodać diagram request-flow:
  - client → memory-api → ML-service → repositories → PostgreSQL → vector store
- [ ] W README dopisać sekcję:
  - „Scaling ML Service horizontally”
  - „Why microservices?” (masz to w rozmowie, warto przenieść do dokumentacji)

---

# 2. GraphExtractionService — refaktoryzacja do pełnego Repository Pattern
### Status: ✅ COMPLETED

**Problem rozwiązany:**
Moduł extraction został całkowicie zrefaktoryzowany do czystej architektury Repository/DAO.

**Wykonano:**
- [x] Przeniesiono logikę odczytu/wstawiania do `GraphRepository`
  - `create_node()` - wstawianie węzłów z ON CONFLICT DO NOTHING
  - `create_edge()` - wstawianie krawędzi z obsługą duplikatów
  - `get_node_internal_id()` - pobieranie wewnętrznych ID węzłów
  - `store_graph_triples()` - kompletna logika zapisu trójek
- [x] Ujednolicono obsługę JSONB (json.dumps() przed INSERT, json.loads() przy SELECT)
- [x] Dodano 7 testów integracyjnych z testcontainers (wszystkie przechodzą)
  - test_fetch_episodic_memories_uses_repository
  - test_store_graph_triples_creates_nodes_and_edges
  - test_store_triples_handles_duplicates_gracefully
  - test_graph_repository_jsonb_serialization
  - test_memory_repository_returns_source_field
  - test_graph_repository_get_node_internal_id
  - test_end_to_end_triple_storage_workflow
- [x] Dodano UNIQUE constraint dla edges (tenant_id, project_id, source_node_id, target_node_id, relation)
- [x] GraphExtractionService używa teraz MemoryRepository i GraphRepository

**Architektura jest teraz w pełni czysta - zero bezpośrednich zapytań SQL w warstwie service.**

---

# 3. MLServiceClient — resilience layer (circuit breaker & retries)
### Status: ✅ COMPLETED

**Problem rozwiązany:**
MLServiceClient jest teraz enterprise-grade z pełną odpornością na błędy.

**Wykonano:**
- [x] Dodano retry logic (3 próby, exponential backoff 200/400/800 ms) używając biblioteki tenacity
- [x] Wprowadzono circuit breaker pattern (otwiera się po 5 błędach, resetuje po 30s)
  - Stany: CLOSED (normalna praca), OPEN (blokowanie żądań), HALF_OPEN (testowanie)
- [x] Zapis awarii ML Service przez structlog (gotowe do integracji z ELK/Grafana)
- [x] Health check z automatycznym resetowaniem circuit breakera
- [x] Wszystkie 4 endpointy ML Service używają warstwy resilience:
  - resolve_entities()
  - extract_triples()
  - generate_embeddings()
  - extract_keywords()

**RAE jest teraz gotowy do długich zadań produkcyjnych - resilience jest kluczowy.**

---

# 4. Code Coverage — poprawa kluczowych modułów
### Status: realne 11% (bo duża część kodu nie jest instrumentowana)

**Plan minimum przed release:**
- [ ] Dodać testy unit (nie integracyjne) dla:
  - HybridSearchService (mocks)
  - GraphRepository traversal fallback
  - MemoryRepository filtering
  - MLServiceClient (mock responses)
- [ ] Osiągnąć 35–40% pokrycia (realne w 1 dzień)
- [ ] Usunąć z repo katalog `htmlcov/`

Nie trzeba 80%.  
Zespół open-source chętnie kontrybuuje w testy, jeśli projekt ma solidne core.

---

# 5. Docker / Deployment – ostatnie wygładzenie
### Status: ✅ COMPLETED

**Problem rozwiązany:**
Docker Compose jest teraz w pełni production-ready z parametryzacją i health checks.

**Wykonano:**
- [x] Wszystkie serwisy mają `restart: unless-stopped` (production-ready)
- [x] Healthchecks dla wszystkich serwisów już istnieją (postgres, redis, qdrant, ml-service, rae-api)
- [x] Sparametryzowano `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` przez zmienne środowiskowe:
  - `${POSTGRES_USER:-rae}`
  - `${POSTGRES_PASSWORD:-rae_password}`
  - `${POSTGRES_DB:-rae}`
- [x] DATABASE_URL używa parametrów środowiskowych we wszystkich serwisach

---

# 6. Stabilizacja OpenAPI / Versioning
### Status: dobre — wymaga drobnego ujednolicenia

**Do zrobienia:**
- [ ] Ustawić stałą wersję API: `v1` (ustabilizowane)
- [ ] Dodać datę generacji OpenAPI do dokumentu
- [ ] Dodać w README sekcję:
  - „Breaking changes policy”
  - „Planned v2 improvements (optional)”

---

# 7. Dodanie 1–2 E2E Workflow Examples
### Status: brakuje gotowego „jak tego użyć w realnym projekcie”

**Warto dodać:**
- [ ] `examples/python/basic_workflow.py`:  
  - store memory → embed → hybrid search → get reflection → store result
- [ ] `examples/python/graph_workflow.py`:  
  - add nodes → create edges → traverse BFS/DFS → GraphRAG search

Użytkownicy lubią od razu uruchomić przykład.

---

# 8. Release Engineering (przed ogłoszeniem)
### Status: ✅ PARTIALLY COMPLETED

**Problem rozwiązany:**
CHANGELOG.md utworzony z pełną dokumentacją wersji.

**Wykonano:**
- [x] Dodano `CHANGELOG.md` z dokumentacją:
  - v1.0.0-rc.1 - Production readiness (MLService resilience, GraphExtraction refactor, Docker improvements)
  - v0.9.0 - Microservices architecture
  - v0.8.0 - Core features
  - Release naming conventions
  - Linki do repozytorium i issue trackera

**Do dokończenia (opcjonalne):**
- [ ] Dodać GitHub Release z opisem zmian (po finalnym review)
- [ ] Podpiąć realny badge do CI (test + build)
- [ ] Ustawić draft na PyPI dla `rae-memory-sdk`

---

# 9. Dokumentacja ML Service
### Status: dobra — wymaga pełnego opisania kontraktów

Masz:
- embeddings,
- keywords,
- triples,
- entity-resolution.

**Do zrobienia:**
- [ ] Dodać tabelę „Performance & timeouts”
- [ ] Dodać przykłady request+response dla każdego endpointu
- [ ] Dodać sekcję „Load Balancing ML Service”

---

# 10. Oznaczenie projektu jako „Beta / Release Candidate”
### Status: wymagane przed public announcement

**Do zrobienia:**
- [ ] W README dopisać:
  - „Status: Beta / Release Candidate”
  - „Core architecture stable”
  - „Public API stable (v1)”
- [ ] Zachęcić community do PR-ów:
  - testy,
  - research integrations,
  - optymalizacje GraphRAG,
  - wektorowe indeksy alternatywne.

---

# 11. Techniczna higiena repo (ostatni punkt)
### Status: ✅ COMPLETED

**Problem rozwiązany:**
Repozytorium jest teraz czyste i profesjonalne.

**Wykonano:**
- [x] Usunięto `.coverage` i `htmlcov/` z repozytorium
- [x] Zaktualizowano `.gitignore` z kompletnymi wykluczeniami:
  - `.coverage` i `.coverage.*`
  - `htmlcov/`
  - `.pytest_cache/`
  - `.tox/`
  - `coverage.xml`
  - `.hypothesis/`
- [x] Struktura katalogów jest już w snake_case (apps/memory_api)

---

# 12. Proponowany Release Tag
- v0.9.0 – „Microservices + Testcontainers + DAO”
- v1.0.0-rc.1 – po wykonaniu tej checklisty

---

