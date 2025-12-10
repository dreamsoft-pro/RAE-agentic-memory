# 🚀 SESSION START - Instrukcja Rozpoczynania Sesji AI Agenta

> **⏱️ Czas: 15 minut** | **🔴 Status: MANDATORY - OBOWIĄZKOWE PRZED KAŻDĄ SESJĄ**

---

## 📖 KROK 1: Przeczytaj Krytyczne Dokumenty (10 minut)

Przeczytaj dokumenty w tej **DOKŁADNEJ** kolejności:

| # | Dokument | Czas | Priorytet | Co zawiera |
|---|----------|------|-----------|------------|
| 1 | **CRITICAL_AGENT_RULES.md** | 5 min | 🔴 CRITICAL | 10 obowiązkowych zasad które NIE MOGĄ być złamane |
| 2 | **AI_AGENT_MANIFEST.md** | 3 min | 🔴 CRITICAL | Uniwersalna nawigacja i hierarchia dokumentacji |
| 3 | **AUTONOMOUS_OPERATIONS.md** | 2 min | 🔴 CRITICAL | Lista operacji które wykonujesz BEZ pytania |

### Dlaczego ta kolejność?

1. **CRITICAL_AGENT_RULES.md** - Podstawowe zasady bezpieczeństwa i workflow
2. **AI_AGENT_MANIFEST.md** - Mapa całej dokumentacji i jak się poruszać
3. **AUTONOMOUS_OPERATIONS.md** - Jak pracować AUTONOMICZNIE bez blokowania użytkownika

---

## 🔍 KROK 2: Sprawdź Stan Projektu (3 minuty)

Uruchom te komendy aby zrozumieć kontekst:

```bash
# 1. Status brancha
git status
git branch -a

# 2. Ostatnie zmiany (10 commitów)
git log --oneline -10

# 3. Stan CI/CD (ostatnie 5 runów)
gh run list --limit 5

# 4. Aktualna lokalizacja
pwd
ls -la
```

### Zrozum kontekst:

- **Na jakim branchu jesteś?** (feature/develop/release/main)
- **Czy są uncommitted changes?**
- **Czy CI jest zielone czy czerwone?**
- **Jaki był ostatni commit?**

---

## 🎯 KROK 3: Zidentyfikuj Typ Zadania (2 minuty)

Określ jaki typ pracy będziesz wykonywać:

| Typ Zadania | Branch | Testowanie | Przykład |
|-------------|--------|------------|----------|
| **Nowy Feature** | `feature/*` | TYLKO nowy kod (--no-cov) | Dodaj cache service |
| **Bug Fix** | `feature/*` lub `hotfix/*` | TYLKO zmieniony kod | Napraw null pointer |
| **Refactoring** | `feature/*` | Full tests lokalnie | Przenieś do repo pattern |
| **Dokumentacja** | `feature/*` | SKIP testy (tylko lint) | Zaktualizuj README |
| **Release** | `release/*` | Full tests + integration | Stabilizacja v1.2.0 |

---

## ⚡ KROK 4: Rozpocznij Pracę AUTONOMICZNIE

Po przeczytaniu dokumentów i zrozumieniu kontekstu:

### ✅ NIE PYTAJ o:

- Czy mogę utworzyć plik/katalog?
- Czy mam dodać testy?
- Którego wzorca użyć? (użyj templates z `.ai-templates/`)
- Czy mogę commitować?
- Czy mogę pushować na feature branch?
- Czy mogę mergować feature → develop?

### ❓ PYTAJ TYLKO o:

- **Architektura**: Wiele równie dobrych podejść
- **Breaking changes**: Zmiany łamiące API
- **Biznes**: Niejasne wymagania lub decyzje produktowe
- **Ryzyko**: Force push, usuwanie danych, zmiany w prod

### 🔄 Standardowy Workflow (Autonomiczny):

```
1. Otrzymaj zadanie od użytkownika
2. [CISZA - nie pytaj o pozwolenie na standardowe rzeczy]
3. Przeczytaj niezbędne pliki (PROJECT_STRUCTURE.md, CONVENTIONS.md)
4. Dla non-trivial features: Stwórz design document
5. Implementuj używając templates z .ai-templates/
6. Testuj zgodnie z branchem i typem zmiany
7. Format + lint: make format && make lint
8. Commit z conventional message
9. Push (jeśli feature branch)
10. RAPORTUJ wynik użytkownikowi
11. NIE pytaj "czy mogę kontynuować?" - po prostu kontynuuj
```

