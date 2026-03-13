#!/usr/bin/env python3
import zipfile
import os
import shutil
from pathlib import Path

INPUT_ZIP = "RAE_PORTABLE_STATE.zip"

def run_import():
    if not os.path.exists(INPUT_ZIP):
        print(f"❌ Błąd: Nie znaleziono pliku {INPUT_ZIP} w bieżącym katalogu.")
        return

    print(f"🚀 Rozpoczynam import stanu RAE z {INPUT_ZIP}...")
    
    with zipfile.ZipFile(INPUT_ZIP, 'r') as zipf:
        # Wyodrębniamy pliki
        for member in zipf.infolist():
            if member.filename == "import_rae_session.py":
                continue
                
            print(f"  -> Przywracam: {member.filename}")
            
            # Tworzymy katalogi jeśli nie istnieją
            target_path = Path(member.filename)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Wypakowujemy
            with zipf.open(member) as source, open(member.filename, "wb") as target:
                shutil.copyfileobj(source, target)

    print("
✅ Stan RAE został odtworzony!")
    print("---------------------------------------------------------------")
    print("Teraz możesz uruchomić bootstrap:")
    print("python3 scripts/bootstrap_session.py")
    print("---------------------------------------------------------------")

if __name__ == "__main__":
    run_import()
