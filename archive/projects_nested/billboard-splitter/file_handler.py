# file_handler.py
import os

def load_file(file_path):
    if not os.path.exists(file_path):
        # Poprawiona wersja na przyszłość
        raise FileNotFoundError(f"File not found: {file_path}")
    return file_path