---

## 🗺️ QUICK REFERENCE CARD

Wydrukuj i trzymaj widoczne podczas pracy:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RAE AGENT QUICK REFERENCE                         │
├─────────────────────────────────────────────────────────────────────┤
│  GIT WORKFLOW (4-fazowy):                                           │
│    feature/* → develop → release → main                             │
│                                                                      │
│  TESTING:                                                            │
│    Feature:  Test ONLY new code (pytest --no-cov)                  │
│    Develop:  Test EVERYTHING (make test-unit) - MANDATORY!         │
│    Release:  Full tests + integration + approval                    │
│    Main:     ŚWIĘTY - tylko merge z release przez PR               │
│                                                                      │
│  AUTONOMIA:                                                          │
│    ✅ Twórz pliki/katalogi bez pytania                              │
│    ✅ Używaj templates z .ai-templates/                             │
│    ✅ Commituj i pushuj na feature/develop                          │
│    ✅ Format/lint przed każdym commitem                             │
│    ❌ NIE pytaj o oczywiste rzeczy                                  │
│                                                                      │
│  BEZPIECZEŃSTWO:                                                     │
│    ⚠️  ZAWSZE tenant_id w SQL queries                               │
│    ⚠️  NIGDY nano/vim/less/git -i (interactive commands)            │
│    ⚠️  NIGDY force push na main/release                             │
│                                                                      │
│  TESTY JAKO KONTRAKT:                                                │
│    ❌ Test fails → Fix CODE, not test                               │
│    ✅ Test correctly describes expected behavior                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Dodatkowe Dokumenty (Wg Potrzeby)

Po przeczytaniu obowiązkowych, czytaj wg potrzeby:

| Sytuacja | Dokument | Kiedy czytać |
|----------|----------|--------------|
| Dodaję nowy feature | `PROJECT_STRUCTURE.md` | Gdzie umieścić pliki |
| | `CONVENTIONS.md` | Jak napisać kod |
| | `.ai-templates/README.md` | Które template użyć |
| Zmieniam testy | `docs/AGENTS_TEST_POLICY.md` | Filozofia testów |
| Pracuję z git | `BRANCH_STRATEGY.md` | Szczegóły workflow |
| | `docs/BRANCHING.md` | Git commands |
| Tworzę PR | `CONTRIBUTING.md` | Proces contribution |
| Publiczny PR | `PUBLIC_REPO_STRATEGY.md` | Zasady dla external PR |

---

## 🎓 Przykład - Prawidłowy Start Sesji

```
User: "Dodaj cache service z Redis"

Agent: [CISZA - czyta dokumenty]
       1. ✅ Przeczytał CRITICAL_AGENT_RULES.md (5 min)
       2. ✅ Przeczytał AI_AGENT_MANIFEST.md (3 min)
       3. ✅ Przeczytał AUTONOMOUS_OPERATIONS.md (2 min)
       4. ✅ Sprawdził git status: branch develop, clean
       5. ✅ Sprawdził CI: ostatni run PASSED
       6. ✅ Przeczytał PROJECT_STRUCTURE.md - gdzie umieścić service
       7. ✅ Przeczytał CONVENTIONS.md - wzorzec Service Layer

Agent: [Rozpoczyna pracę AUTONOMICZNIE - BEZ pytania]
       1. ✅ git checkout -b feature/add-cache-service
       2. ✅ cp .ai-templates/service_template.py services/cache_service.py
       3. ✅ [Implementacja cache service z DI]
       4. ✅ cp .ai-templates/test_template.py tests/services/test_cache_service.py
       5. ✅ [Implementacja testów]
       6. ✅ pytest --no-cov tests/services/test_cache_service.py
       7. ✅ make format && make lint
       8. ✅ git add .
       9. ✅ git commit -m "feat(services): add Redis cache service with DI"
       10. ✅ git push origin feature/add-cache-service

Agent: "Zaimplementowałem cache service z pełnym pokryciem testami.

        Rezultaty:
        - ✅ CacheService w services/cache_service.py
        - ✅ 12 testów w tests/services/test_cache_service.py (12/12 PASSED)
        - ✅ Dependency Injection pattern
        - ✅ Lint: PASSED
        - ✅ Format: PASSED
        - ✅ Pushed to feature/add-cache-service

        Gotowe do merge na develop."
```

---

## 🚫 Przykład - NIEPRAWIDŁOWY Start Sesji

```
User: "Dodaj cache service"

Agent: "Czy mam utworzyć nowy plik?"              # ❌ ZŁE!
User: "Tak"
Agent: "Gdzie go umieścić?"                       # ❌ ZŁE! Przeczytaj PROJECT_STRUCTURE.md
User: "W services/"
Agent: "Czy mam dodać testy?"                     # ❌ ZŁE! Zawsze dodaj testy
User: "Tak"
Agent: "Jakiego wzorca użyć?"                     # ❌ ZŁE! Użyj templates
User: "Repository pattern"
Agent: "Czy mogę teraz commitować?"               # ❌ ZŁE! Commituj autonomicznie
User: "Tak"

[15 minut zmarnowane na pytania o oczywiste rzeczy]
```

---

## ⏱️ Podsumowanie Timeline

```
┌────────────────┬──────────────────────────────────────────┐
│ Czas           │ Czynność                                 │
├────────────────┼──────────────────────────────────────────┤
│ 0:00 - 0:05    │ Czytaj CRITICAL_AGENT_RULES.md          │
│ 0:05 - 0:08    │ Czytaj AI_AGENT_MANIFEST.md             │
│ 0:08 - 0:10    │ Czytaj AUTONOMOUS_OPERATIONS.md         │
│ 0:10 - 0:13    │ Sprawdź git status, CI, kontekst        │
│ 0:13 - 0:15    │ Zidentyfikuj typ zadania                │
│ 0:15+          │ ROZPOCZNIJ PRACĘ AUTONOMICZNIE          │
└────────────────┴──────────────────────────────────────────┘
```

---

## ✅ Checklist - Gotowość do Pracy

Przed rozpoczęciem implementacji, potwierdź:

- [ ] ✅ Przeczytałem CRITICAL_AGENT_RULES.md (10 zasad)
- [ ] ✅ Przeczytałem AI_AGENT_MANIFEST.md (nawigacja)
- [ ] ✅ Przeczytałem AUTONOMOUS_OPERATIONS.md (co robić bez pytania)
- [ ] ✅ Sprawdziłem git status i CI
- [ ] ✅ Zidentyfikowałem typ zadania (feature/bugfix/docs/release)
- [ ] ✅ Wiem na jakim branchu pracuję
- [ ] ✅ Rozumiem że NIE pytam o standardowe operacje
- [ ] ✅ Gotowy do pracy AUTONOMICZNEJ

---

## 🆘 Co Robić Gdy...

| Sytuacja | Działanie |
|----------|-----------|
| Nie wiem gdzie umieścić plik | Przeczytaj `PROJECT_STRUCTURE.md` - NIE pytaj |
| Nie wiem jakiego wzorca użyć | Przeczytaj `CONVENTIONS.md` + użyj `.ai-templates/` - NIE pytaj |
| Testy failują | Popraw CODE, nie test (chyba że test jest błędny) |
| CI jest czerwone na develop | Popraw na develop, NIE merguj do main |
| Potrzebuję approval | Tylko dla release→main i main merges |
| Naprawdę nie wiem co robić | TERAZ możesz zapytać użytkownika |

---

## 🎯 Success Metrics

Wiesz że dobrze rozpocząłeś sesję gdy:

- ✅ Spędziłeś 15 minut na czytaniu dokumentacji
- ✅ NIE zadałeś żadnych "oczywistych" pytań
- ✅ Zacząłeś od `git checkout -b feature/...`
- ✅ Użyłeś templates z `.ai-templates/`
- ✅ Testowałeś zgodnie z branchem
- ✅ Scommitowałeś z conventional message
- ✅ Raportowałeś wynik, nie pytałeś "czy mogę kontynuować?"

---

**Wersja**: 1.0.0
**Data**: 2025-12-10
**Status**: 🔴 MANDATORY - Obowiązkowe przed każdą sesją
**Ostatnia aktualizacja**: 2025-12-10

**Pamiętaj**: Te 15 minut czytania zaoszczędzi godziny na zadawaniu pytań i poprawkach!
