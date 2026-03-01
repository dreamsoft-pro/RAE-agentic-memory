# init_directories.py
import os
import sys
import shutil
# Usunięto import main_utils, bo logika get_base_dir jest powtórzona poniżej
import logging # <-- Dodano import
from lang_pl import LANG # <-- Dodano import (upewnij się, że importuje poprawny plik)

# Uzyskaj instancję loggera używaną w reszcie aplikacji
# WAŻNE: To zadziała poprawnie tylko jeśli logger jest już skonfigurowany
# (np. przez splitter.setup_logging() wywołane wcześniej w main.py lub przez logging.basicConfig()).
# Jeśli nie, logi z tego modułu mogą się nie pojawić w oczekiwanym miejscu.
logger = logging.getLogger('BillboardSplitter')

def initialize_directories():
    # Dla exe (frozen) używamy katalogu z exe, a nie sys._MEIPASS
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
        # Katalog z zasobami w trybie frozen (dla pliku przykładowego)
        bundled_dir = sys._MEIPASS
    else:
        # W trybie developerskim używamy katalogu, gdzie jest ten skrypt
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bundled_dir = base_dir # W trybie dev zasoby są tam gdzie kod

    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    logs_dir = os.path.join(base_dir, "logs")

    # Tworzymy katalogi, jeśli nie istnieją
    for d in [input_dir, output_dir, logs_dir]:
        if not os.path.exists(d):
            try:
                os.makedirs(d, exist_ok=True)
                # Zamiast print:
                logger.info(LANG["directory_created"].format(d))
            except Exception as e:
                # Zamiast print:
                logger.error(LANG["directory_creation_error"].format(d, e))

    # Kopiujemy przykładowy plik do katalogu input, jeśli go tam nie ma
    sample_filename = "bilboard3.pdf" # Upewnij się, że nazwa jest poprawna
    destination_sample = os.path.join(input_dir, sample_filename)

    # Ścieżka źródłowa zależy od trybu uruchomienia
    source_sample = os.path.join(bundled_dir, "input", sample_filename)

    # Kopiuj tylko jeśli źródło istnieje, a cel nie
    if not os.path.exists(destination_sample) and os.path.exists(source_sample):
        try:
            shutil.copyfile(source_sample, destination_sample)
            # Zamiast print:
            logger.info(LANG["sample_file_copied"].format(destination_sample))
        except Exception as e:
            # Zamiast print:
            logger.error(LANG["sample_file_copy_error"].format(e))
    # Usunięto blok else, który powielał logikę - teraz source_sample jest ustalane raz

# --- Koniec zmian ---