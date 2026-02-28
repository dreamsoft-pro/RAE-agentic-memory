# Podsumowanie Sesji (14.01.2026)

## ✅ Rozwiązane Problemy

### 1. Dashboard - Puste Wyniki ("0 Memories")
- **Przyczyna:** Dashboard wysyła zapytanie `query_text: "*"`, które nie było obsługiwane przez strategie wyszukiwania (`FullTextStrategy` i `VectorSearchStrategy` zwracały puste listy).
- **Rozwiązanie:** Zmodyfikowano `rae-core/rae_core/search/strategies/fulltext.py`. Dodano warunek: jeśli `query == "*"`, zwracaj wszystkie rekordy z maksymalnym wynikiem (`1.0`).
- **Weryfikacja:** Utworzono i uruchomiono test `rae-core/tests/test_wildcard.py` wewnątrz kontenera `rae-api-dev`. Test przeszedł pomyślnie.

### 2. Weryfikacja Mechanizmu Wektorów
- Potwierdzono, że `QdrantVectorStore` w `rae_adapters/qdrant.py` jest **agnostyczny względem modelu**.
- Automatycznie mapuje wektory na odpowiednie pola w Qdrant na podstawie ich wymiarowości (1536 -> openai, 768 -> ollama, 384 -> dense, 1024 -> cohere).
- Działa to niezależnie od użytego LLM.

## ⚠️ Uwagi Techniczne dla Następnej Sesji
- **Środowisko Lokalne:** Brak działającego `.venv` na hoście. Wszystkie komendy Pythonowe (testy, skrypty) należy uruchamiać wewnątrz kontenerów Docker (`docker exec rae-api-dev ...`).
- **Auth:** API w trybie dev ma włączone `TENANCY_ENABLED=true`. Aby robić zapytania `curl`, trzeba użyć poprawnego klucza API (lub wyłączyć auth w `.env`). Testy jednostkowe omijają ten problem.
- **Baza Danych:** Tenant ID w bazie to `00000000-0000-0000-0000-000000000000`.

## 📌 Plan na Kolejną Sesję
1. **User Verification:** Poprosić użytkownika o potwierdzenie, że Dashboard wyświetla dane.
2. **Commit:** Zatwierdzić zmiany w `rae-core` (fix + test).
3. **Docs:** Zaktualizować dokumentację API, wspominając o obsłudze wildcarda `*`.

## 🚨 Krytyczny Błąd do Rozwiązania (Priorytet #1)
**Problem:** Dashboard -> Project Reflection zwraca **500 Internal Server Error**.
**Komunikat:** `Hierarchical reflection generation failed: Could not connect to Ollama server at http://localhost:11434: All connection attempts failed` (lub podobny błąd połączenia).

**Co zrobiono:**
1. Zmieniono konfigurację `llm_config.yaml` na używanie `local_deepseek_coder` (zamiast OpenAI).
2. Zaktualizowano `docker-compose.yml` (`RAE_LLM_MODEL_DEFAULT=local_deepseek_coder`).
3. Zaktualizowano `LLMRouter` (`apps/llm/broker/llm_router.py`), aby:
   - Mapował modele `local_deepseek*` na providera `ollama`.
   - Nadpisywał endpoint `http://localhost:11434` wartością ze zmiennej środowiskowej `OLLAMA_API_URL`.
   - W `docker-compose.yml` zmienna ta jest ustawiona na `http://ollama-dev:11434`.

**Stan obecny:**
Mimo powyższych zmian, błąd sugeruje, że API nadal próbuje łączyć się z `localhost:11434` LUB `ollama-dev` jest nieosiągalne z kontenera `rae-api-dev`.

**Zadanie dla następnego Agenta:**
1. Sprawdzić, czy zmienna `OLLAMA_API_URL` jest poprawnie widoczna wewnątrz procesu Pythona (może `os.getenv` nie widzi jej w momencie importu?).
2. Zdebugować połączenie sieciowe z kontenera `rae-api-dev` do `rae-ollama-dev` (ping, curl).
3. Sprawdzić logi `rae-api-dev` pod kątem dokładnego adresu URL, z jakim próbuje się połączyć.

