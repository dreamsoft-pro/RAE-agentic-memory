# PLAN IMPLEMENTACJI: TWARDE RAMY (HARD FRAMES)
**Data:** 2026-01-21
**Cel:** Przejście z zabezpieczeń deklaratywnych (prompty, kontrakty) na zabezpieczenia fizyczne (runtime enforcement).
**Status:** IN PROGRESS (Phase 1 & 2 Verified)
**Inspiracja:** Analiza zachowań LLM przy skali 100k pamięci (System Drift).

---

## 1. DOKTRYNA I MANIFEST (FAZA 0)
Zanim zmienimy kod, musimy zmienić definicję agenta w dokumentacji.

### 1.1. Nowa Definicja Agenta
Agent nie jest "użytkownikiem" API. Agent jest **niezaufanym procesem**, który ma zostać uruchomiony w kontrolowanym środowisku.

- **Prompt ≠ Prawo:** Prompt jest tylko sugestią.
- **Runtime = Prawo:** Tylko to, co fizycznie zablokowane, jest niemożliwe.
- **Brak Bezpośredniego IO:** Agent nie ma prawa "widzieć" Internetu ani modeli. Widzi tylko RAE.

**Zadania:**
- [x] Utworzyć `docs/architecture/HARD_FRAMES_MANIFESTO.md` (Formalny opis doktryny).
- [x] Zaktualizować `README.md` z ostrzeżeniem: "Prompt-based alignment fails at scale".
- [x] Zdefiniować "RAE-First Contract v2" – koniec z "prośbami", początek "fizycznych barier".

---

## 2. WARSTWA FIZYCZNA: KONTENER "ŚLEPY I GŁUCHY" (FAZA 1)
Cel: Stworzenie środowiska Docker, w którym agent fizycznie nie posiada narzędzi do ucieczki.

### 2.1. Hardening Obrazu (Dockerfile)
Agent nie może mieć zainstalowanych bibliotek, których nie powinien używać.

**Zadania:**
- [x] Stworzyć `Dockerfile.agent_secure` (bazujący na `python:3.12-slim`).
- [x] **Usunięcie binariów sieciowych:** `RUN rm -rf /usr/bin/curl /usr/bin/wget /usr/bin/nc`.
- [x] **Usunięcie SDK LLM:** Zablokowanie instalacji `openai`, `anthropic`, `google-generativeai`.
- [x] **Blokada PIP w runtime:** `ENV PIP_NO_INDEX=1`, usunięcie `pip` po instalacji zależności.

### 2.2. Izolacja Sieciowa (Network Jail)
Agent nie może mieć trasy do Internetu.

**Zadania:**
- [x] Konfiguracja `docker-compose.secure.yml`.
- [x] Sieć `rae_internal`: brak bramy domyślnej (no default gateway).
- [x] **Allowlist:** Agent widzi TYLKO `rae-api` (po nazwie hosta lub socket).
- [x] Test penetracyjny: Próba wykonania `requests.get('google.com')` z wnętrza kontenera musi zakończyć się natychmiastowym błędem sieci (nie timeoutem).
- **Status:** Zweryfikowano 2026-01-21 (`test_containment.py` PASSED).

---

## 3. WARSTWA LOGICZNA: RAE JAKO JEDYNY PROVIDER (FAZA 2)
Agent nie może wiedzieć, z jakim modelem rozmawia.

### 3.1. RAE Client (Thin Client)
Zamiast pełnych SDK, agent otrzymuje "cienkiego klienta".

**Zadania:**
- [x] Refaktoryzacja `rae-sdk`: Usunięcie wszelkich zależności od `langchain` czy `openai` w warstwie klienta.
- [x] Jedyny interfejs: `rae.ask(intent, context)` oraz `rae.perform(tool_name, args)`.
- [x] Agent nie importuje `models`, importuje `capabilities`.

### 3.2. Monkey Patching (Opcjonalne, ale zalecane)
Dla pewności, wstrzykujemy kod blokujący standardowe biblioteki w runtime Pythona.

**Zadania:**
- [x] Skrypt startowy nadpisujący `socket.socket` tak, aby pozwalał na połączenie tylko z adresem RAE API.
- [x] Każda inna próba otwarcia socketu rzuca `RuntimeError("Use RAE Protocol")`.
- **Status:** Zweryfikowano 2026-01-21 (`test_protocol_bypass_attempt` PASSED).

---

## 4. WARSTWA SYSTEMOWA: RAE KERNEL (FAZA 3)
To RAE (API/Server) decyduje o wszystkim.

### 4.1. Semantyczny Firewall
RAE API musi analizować żądania agenta ZANIM trafią do modelu.

**Zadania:**
- [x] Wdrożenie `IntentFilter` w `rae-api`.
- [x] Egzekucja limitów tokenów i budżetu "na sztywno" (hard caps).
- [x] **Memory Gating:** Przy 100k wspomnień, RAE API (nie LLM) decyduje, które 50 jest istotnych (Retrieval-First Enforcement).
- **Status:** Zweryfikowano 2026-01-21 (`test_firewall.py` PASSED, implementation in `apps/memory_api/firewall.py`).

### 4.2. Edytory jako "Głupie Terminale"
VS Code / Cursor nie mogą mieć własnych kluczy API.

**Zadania:**
- [ ] Opracowanie `RAE Editor Protocol` (JSON over HTTP/MCP).
- [ ] Edytor wysyła tylko diffy/kontekst do RAE. RAE odsyła zmiany.

---

## 5. HARMONOGRAM WDRAŻANIA

### Tydzień 1: Proof of Concept
1. Spisanie `HARD_FRAMES_MANIFESTO.md`.
2. Stworzenie `Dockerfile.agent_secure` (wersja beta).
3. Uruchomienie "głuchego" kontenera i próba ucieczki (curl/python requests).

### Tydzień 2: SDK Refactor
1. Oczyszczenie `rae-sdk` z zależności zewnętrznych.
2. Migracja jednego prostego agenta na `rae-sdk-secure`.

### Tydzień 3: Pełna Izolacja
1. Wdrożenie `docker-compose.secure.yml` dla środowiska deweloperskiego.
2. Testy na klastrze (Lumina) przy obciążeniu 100k pamięci – weryfikacja czy agent "głupieje" bezpiecznie (tzn. nie ucieka, tylko zgłasza brak możliwości).

---

## 6. MIERZALNE KRYTERIA SUKCESU
1. **Zero Egress:** `docker exec agent curl google.com` -> `Command not found` / `Network unreachable`.
2. **Zero Hallucinated API:** Agent próbujący importować `openai` dostaje `ImportError`.
3. **Stability at Scale:** Przy 100k pamięci agent nadal komunikuje się wyłącznie przez protokół RAE, nawet jeśli jego logika decyzyjna degraduje.
