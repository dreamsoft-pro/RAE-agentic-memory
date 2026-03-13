import os
import sys
from datetime import datetime

# Określa katalog, w którym znajduje się ten plik
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lista folderów do przeszukania względem BASE_DIR
FOLDERS_TO_SCAN = [
    "",  # katalog główny
    "config",
    "core",
    "devices",
    "gui",
    "settings",
    "simulation",
    "tests",
    "utils"
]

# Pliki i foldery, które mają być pominięte
IGNORE_FILES = {
    "__init__.py",
    "setup_firewall.py",
    "test_tcp.py",
    "billboard-splitter.spec",
    "'main.spec",
    os.path.basename(__file__)  # ignoruje sam siebie
}

IGNORE_FOLDERS = {
    "zzz_info", "hooks", "icons", "input", "logs", "mysql_data",
    "opisy_wyjasniające", "output", "poppler", "venv", "build",
    "dist", "__pycache__"
}

# --- NOWE: biała lista plików językowych, które chcemy zachować ---
LANG_WHITELIST = {"lang_en.py"}

def collect_sources() -> None:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_filename = f"wszystkie-pliki-billboard_ciecie_{timestamp}.txt"
    output_path = os.path.join(BASE_DIR, output_filename)

    summary: list[tuple[str, int]] = []

    with open(output_path, "w", encoding="utf-8") as outfile:
        for folder in FOLDERS_TO_SCAN:
            folder_path = os.path.join(BASE_DIR, folder)
            if not os.path.isdir(folder_path):
                continue

            for dirpath, dirnames, filenames in os.walk(folder_path):
                # Pomijamy zdefiniowane foldery
                dirnames[:] = [d for d in dirnames if d not in IGNORE_FOLDERS]

                for fname in filenames:
                    # Pomiń nieobsługiwane rozszerzenia na wejściu
                    if fname.endswith(".txt"):
                        continue
                    if not (fname.endswith(".py") or fname.endswith(".json")):
                        continue

                    # Pomiń pliki globalnie ignorowane
                    if fname in IGNORE_FILES:
                        continue

                    # --- NOWE: ignoruj wszystkie pliki językowe poza lang_en.py ---
                    # Działa niezależnie od folderu, wystarczy nazwa pliku.
                    if fname.startswith("lang_") and fname.endswith(".py") and fname not in LANG_WHITELIST:
                        continue

                    full_path = os.path.join(dirpath, fname)
                    try:
                        with open(full_path, "r", encoding="utf-8") as infile:
                            lines = infile.readlines()
                        rel_path = os.path.relpath(full_path, BASE_DIR)
                        outfile.write(f"# Plik: {rel_path}\n")
                        outfile.write("".join(lines))
                        outfile.write("\n\n")
                        summary.append((rel_path, len(lines)))
                    except Exception as e:
                        outfile.write(f"# Błąd wczytywania pliku {fname}: {e}\n\n")

        # Podsumowanie
        outfile.write("# Podsumowanie liczby linii:\n")
        total_lines = sum(count for _, count in summary)
        for path, count in summary:
            outfile.write(f"{path} - {count} linii\n")
        outfile.write(f"RAZEM: {total_lines} linii\n")

    print(f"Zapisano plik: {output_path}")

if __name__ == "__main__":
    collect_sources()
