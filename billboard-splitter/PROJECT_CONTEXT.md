# Project Context: Billboard Splitter

## Overview
**Billboard Splitter** is a desktop application designed for the printing industry. It automates the process of splitting large billboard designs (PDF, JPG, TIFF) into printable tiles (bryty).

- **Location:** `~/cloud/billboard-splitter`
- **Primary Language:** Python 3.10+
- **GUI Framework:** Tkinter (with `ttkthemes`)

## Key Features
1.  **Splitting Engine:** Divides large files based on rows/cols with configurable overlaps and white stripes.
2.  **Output Formats:** Common sheet (all tiles on one page) or Separate files (one PDF per tile).
3.  **Markers:** Automatically adds registration marks (cross/line) and barcodes (QR/Code128) for print management.
4.  **Preview:** Real-time preview of input and output using `pdf2image` and `PyMuPDF`.
5.  **Localization:** Multi-language support (PL/EN and others via `lang_*.py`).

## Tech Stack
-   **Core:** `PyMuPDF` (fitz), `ReportLab` (PDF generation), `Pillow` (Image processing).
-   **GUI:** `tkinter`, `ttkthemes`.
-   **Distribution:** `PyInstaller` (builds single-file EXE).
-   **Utilities:** `qrcode`, `python-barcode`.

## Project Structure
-   `main.py`: Entry point, GUI initialization, threading for generation.
-   `splitter.py`: Core logic for slicing PDFs and rendering output.
-   `config.py`: Configuration management (`settings.json`).
-   `main_ui_*.py`: GUI tabs (Home, Settings, Help).
-   `lang_manager.py`: Localization logic.
-   `requirements.txt`: Python dependencies.

## Setup & Run
1.  **Environment:** `python -m venv .venv && source .venv/bin/activate`
2.  **Dependencies:** `pip install -r requirements.txt` (or use `bootstrap.py`)
3.  **Run:** `python main.py`
4.  **Tests/Benchmark:** `python benchmark.py`

## Development Notes
-   **No Interactive Tools:** Do not use `nano` or `vim`. Use `replace` or `write_file`.
-   **Logging:** Logs are stored in `logs/`.
-   **Build:** Use `pyinstaller` commands found in `README.md`.
