# Plan Naprawy Jakości Wyszukiwania RAE-Windows

## 1. Diagnoza problemu (Dlaczego wyniki są słabe?)

Podczas testów na plikach `improove.txt` i `Propozycja...txt` zidentyfikowano dwa krytyczne problemy:

1.  **Błędne kodowanie znaków (Data Corruption):** 
    Pliki tekstowe z polskimi znakami (Windows-1250) były błędnie odczytywane jako UTF-8. Powodowało to wycinanie polskich liter (np. "bezpieczeństwo" stawało się "bezpieczestwo").
    *   **Skutek:** Wyszukiwanie słów kluczowych (FTS5) zwracało zero wyników dla poprawnie wpisanych haseł.

2.  **Wyłączanie wyszukiwania wektorowego (Policy Failure):**
    Silnik matematyczny (Math Controller) dla krótkich zapytań wybierał strategię z wagą `vector: 0.0`.
    *   **Skutek:** System polegał wyłącznie na (uszkodzonym przez kodowanie) tekście, ignorując semantykę modelu Nomic. To powodowało "płaskie" wyniki ze score 0.5100 (brak dopasowania).

## 2. Kroki naprawcze (Do wdrożenia)

### Krok 1: Robust Decoding (Ingest)
Należy zmodyfikować proces wczytywania plików w `rae_lite/ui/app.py`, aby automatycznie wykrywał kodowanie.
- **Działanie:** Próba dekodowania kolejno: `utf-8-sig` (z BOM), `windows-1250` (polski Windows), a na końcu `utf-8` z ignorowaniem błędów.
- **Cel:** Poprawne zapisanie polskich znaków w bazie danych.

### Krok 2: Minimum Vector Weight (Brain)
Należy zmodyfikować generator ramion bandyty w `rae_core/math/controller.py`.
- **Działanie:** Wprowadzenie "podłogi" (floor) dla wagi wektorowej na poziomie `0.5`.
- **Cel:** Nawet jeśli wyszukiwanie tekstowe jest priorytetem, model semantyczny (Nomic) zawsze musi mieć głos, aby wyłapać podobieństwo znaczeń.

### Krok 3: Rekalibracja FTS5 (Search)
Weryfikacja działania indeksu pełnotekstowego w SQLite.
- **Działanie:** Upewnienie się, że operator `MATCH` poprawnie współpracuje z polskimi znakami po naprawieniu Kroku 1.
- **Cel:** Błyskawiczne i precyzyjne trafienia na hasła takie jak "oskarżony".

### Krok 4: Ponowny Ingest
Po wdrożeniu poprawek 1 i 2, konieczne jest **wyczyszczenie bazy danych** i ponowne wgranie dokumentów.
- **Cel:** Wygenerowanie poprawnych wektorów i indeksów tekstowych dla treści zawierających polskie znaki.

## 3. Integracja z RAE-mesh (Perspektywa)
Wdrożenie powyższych kroków pozwoli na zachowanie agnostycyzmu Core. Te same poprawki dekodowania i wag będą korzystne również dla wersji serwerowej, zwiększając jej odporność na różnorodne formaty plików wejściowych.

---
**Data:** 09.02.2026
**Autor:** RAE Agent
