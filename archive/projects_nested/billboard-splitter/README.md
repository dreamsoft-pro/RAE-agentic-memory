# Billboard Splitter

Billboard Splitter to narzędzie do **cięcia dużych projektów billboardowych** (PDF/JPG/TIFF) na bryty oraz generowania wyjść w postaci:
- jednego **wspólnego arkusza** (common sheet),
- **osobnych plików** PDF dla każdego brytu,
- lub **obie opcje jednocześnie**.

Aplikacja ma GUI (Tkinter + ttk/ttkthemes), szybkie podglądy wejścia/wyjścia, profile ustawień, kody (QR/Code128) i znaczniki rejestracyjne. Wewnątrz wykorzystuje m.in. **PyMuPDF (fitz)** do szybkiego łączenia i renderowania PDF oraz **ReportLab/Pillow** do rysowania elementów pomocniczych.

---

## Spis treści

1. [Wymagania](#wymagania)
2. [Instalacja i uruchomienie (Windows)](#instalacja-i-uruchomienie-windows)
3. [Instalacja i uruchomienie (Linux)](#instalacja-i-uruchomienie-linux)
4. [Szybki start](#szybki-start)
5. [Ustawienia i profile](#ustawienia-i-profile)
6. [Kody (QR/Barcode) i znaczniki rejestracyjne](#kody-qrbarcode-i-znaczniki-rejestracyjne)
7. [Podgląd wejścia i wyjścia](#podgląd-wejścia-i-wyjścia)
8. [Tryby wyjścia](#tryby-wyjścia)
9. [Budowa pliku EXE (PyInstaller)](#budowa-pliku-exe-pyinstaller)
10. [Benchmark i profilowanie](#benchmark-i-profilowanie)
11. [Licencjonowanie](#licencjonowanie)
12. [Rozwiązywanie problemów](#rozwiązywanie-problemów)
13. [Struktura repo i główne pliki](#struktura-repo-i-główne-pliki)
14. [Wsparcie](#wsparcie)

---

## Wymagania

- Python 3.10+ (zalecane)
- System: Windows 10/11 lub Linux (x86_64)
- Biblioteki z `requirements.txt` (instalowane automatycznie przez `bootstrap.py` lub ręcznie – patrz niżej)
- **Dla podglądu przez pdf2image (miniatury)** na Linuxie wymagane jest `poppler-utils`

Minimalny zestaw pakietów (pełna lista w `requirements.txt` w repo):
- PyMuPDF (fitz), Pillow, ReportLab, pdf2image, pypdf/PyPDF2, python-barcode, qrcode, ttkthemes, svglib, tinycss2, cssselect2 itp.

> Uwaga: Aplikacja korzysta z obu dróg renderowania miniatur PDF (pdf2image + PyMuPDF) aby zapewnić szybkość i kompatybilność.

---

## Instalacja i uruchomienie (Windows)

### 1) Klon repozytorium / rozpakowanie paczki
```powershell
cd C:\path\to\
git clone https://github.com/<twoje-repo>/billboard-splitter.git
cd billboard-splitter
```

### 2) Utwórz i aktywuj wirtualne środowisko
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Zainstaluj zależności
Najprościej:
```powershell
python bootstrap.py
```
To utworzy/uzupełni `.venv` i doinstaluje wymagania z `requirements.txt`.
Alternatywnie ręcznie:
```powershell
pip install -r requirements.txt
```

### 4) Uruchom aplikację
```powershell
python main.py
```

---

## Instalacja i uruchomienie (Linux)

```bash
git clone https://github.com/<twoje-repo>/billboard-splitter.git
cd billboard-splitter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# dla miniatur z pdf2image:
sudo apt update && sudo apt install -y poppler-utils
python3 main.py
```

---

## Szybki start

1. **Plik wejściowy** – w zakładce *Home* wskaż plik PDF/JPG/TIFF (skala projektów zwykle 1:10).
2. **Ustaw podział** – wprowadź liczbę wierszy/kolumn, zakładkę/zakładkę białą (*overlap* / *white stripe*).
3. **Wybierz układ** – *Vertical* lub *Horizontal* (wpływa m.in. na położenie linii separacyjnych).
4. **Typ wyjścia** – *Common sheet*, *Separate files* lub *Both*.
5. (Opcjonalnie) **Znaczniki** i **kody** – włącz i skonfiguruj w zakładce *Settings*.
6. **Generate PDF** – wyniki trafią do folderu *output* (lub wskazanego).

---

## Ustawienia i profile

- Globalne ustawienia są ładowane/zapisywane w `settings.json` (tworzony automatycznie w katalogu aplikacji).
- Profile użytkownika są w `profiles.json` i można je: zapisać, wczytać, usunąć z poziomu GUI.
- Kluczowe pola (wybrane):
  - `split_rows`, `split_cols` – siatka cięcia,
  - `overlap`, `white_stripe`, `add_white_to_overlap` – parametry zakładki,
  - `layout` – `layout_vertical` lub `layout_horizontal`,
  - `output_type` – `output_common_sheet` / `output_separate_files` / `output_both`,
  - `enable_reg_marks`, `registration_mark_type` – znaczniki rejestracyjne,
  - `enable_barcode`, `barcode_type` – `code_qr` albo `code_barcode`,
  - `graphic_settings.code_settings` – precyzyjne pozycjonowanie/rotacja/skala kodów (osobno dla układu i trybu wyjścia),
  - `margin_*`, `sep_line_*`, `slice_gap` – marginesy, linie separacyjne, odstępy.

> W trybie „zamrożonym” (EXE) domyślne katalogi `input`, `output`, `logs` są tworzone obok pliku wykonywalnego.  

---

## Kody (QR/Barcode) i znaczniki rejestracyjne

- Generowanie QR i Code128 jest w pełni konfigurowalne (skala, offset, rotacja, kotwica rogu).
- Źródło treści kodu domyślnie pochodzi z nazwy pliku + nazwy brytu (`generate_barcode_data(...)`).
- Znaczniki rejestracyjne (krzyż/linia) mają odseparowane szerokości linii białej/czarnej oraz rozmiary w cm.

---

## Podgląd wejścia i wyjścia

- Podgląd **wejścia** korzysta z `pdf2image` (i `poppler`), aby szybko generować miniatury.
- Podgląd **wyjścia** korzysta z **PyMuPDF**; dla wielu plików rysowana jest mozaika (siatka 3×3).  
- Render działa w wątku roboczym, aby nie blokować GUI; na płótnach widać progres.

---

## Tryby wyjścia

- **Common sheet** – wszystkie bryty na jednym arkuszu (horyzontalnym lub wertykalnym).
- **Separate files** – każdy bryt w osobnym PDF; nazwy zawierają sufiksy z indeksami.
- **Both** – generuje arkusz wspólny oraz osobne pliki.

---

## Budowa pliku EXE (PyInstaller)

Z wiersza poleceń (w aktywnym `.venv`):
```powershell
pyinstaller --onefile --noconsole --name billboard-splitter ^
  --add-data "settings.json;." ^
  --add-data "profiles.json;." ^
  --add-data "billboard3.pdf;input" ^
  --add-data "poppler\\bin;poppler\\bin" ^
  --icon "icons/billboard_icon.ico" main.py
```
Warianty:
- `--console` zamiast `--noconsole` – aplikacja konsolowa,
- `--onedir` zamiast `--onefile` – katalog z zależnościami obok EXE.

> Ikona aplikacji: `icons/billboard_icon.ico`. W pliku wynikowym zasoby `settings.json`, `profiles.json` i plik przykładowy są dołączone.

---

## Benchmark i profilowanie

Moduł `benchmark.py` uruchamia zestaw scenariuszy (separate/common) na plikach testowych i zapisuje wyniki oraz profil cProfile (do `profiling_results_final.txt`).  
Uruchomienie:
```bash
python benchmark.py
```

---

## Licencjonowanie

- Licencja jest powiązana z HWID urządzenia; weryfikacja odbywa się z użyciem klucza publicznego osadzonego w aplikacji.
- Generator licencji (narzędzie pomocnicze) wymaga prywatnego klucza RSA w PEM.

---

## Rozwiązywanie problemów

- **Miniatury PDF nie działają na Linux** – doinstaluj `poppler-utils`.
- **Brak ikon/zasobów w EXE** – sprawdź ścieżki w `--add-data` (na Windows używamy separatora `;`, nie `:`).
- **Wolny podgląd** – zmniejsz DPI miniatur lub wyłącz siatkę 3×3 dla wielu plików.
- **Błędy zapisu** – zweryfikuj uprawnienia do katalogu `output` i `logs`.
- **Komunikaty o błędach** – sprawdź pliki w `logs`. Logi mają dzienną rotację i poziom konfigurowalny w *Settings*.

---

## Struktura repo i główne pliki

- `main.py` – uruchamia GUI i orkiestruje pracę.
- `splitter.py` – logika cięcia/generowania PDF (PyMuPDF/ReportLab).
- `barcode_qr.py` – generowanie QR/Code128 w pamięci (PNG/SVG) i rysowanie na PDF.
- `config.py` – domyślne ustawienia + load/save `settings.json` (w trybie EXE ustawia katalogi obok binarki).
- `init_directories.py` – tworzenie `input`, `output`, `logs` oraz kopiowanie pliku przykładowego.
- `lang_*.py` + `lang_manager.py` – warstwa tłumaczeń (PL/EN).
- `benchmark.py` – testy wydajności i profilowanie.
- `bootstrap.py` – automatyczne `.venv` + `pip install -r requirements.txt` + bezgłośny start.
- `requirements.txt` – lista zależności.
- `profiles.json` / `settings.json` – konfiguracje użytkownika.

---

## Wsparcie

- E‑mail: **tech@printworks.pl** (dni robocze 8–16)
- Zgłoszenia błędów i propozycje: Issues w repozytorium

