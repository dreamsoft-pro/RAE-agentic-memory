#!/usr/bin/env python3
"""
Bootstrap aplikacji:
  • zakłada/aktualizuje .venv
  • instaluje requirements.txt
  • uruchamia main.py z wyciszoną konsolą (Windows) lub w tle (Unix)
"""

import os
import sys
import subprocess
from pathlib import Path
import venv
import logging

# === ANTY-MIGANIE KONSOLI (Windows) ===
if os.name == "nt":
    try:
        import ctypes
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd:
            # SW_HIDE = 0
            ctypes.windll.user32.ShowWindow(whnd, 0)
            ctypes.windll.kernel32.CloseHandle(whnd)
    except Exception:
        # Nie przerywaj uruchamiania, nawet jeśli ukrycie się nie powiedzie
        pass
# ======================================

BASE_DIR = Path(__file__).resolve().parent
VENV_DIR = BASE_DIR / ".venv"
REQ_FILE = BASE_DIR / "requirements.txt"
MAIN_FILE = BASE_DIR / "main.py"  # jeśli masz .pyw, zmień tu na main.pyw

# Logi bootstrapu (osobne od logów aplikacji)
LOG_DIR = (Path(sys.executable).parent if getattr(sys, "frozen", False) else BASE_DIR) / "logs"
LOG_DIR.mkdir(exist_ok=True)
BOOTSTRAP_LOG = LOG_DIR / "bootstrap.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(BOOTSTRAP_LOG, encoding="utf-8")]
)
log = logging.getLogger("bootstrap")

# Flagi/ustawienia okna dla subprocess (Windows)
CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0
DETACHED_PROCESS = 0x00000008 if os.name == "nt" else 0
CREATE_NEW_PROCESS_GROUP = 0x00000200 if os.name == "nt" else 0

def _startupinfo_hidden():
    """Zwraca startupinfo z ukrytym oknem (Windows)."""
    if os.name != "nt":
        return None
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0  # SW_HIDE
    return si


def ensure_venv() -> Path:
    """Tworzy .venv (jeśli brak) i instaluje wymagane paczki – bez żadnych okien konsoli."""
    if not VENV_DIR.exists():
        log.info("Tworzę izolowane środowisko .venv…")
        venv.create(VENV_DIR, with_pip=True)

    # Ścieżki do interpreterów w zależności od OS
    py_bin = VENV_DIR / ("Scripts" if os.name == "nt" else "bin")
    python = py_bin / ("python.exe" if os.name == "nt" else "python3")
    pythonw = py_bin / ("pythonw.exe" if os.name == "nt" else "python3")

    # Instalacja/aktualizacja zależności – z wyciszeniem do logu
    if REQ_FILE.exists():
        log.info("Instaluję/aktualizuję zależności z %s…", REQ_FILE)
        cmd = [str(python), "-m", "pip", "install", "--upgrade", "-r", str(REQ_FILE)]
        with open(BOOTSTRAP_LOG, "a", encoding="utf-8") as logf:
            proc = subprocess.run(
                cmd,
                cwd=BASE_DIR,
                stdout=logf,
                stderr=logf,
                stdin=subprocess.DEVNULL,
                startupinfo=_startupinfo_hidden(),
                creationflags=CREATE_NO_WINDOW,
                shell=False,
                check=False
            )
        if proc.returncode != 0:
            log.error("pip install zakończony kodem %s (sprawdź bootstrap.log)", proc.returncode)
            # nie przerywamy – aplikacja może działać bez części pakietów
        else:
            log.info("Zależności zainstalowane.")

    # Preferuj pythonw na Windows (brak konsoli)
    return pythonw if (os.name == "nt" and pythonw.exists()) else python


def launch_app(python: Path) -> None:
    """Uruchamia main.py bez konsoli (Windows) lub w nowej sesji (Unix)."""
    if not MAIN_FILE.exists():
        log.error("Brak pliku %s – przerywam.", MAIN_FILE)
        sys.exit(1)

    kwargs = {
        "cwd": BASE_DIR,
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "startupinfo": _startupinfo_hidden(),
        "shell": False,
    }

    cmd = [str(python), str(MAIN_FILE)]

    if os.name == "nt":
        # Pełny zestaw flag ukrywających okno i odłączających proces
        creation = CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
        kwargs["creationflags"] = creation
        try:
            subprocess.Popen(cmd, **kwargs)
            log.info("Aplikacja uruchomiona (Windows, ukryta).")
        except Exception as e:
            log.exception("Błąd przy uruchamianiu aplikacji: %s", e)
            sys.exit(1)
    else:
        # Unix: uruchom w nowej sesji (detached)
        try:
            subprocess.Popen(cmd, start_new_session=True, **kwargs)
            log.info("Aplikacja uruchomiona (Unix, detached).")
        except Exception as e:
            log.exception("Błąd przy uruchamianiu aplikacji: %s", e)
            sys.exit(1)


def main() -> None:
    log.info("Bootstrap start. BASE_DIR=%s", BASE_DIR)
    python = ensure_venv()
    log.info("Interpreter: %s", python)
    launch_app(python)
    log.info("Bootstrap koniec.")


if __name__ == "__main__":
    main()
