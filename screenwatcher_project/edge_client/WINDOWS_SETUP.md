# Instrukcja uruchomienia Edge Client na Windows (przez Tailscale)

Ten klient służy do zbierania danych z ekranu (OCR) i wysyłania ich do serwera ScreenWatcher działającego na Linuxie.

## Wymagania
1. Python 3.10+ zainstalowany na Windows.
2. Połączenie Tailscale aktywne (dostęp do 100.66.252.117).
3. (Opcjonalnie) Tesseract OCR zainstalowany (jeśli planujesz używać OCR).

## Instalacja

1. Otwórz terminal (PowerShell lub CMD) w tym katalogu.
2. Utwórz wirtualne środowisko (opcjonalnie, ale zalecane):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Zainstaluj zależności:
   ```powershell
   pip install -r requirements.txt
   ```

## Konfiguracja

1. Przy pierwszym uruchomieniu zostanie utworzony plik `config.json`.
2. Otwórz `config.json` i ustaw:
   - `api_url`: `"http://100.66.252.117:9000/api/collector/ingest/"`
   - `machine_code`: Unikalny kod tej maszyny (np. `"WIN_CLIENT_01"`).

## Uruchomienie

Uruchom aplikację komendą:
```powershell
python main.py
```

## Konfiguracja Obszarów (ROI)

Aby zdefiniować obszary do skanowania, uruchom konfigurator (jeśli dostępny) lub edytuj `config.json` w sekcji `rois`.

Przykład ROI:
```json
{
    "name": "speed",
    "x": 100, "y": 200, "w": 50, "h": 30,
    "type": "number"
}
```
