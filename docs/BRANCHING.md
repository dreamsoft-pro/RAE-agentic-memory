# Branch strategy (RAE)

- `main` – zawsze stabilny, gotowy do deploymentu. Merge tylko przez PR + zielony CI.
- `develop` – główny branch developerski, integruje feature branch'e.
- `release/x.y` – przygotowanie wydań, tylko bugfixy, dokumentacja i kosmetyka.
- `feature/*` – nowe funkcjonalności, zawsze z `develop`.
- `hotfix/*` – szybkie poprawki, zawsze z `main`.

Workflow:
1. Twórz `feature/*` z `develop`.
2. Po zakończeniu – PR do `develop`.
3. Przy freeze – utwórz `release/x.y` z `develop`.
4. Po testach – PR `release/x.y` → `main` (tag `vX.Y`) oraz `release/x.y` → `develop`.
5. Krytyczne bugfixy w `main` → `hotfix/*` → merge do `main` i `develop`.