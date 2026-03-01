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

To create a standalone directory with all dependencies and the local LLM:

1.  **Install Dependencies**
    ```powershell
    pip install ".[dev]" huggingface_hub
    ```

2.  **Download Local LLM** (Required for bundling)
    ```powershell
    python ../scripts/download_llm.py
    ```

3.  **Build (ONEDIR Mode)**
    ```powershell
    pyinstaller --noconfirm rae-lite.spec
    ```

    The output will be in the `dist/RAE-Lite` folder. You can distribute this entire folder.

## 🤖 Assistant Mode (Order Entry Oracle)

The tool now includes a **Procedural Assistant Mode** that generates step-by-step instructions. 
For the best experience, it is recommended to have **Ollama** installed and running on your Windows machine:

1.  **Download Ollama:** [ollama.com](https://ollama.com)
2.  **Pull the model:** `ollama pull llama3:8b` (or another model of your choice, configurable in `server.py`)
3.  **Run Ollama:** Ensure the Ollama tray icon is visible.

If Ollama is not available, the tool will use **Designed Math Fallback** to synthesize instructions from document fragments.

## 🛠️ Configuration

Configuration is loaded from environment variables (prefix `RAE_LITE_`) or defaults.
- **Port:** 8765 (Default)
- **Data Dir:** `~/.rae-lite/data`

```