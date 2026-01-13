# PLAN: RAE Full Potential Activation (Session & Sensory)

**Cel:** Ożywienie "martwych" kolumn (`session_id`, `ttl`, `expires_at`) i pełna aktywacja architektury poznawczej RAE.

## 1. Problem (Stan obecny)
- **Martwe Sesje:** Kolumna `session_id` jest w 100% pusta (NULL). RAE traktuje każde wspomnienie jako atomowe zdarzenie bez kontekstu konwersacji.
- **Brak Zapominania:** Kolumny `ttl` i `expires_at` są puste. Warstwa Sensoryczna nie działa – wszystko trafia od razu do Episodic i zostaje tam na zawsze.
- **Brak Wektorów:** Tylko 0.8% wspomnień w tabeli głównej ma embeddingi. Wyszukiwanie semantyczne (Math-1) działa na ułamku wiedzy.

## 2. Plan Realizacji (Next Session)

### Faza 1: Zarządzanie Sesjami (Session Awareness)
- [ ] Zaktualizować `RAEClient` (SDK), aby generował i przesyłał `session_id` w nagłówkach lub payloadzie.
- [ ] Wdrożyć middleware w API, który wiąże `session_id` z nowymi wspomnieniami.
- [ ] Dodać endpoint `GET /sessions/{id}/context` do pobierania pełnego kontekstu sesji.

### Faza 2: Aktywacja Pamięci Sensorycznej (Sensory Layer)
- [ ] Skonfigurować domyślny TTL dla warstwy `sensory` (np. 24h).
- [ ] Przekierować surowe inputy agenta (User/Assistant message) najpierw do warstwy `sensory`.
- [ ] Uruchomić `GarbageCollector` (Celery Beat), który usuwa przeterminowane rekordy `sensory`, jeśli nie zostały skonsolidowane ("zapominanie szumu").

### Faza 3: Uzupełnienie Wektorów (Embedding Backfill)
- [ ] Stworzyć skrypt/worker `scripts/backfill_embeddings.py`.
- [ ] Przeliczyć wektory dla 19 800+ wspomnień bez embeddingów (używając klastra Node1/Kubus dla wydajności).
- [ ] Zaktualizować tabelę `memories` oraz `memory_embeddings`.

### Faza 4: Wzbogacenie Metadanych (Metadata Enrichment)
- [ ] Zaktualizować logikę agentów, aby przesyłali `type` (text, code, image) i `source` w metadanych.

## 3. Instrukcja Startowa (Dla nowej sesji)

Aby rozpocząć realizację tego planu, w nowej sesji wydaj polecenie:

> **"Rozpocznij realizację planu RAE Full Potential Activation z pliku PLAN_RAE_FULL_POTENTIAL.md. Zacznij od Fazy 1: Zarządzanie Sesjami."**
