# Instrukcja Obsługi i Konfiguracji ScreenWatcher

Dokumentacja opisuje proces uruchomienia serwera, konfiguracji klienta (Windows Edge Client) oraz zasady działania systemu ScreenWatcher w wersji przemysłowej.

---

## 1. Architektura Systemu

System składa się z dwóch głównych elementów:
1.  **Serwer (Backend):** Centralna baza danych i panel zarządzania. Przechowuje dane, liczy OEE i generuje wykresy.
2.  **Klient (Edge Client):** Aplikacja `.exe` uruchamiana na komputerach przy maszynach. "Patrzy" na ekran, zczytuje dane (OCR) i wysyła je do serwera.

Komunikacja odbywa się przez sieć (HTTP) lub za pomocą pendrive'a (**Tryb Offline**).

---

## 2. Przygotowanie Serwera (Pierwsze uruchomienie)

Zanim uruchomisz Agenta na maszynach, musisz przygotować serwer do odbioru danych.

### Krok 1: Rejestracja Maszyn
1.  Wejdź do Panelu Administratora: `http://<IP_SERWERA>:9000/admin/`.
2.  W sekcji **Registry** wybierz **Machines** -> **Add Machine**.
3.  Wypełnij **Code** (np. `M01`) oraz **Name** (np. "Frezarka 1"). Zapisz.
4.  Powtórz to dla wszystkich zestawów (np. od `M01` do `M08`).

### Krok 2: Pobranie Klucza API (Token)
1.  W Panelu Administratora przejdź do sekcji **Authtoken** -> **Tokens**.
2.  Kliknij **Add Token** i wybierz użytkownika (np. `operator` lub `admin`).
3.  Zapisz długi ciąg znaków (np. `3a1fcce...`). Będziesz go potrzebował w Konfiguratorze na każdym komputerze.

---

## 3. Konfiguracja Klienta na Windows (sw_configurator.exe)

Użyj tego programu, aby powiedzieć systemowi, co i jak ma czytać z ekranu.

### A. Ustawienia Połączenia i Pracy
*   **Kod Maszyny:** Wpisz unikalny kod zarejestrowany w Adminie (np. `M01`).
*   **Klucz API (Token):** Wklej klucz pobrany w kroku 2.
*   **URL Ingestora:** Zostaw domyślny (`http://localhost:9000/...`), jeśli backend jest na tym samym PC, lub wpisz adres IP serwera w fabryce.
*   **Interwał (s):** Określa, jak często program robi zrzut ekranu i wysyła dane. Standard to **14 sekund**.
*   **Wybierz Ekran:** Wybierz z listy monitor, który ma być śledzony. Program wyświetla rozdzielczość i informację, który ekran jest główny.
*   **Tryb Offline:** Zaznacz, jeśli komputer nie ma dostępu do sieci. Dane będą zapisywane do pliku `offline_data.jsonl` w folderze programu.

### B. Przechwytywanie Obrazu
*   **Capture Live:** Pobiera aktualny widok z wybranego monitora.
*   **Wczytaj z pliku:** Pozwala wczytać wcześniej zapisany zrzut ekranu (PNG/JPG) do ustawienia obszarów. Przydatne, gdy nie masz dostępu do maszyny "na żywo".
*   **Suwaki:** Jeśli obraz jest duży, użyj suwaków, aby przewinąć go w pionie lub poziomie. Prawy panel ustawień również posiada suwak, aby zmieścił się na mniejszych ekranach.

### C. Definiowanie Obszarów (ROIs)
1.  Kliknij i przeciągnij myszką na obrazie, aby zaznaczyć obszar (np. licznik sztuk).
2.  Wypełnij właściwości pola po prawej:
    *   **Nazwa / Klucz API:** Nazwa, pod jaką dane trafią do systemu (np. `counter`, `temperature`).
    *   **Typ:** `number` dla liczb, `status` dla stanów (PRACA/STOP), `text` dla dowolnego napisu.
    *   **Jednostka:** Wybierz z listy (np. `kg`, `bar`, `pcs`). Możesz zostawić puste – czytanie danych i tak zadziała.
    *   **Kategoria:** Domyślnie "General". Możesz zostawić bez zmian.
    *   **Transformacje:** Zaawansowane czyszczenie tekstu w formacie JSON. Przykłady:
        *   Tylko cyfry: `[{"type": "regex", "pattern": "\\d+"}]`
        *   Zamiana znaku: `[{"type": "replace", "old": ",", "new": "."}]`
        *   Jeśli nie potrzebujesz zmian, zostaw puste: `[]`.

**WAŻNE:** Po zakończeniu kliknij **ZAPISZ KONFIGURACJĘ**.

---

## 4. Praca Agenta (sw_agent.exe)

Po poprawnym zapisaniu konfiguracji, uruchom `sw_agent.exe`.

1.  Agent będzie działał w tle zgodnie z ustawionym interwałem.
2.  W oknie zobaczysz logi:
    *   `Data saved (ONLINE)` - dane wysłane do serwera.
    *   `Data saved (OFFLINE)` - dane dopisane do pliku `offline_data.jsonl`.

### Import danych z Pendrive'a (Gdy pracowałeś Offline)
Gdy masz już plik `offline_data.jsonl`:
1.  Zaloguj się do Admina na serwerze docelowym.
2.  Przejdź do **Telemetry** -> **Telemetry Points**.
3.  Kliknij przycisk **"Importuj dane Offline"** (prawy górny róg).
4.  Wybierz plik z pendrive'a i kliknij **"Rozpocznij Import"**. Dane zostaną automatycznie przeliczone na statystyki OEE.

---

## 5. Troubleshooting (Najczęstsze problemy)

1.  **Silnik OCR nie działa:** Kliknij "Sprawdź silnik OCR" w Konfiguratorze. Jeśli brakuje Tesseracta, program spróbuje go automatycznie zainstalować z wewnętrznych zasobów przy pierwszym uruchomieniu EXE.
2.  **Wywalanie przy zaznaczaniu:** Upewnij się, że używasz najnowszej wersji EXE (v2.2+), w której naprawiono błąd resetowania pól.
3.  **Brak danych na serwerze:** Sprawdź, czy klucz API (Token) jest poprawny oraz czy kod maszyny zgadza się z tym w Adminie.

---
*Aktualizacja dokumentacji: 8 stycznia 2026*