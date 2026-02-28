# 🚑 PLAN NAPRAWY LUMINY (System 4.16 Recovery)

## 🚨 Diagnoza (Sesja 10 Lutego 2026)
Wdrożenie "Safety Net" (bezpiecznika) w kodzie było poprawne, ale ujawniło **krytyczną degradację środowiska na Node 1 (Lumina)**:

1.  **Zniknięcie Modeli ONNX**:
    - Log: `reranker_model_missing path=.../models/cross-encoder/model.onnx`
    - Skutek: System działa bez "Neural Scalpel" (rerankera), co drastycznie obniża precyzję (MRR 0.15 zamiast 1.0).
    - Przyczyna: Prawdopodobnie `rsync` nadpisał katalog `models/` stanem lokalnym (gdzie te pliki mogą być w `.gitignore`) lub brak ich w repozytorium.

2.  **Uszkodzony Benchmark 100k**:
    - Błąd: `ScannerError ... industrial_100k.yaml` (ucięty plik).
    - Skutek: Niemożność weryfikacji skali.
    - Przyczyna: Przerwany przesył pliku lub błąd edycji.

3.  **Niedopasowanie Wektorów**:
    - Logi wskazują próbę użycia `['nomic', 'dense']`. Jeśli kolekcja Qdrant na Luminie nie ma tych nazwanych wektorów (lub ma inne wymiary), wyszukiwanie wektorowe zwraca śmieci lub 0.

---

## 🛠️ Stan Infrastruktury (Aktualizacja: 10 Lutego 2026)

✅ **Krok 1: Odbudowa Modeli** - POTWIERDZONE. Modele ONNX są obecne na Luminie.
✅ **Krok 2: Naprawa Plików Danych** - POTWIERDZONE. Benchmark 100k został poprawiony.
✅ **Krok 3: Weryfikacja Qdrant** - ZAKOŃCZONE.

---

## 🚀 Cel: Silicon Oracle 40.0
Przechodzimy do implementacji ulepszeń jakościowych (System 40.0) bezpośrednio na Luminę.
