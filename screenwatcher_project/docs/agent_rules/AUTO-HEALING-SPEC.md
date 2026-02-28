📄 3. AUTO-HEALING-SPEC.md
Specification for Automated CI Repair Using AI Agents

Version: 1.0

1. Cel dokumentu

Dokument definiuje, jak działa Auto-Healing CI – mechanizm, w którym CI generuje:

pełny kontekst problemu,

zakres zmian,

PR z poprawką przygotowany przez AI.

2. Jak działa Auto-Healing CI
2.1. Zdarzenie wyzwalające

Auto-Healing może być uruchomiony przez:

warning (wbrew Zero Warnings),

flaky test,

drift performance,

błąd lintera,

błąd kompilacji,

naruszenie zasad bezpieczeństwa.

2.2. Mechanizm CI przygotowuje paczkę kontekstu

Paczka zawiera:

diff ostatniego commit,

logi CI,

treść wyjątku lub błędu,

snapshot metryk,

pliki powiązane z błędem,

wskazówki z Quality Pattern.

Format np. JSON:

{
  "type": "warning",
  "file": "src/core/module.py",
  "line": 42,
  "message": "deprecated call",
  "context_files": ["tests/test_module.py"],
  "metrics": {...}
}

2.3. Agent tworzy PR

Zgodnie z AGENT-GUIDELINES.md.

2.4. Review człowieka

obowiązkowy,

PR może być scalony dopiero po zaakceptowaniu.

3. Zakres napraw możliwych do auto-poprawy

Agent może:

poprawiać formatowanie,

poprawiać warningi,

stabilizować testy,

optymalizować kod niekrytyczny,

dodawać brakujące walidacje,

poprawiać wydajność, jeśli testy przechodzą.

Agent NIE może:

zmieniać API,

zmieniać zachowania biznesowego,

zmieniać logiki bezpieczeństwa.

4. Tryby pracy Auto-Healing
Mode A – Suggest Only

Agent proponuje poprawkę, ale PR tworzy człowiek.

Mode B – Full Auto-PR

Agent tworzy PR automatycznie (zalecane).

Mode C – Auto-PR + Auto-Assign Maintainer

PR automatycznie przypisany do odpowiedniej osoby.

5. Integracja z CI/CD

Każdy PR od AI:

przechodzi te same testy,

musi spełnić ZERO DRIFT,

nie może wprowadzać warningów,

musi przejść SAST/DAST (jeśli dotyczy).