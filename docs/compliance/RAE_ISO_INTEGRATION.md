# RAE COMPLIANCE FRAMEWORK (ISO 27001 & ISO 42001)

## 📁 1. BEZPIECZEŃSTWO INFORMACJI (ISO 27001)
- **Kontrola Dostępu:** Wdrożono mechanizm **Hard Frames**. Agenci nie mają dostępu do internetu, co zapobiega wyciekowi kodu źródłowego Dreamsoft do zewnętrznych baz danych treningowych.
- **Zarządzanie Kluczami:** Wszystkie klucze API (OpenAI, Anthropic) są wstrzykiwane jako zmienne środowiskowe i nigdy nie są logowane w pamięci semantycznej.
- **Integralność:** Każdy plik przed zapisem jest weryfikowany skrótem (hash), co gwarantuje, że kod nie został zmodyfikowany przez procesy nieautoryzowane.

## 🤖 ZARZĄDZANIE AI (ISO 42001)
- **Przejrzystość (Transparency):** System stosuje hierarchię **Consensus Council**. Decyzje o architekturze są wynikiem debaty wielu modeli, co minimalizuje ryzyko halucynacji (Bias Mitigation).
- **Rozliczalność (Accountability):** Każda linia kodu wygenerowana przez AI posiada cyfrowy ślad w warstwie `episodic` RAE (kto pisał, kto sprawdzał, o której godzinie).
- **Nadzór Ludzki (Human-in-the-loop):** Krytyczne konflikty, których nie rozwiąże "Rada Starszych", są eskalowane do Człowieka (Administratora).

## 📊 KLASYFIKACJA DANYCH
- **RESTRICTED:** Kod źródłowy Dreamsoft, logi z produkcji. (Przetwarzane wyłącznie w Hard Frames).
- **CONFIDENTIAL:** Receptury Feniksa, konfiguracja agentów.
- **PUBLIC:** Standardy Open Source, dokumentacja RAE.
