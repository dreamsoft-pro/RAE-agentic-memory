#fix_and_clean.py
import os
import shutil
import sys
from pathlib import Path

def clean_artifacts():
    """Usuwa zbędne katalogi i cache."""
    dirs_to_remove = [
        "rae_tests",
        ".pytest_cache",
        "apps/reranker-service/tests/__pycache__",
        "tests/__pycache__"
    ]
    
    project_root = Path.cwd()
    
    print(f"🧹 Czyszczenie projektu w: {project_root}")
    
    for dir_name in dirs_to_remove:
        dir_path = project_root / dir_name
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"   ✅ Usunięto: {dir_name}")
            except Exception as e:
                print(f"   ❌ Błąd podczas usuwania {dir_name}: {e}")
        else:
            print(f"   ℹ️  Nie znaleziono (to dobrze): {dir_name}")

    # Usunięcie __init__.py z testów rerankera, aby nie był traktowany jako pakiet podrzędny
    # co przy folderze z myślnikiem powoduje problemy.
    reranker_init = project_root / "apps/reranker-service/tests/__init__.py"
    if reranker_init.exists():
        os.remove(reranker_init)
        print("   ✅ Usunięto zbędny __init__.py w reranker-service/tests")

def fix_reranker_test():
    """Nadpisuje test rerankera poprawną metodą importu dla folderów z myślnikiem."""
    file_path = Path("apps/reranker-service/tests/test_main.py")
    
    # Upewnij się, że katalog istnieje
    file_path.parent.mkdir(parents=True, exist_ok=True)

    content = """
import sys
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# --- FIX IMPORTU DLA KATALOGU Z MYŚLNIKIEM ---
# Folder nazywa się 'reranker-service', więc nie można zrobić 'import apps.reranker_service'
# Musimy dodać ścieżkę bezpośrednio do sys.path
current_file = Path(__file__).resolve()
service_dir = current_file.parent.parent # apps/reranker-service
sys.path.insert(0, str(service_dir))

try:
    from main import app
except ImportError:
    # Fallback jeśli uruchamiane z innej lokalizacji
    sys.path.append(str(service_dir))
    from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_rerank_logic():
    # Sprawdzenie czy biblioteka ML jest dostępna (w CI może jej nie być)
    try:
        import sentence_transformers
    except ImportError:
        pytest.skip("Sentence Transformers not installed - skipping logic test")

    payload = {
        "query": "apple",
        "items": [
            {"id": "1", "text": "fruit red apple"},
            {"id": "2", "text": "car mechanic"}
        ]
    }
    
    response = client.post("/rerank", json=payload)
    assert response.status_code == 200
    data = response.json()
    items = data["items"]
    
    # Apple powinno mieć wyższy wynik (score) niż car dla zapytania "apple"
    # Zakładamy, że model działa poprawnie
    assert items[0]["id"] == "1"
"""
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    
    print("✅ Naprawiono plik: apps/reranker-service/tests/test_main.py")

if __name__ == "__main__":
    clean_artifacts()
    fix_reranker_test()
    print("\n🚀 Gotowe! Teraz uruchom: make test")