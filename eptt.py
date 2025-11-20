import os
from pathlib import Path
from gitignore_parser import parse_gitignore

def export_project(root_dir: str, output_file: str):
    root_path = Path(root_dir).resolve()

    # Wczytaj i sparsuj .gitignore
    gitignore_file = root_path / ".gitignore"
    if gitignore_file.exists():
        matches = parse_gitignore(str(gitignore_file))
    else:
        # jeśli nie ma gitignore – nic nie ignorujemy
        matches = lambda p: False

    with open(output_file, "w", encoding="utf-8") as out:
        for path in sorted(root_path.rglob("*")):
            # pomiń katalogi
            if path.is_dir():
                continue

            # ścieżka relatywna
            rel_path = path.relative_to(root_path)

            # pomijamy pliki ignorowane
            if matches(str(rel_path)):
                continue

            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                # np. plik binarny – pomijamy
                continue

            out.write(f"# {rel_path}\n")
            out.write(content)
            out.write("\n\n")

    print(f"Zapisano pliki do {output_file}")


if __name__ == "__main__":
    # Przykład użycia:
    export_project(
        root_dir=".",                  # katalog projektu
        output_file="project_dump.txt" # plik wynikowy
    )
