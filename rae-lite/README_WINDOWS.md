# RAE-Lite for Windows

RAE-Lite is the standalone desktop client for RAE (Reflective Agentic Engine). It runs a local lightweight memory core (using SQLite) and provides a System Tray interface.

## 🚀 Requirements

- **Python 3.10+**
- Windows 10/11

## 📦 Installation on Windows

1.  **Clone the Repository** (if not already done)
    ```powershell
    git clone https://github.com/dreamsoft-pro/RAE-agentic-memory.git
    cd RAE-agentic-memory\rae-lite
    ```

2.  **Install Dependencies**
    It is recommended to use a virtual environment.
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -e .
    ```
    *Note: `rae-core` is a dependency and must be available.*

## 🏃 Running the App

```powershell
# Run from command line
rae-lite
```

Or directly via Python:
```powershell
python -m rae_lite.main
```

## 🔨 Building EXE (PyInstaller)

To create a standalone `.exe` file:

1.  **Install Dev Dependencies**
    ```powershell
    pip install ".[dev]"
    ```

2.  **Build**
    ```powershell
    pyinstaller --noconfirm --onefile --windowed --name "RAE-Lite" --icon "assets/icon.ico" --add-data "rae_lite;rae_lite" rae_lite/main.py
    ```

    The output will be in the `dist/` folder.

## 🛠️ Configuration

Configuration is loaded from environment variables (prefix `RAE_LITE_`) or defaults.
- **Port:** 8765 (Default)
- **Data Dir:** `~/.rae-lite/data`

```