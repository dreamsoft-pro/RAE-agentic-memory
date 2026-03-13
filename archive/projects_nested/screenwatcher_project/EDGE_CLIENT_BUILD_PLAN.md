# Plan przygotowania pliku EXE dla Edge Client

## 1. Cel modułu
`edge_client` ma za zadanie:
- Pozwalać użytkownikowi na zdefiniowanie obszarów zainteresowania (ROI) na ekranie (Konfigurator).
- Cyklicznie wykonywać zrzuty ekranu, wycinać zdefiniowane obszary i odczytywać z nich dane za pomocą OCR (Agent).
- Przesyłać odczytane dane (tekst/liczby) do centralnego systemu ScreenWatcher przez API.

## 2. Rozbudowa Agenta (`edge_client/main.py`)
Obecny skrypt to tylko proof-of-concept. Należy dodać:
- Wczytywanie pliku `config.json` wygenerowanego przez konfigurator.
- Integrację z `pytesseract` do odczytu tekstu.
- Logikę wysyłania wyników do endpointu `/api/collector/telemetry/`.
- Parametryzację (interwał skanowania, adres serwera).

## 3. Przygotowanie środowiska do kompilacji
- Instalacja `PyInstaller` w wirtualnym środowisku.
- Upewnienie się, że wszystkie zależności z `edge_client/requirements.txt` są zainstalowane.
- Przygotowanie silnika Tesseract OCR (instrukcja dołączenia binariów).

## 4. Pakowanie (PyInstaller)
Stworzenie dwóch osobnych plików wykonywalnych:
1. **`sw_configurator.exe`** - na bazie `configurator.py` (GUI PyQt6).
2. **`sw_agent.exe`** - na bazie rozbudowanego `main.py` (proces konsolowy/tło).

Ustawienia kompilacji:
- `--onefile` - dla łatwej dystrybucji.
- `--noconsole` - dla konfiguratora.
- `--add-data` - dołączenie niezbędnych zasobów (ikony, ewentualnie binaria Tesseract).

## 5. Weryfikacja
- Test uruchomienia na "czystym" systemie Windows.
- Test komunikacji z lokalnym serwerem ScreenWatcher.
