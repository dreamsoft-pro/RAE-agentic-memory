👎 Słabe strony / ryzyka
1. Złożoność i próg wejścia

Architektura jest gęsta: wiele usług, wiele trybów (bare API vs ML vs reranker vs MCP vs watcher vs dashboard). Dla „zwykłego” zespołu to może być psychologicznie ciężkie – wymaga dobrego „minimal path to value”.

Dokumentacja jest obszerna, ale przy tej ilości komponentów przydałby się jeden bardzo prosty „deployment profile”: „single docker compose na 1 serwerze, minimal features, single-tenant”.

2. Test coverage & „enterprise target”

Sam projekt deklaruje, że 80%+ coverage to wciąż cel, nie stan – w TODO.md jest to nadal HIGH priority.

Endpoints są w dużej części opisane w API_DOCUMENTATION, ale coverage tras (route tests) jest jeszcze niewystarczający – to znaczy, że dużo logiki „przebicia” request→service jest testowane pośrednio, ale nie masz pełnych E2E na wszystkie 96 endpointów.

Część testów wymaga zewnętrznej infrastruktury (Postgres, Redis, Qdrant, ML), więc „pełne” odpalenie wszystkiego jest cięższe – to jest klasyczny koszt architektury microservices/ML-heavy.

3. Rozjazd między „Production Ready” a „Pre-release”

STATUS.md mówi jasno: Status: Production Ready, Version 2.0.0-enterprise, wszystkie joby CI na zielono. 

project_dump

VERSION_MATRIX wciąż kwalifikuje część rzeczy jako „development” (Core API 2.0.0-enterprise 🟡 Development, Python SDK 0.1.0 Development, Dashboard Development). 

project_dump

To nie jest techniczny problem, ale percepcyjny: na zewnątrz warto bardzo jasno komunikować, które komponenty są „GA/stable”, a które „beta/experimental”, żeby nie obiecywać za dużo.

4. Koszt i ciężar pełnego stacka

Pełny pakiet (Kubernetes, Prometheus, MCP, context-watcher, reranker, ML-service) jest świetny dla większych firm, ale może być zbyt ciężki operacyjnie dla małych zespołów – to wymaga jasno opisanego trybu „RAE Lite”.

ML heavy dependencies + dodatkowe usługi (reranker, embeddings, drift detection) – to jest duże obciążenie przy on-prem, szczególnie bez GPU / ograniczonych zasobach.

5. Wciąż otwarte „last mile features”

Z dokumentów wynika, że część koncepcji jest bardzo dobrze opisana, ale jeszcze nie w pełni domknięta implementacyjnie lub nie ma UX-owego opakowania:

Replay Tool dla sesji agenta – bardzo dobry pomysł, ale na razie to projekt w docsach, nie gotowe narzędzie. 

project_dump

Niektóre DI/metrics patterns wymienione jako „Next Steps” – DI dla wszystkich usług, health-checki DI, dodatkowe metryki.

Python SDK jest jeszcze w wersji 0.1.0 – przy takiej architekturze SDK jest kluczowe, bo większość ludzi będzie wchodzić przez niego, a nie bezpośrednio przez REST.

Co bym zrobił „dalej” jako 3 najbliższe kroki

RAE Lite Profile
Jeden prosty scenariusz: docker compose up → jeden kontener API + Postgres + Qdrant + Redis (bez dodatkowych usług), z gotowym PROFILE_LITE w docsach i Helm/compose.

Podniesienie coverage do ~75–80% dla kluczowych endpointów
Skupiłbym się na:

/v2/memory/*, /v2/agent/execute, /v2/search/hybrid, /v2/governance/*.

Stabilne „product story” i wersjonowanie

Wyraźne oznaczenie: które komponenty są GA (Core API, GraphRAG, MCP, Governance), a co jest „beta/experimental”.

Jedna tabela w README: „Enterprise Core vs Optional Modules”.