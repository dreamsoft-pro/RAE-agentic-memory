📄 AUTO-DOCS-SPEC.md
Automatic Documentation & Knowledge Flow Specification

Version: 1.0

1. Cel dokumentu

Celem jest zapewnienie, że dokumentacja jest zawsze aktualna, generowana automatycznie i spójna z kodem, zarówno dla:

developerów,

naukowców,

przemysłu,

administracji / audytorów.

Dokumentacja ma być:

powtarzalna,

weryfikowalna w CI,

możliwa do generowania z kodu i metadanych (docstringi, komentarze, anotacje typów, kontrakty, schematy).

2. Rodzaje dokumentacji objęte automatyzacją

System automatycznej dokumentacji obejmuje:

API Docs

REST / GraphQL / RPC / CLI.

Code Docs

docstringi, komentarze, typy, struktury modułów.

Architecture Docs

high-level diagramy, podział na moduły, przepływy.

Quality & CI Docs

zasady Zero Warnings, Zero Flake, Zero Drift, Auto-Healing, Telemetry, Security.

Change Logs & Release Notes

automatyczne changelogi z commitów / PR.

Domain / Business Docs (opcjonalnie)

opisy procesów, przypadków użycia, kontraktów z zewnętrznymi systemami.

3. Zasady ogólne automatycznej dokumentacji
3.1. Kod jest źródłem prawdy, dokumentacja jest projekcją

Dokumentacja ma być generowana z kodu oraz formalnych artefaktów (kontrakty, schematy, anotacje), a nie pisana „z powietrza”.

Konsekwencje:

kluczowe struktury muszą mieć docstringi / komentarze,

API musi mieć opisane parametry i typy,

kontrakty (JSON Schema, OpenAPI, proto, inne) są podstawą generowanych opisów.

3.2. Dokumentacja musi się budować w CI

Budowanie dokumentacji jest osobnym krokiem w CI.

Nieprzechodzący build dokumentacji = blokada merge (w trybie strict).

Ostrzeżenia z generatorów dokumentacji są traktowane tak jak inne warningi: ZERO WARNINGS.

3.3. Dokumentacja musi być wersjonowana

Każda wersja / release projektowy ma odpowiadającą jej wersję dokumentacji.

Dokumentacja dla main zawsze odzwierciedla aktualny stan kodu.

3.4. Dokumentacja nie może zawierać danych wrażliwych

Żadnych sekretów, danych osobowych, konfiguracji bezpieczeństwa.

Przykłady i fragmenty muszą być zanonimizowane.

4. Źródła danych do automatycznej dokumentacji

W zależności od stacku, wykorzystujemy:

Docstringi / komentarze – w funkcjach, klasach, modułach.

Typy – signatury funkcji, typy parametrów i zwrotów.

Kontrakty API – OpenAPI/Swagger, JSON Schema, GraphQL SDL, proto.

Schematy danych – definicje tabel, encji, modeli domenowych.

Konfiguracje – pliki .yaml, .json używane jako źródła metadanych.

Quality Pattern docs – SOFTWARE-CI-QUALITY-PATTERN, SECURITY, TELEMETRY itd.

Dla każdego projektu wybieramy generator odpowiedni dla języka (np. Sphinx/MkDocs/Doxygen/PhpDocumentor/JSDoc), ale logika specyfikacji jest wspólna.

5. Struktura wygenerowanej dokumentacji

Wygenerowana dokumentacja powinna zawierać co najmniej:

Home / Overview

opis projektu,

główne use-case’y,

architektura high-level,

linki do kluczowych sekcji.

Getting Started

instalacja,

uruchomienie (dev, test, prod),

minimalny przykład użycia.

API Reference

endpointy (lub komendy CLI, funkcje publik API),

parametry, typy, odpowiedzi,

przykłady wywołań.

Architecture

moduły i warstwy,

diagramy przepływów,

powiązania między komponentami.

Internals (dla developerów)

struktura katalogów,

kluczowe klasy/funkcje,

mechanizmy core (np. pamięć, math, scheduling).

Quality & CI

zasady Zero Warnings / Flake / Drift,

Auto-Healing CI,

telemetria, metryki.

Security & Compliance

link do SECURITY-GUIDELINES,

wymagania compliance,

zasady korzystania w środowiskach regulowanych.

Changelog

automatycznie generowane wpisy dla kolejnych wersji.

6. Integracja z CI/CD
6.1. Krok „Build Docs” w pipeline

Każdy PR i każdy push do main musi uruchamiać:

generowanie dokumentacji,

weryfikację, że proces się udał,

opcjonalnie „link checker”, jeśli dokumentacja zawiera przekierowania.

Jeśli:

build dokumentacji się nie powiedzie,

pojawią się warningi (deprecated, missing reference, etc.),

→ pipeline musi uznać to za błąd (w trybie strict / Mode 2).

6.2. Netlify/Pages/Artifacts

W zależności od projektu:

Dokumentacja może być publikowana jako:

artefakt CI (downloadable),

static site (GitHub Pages, Netlify, S3, itp.),

paczka do wewnętrznego portalu dokumentacji.

7. Automatyczne changelogi i release notes

Changelog powinien być generowany z:

commitów,

tagów,

opisów PR.

Minimalne wymagania:

zakres zmian,

wpływ na API,

wpływ na bezpieczeństwo,

wpływ na wydajność (jeśli dotyczy),

link do PR / ticketów.

8. Dokumentacja jako element jakości (Quality Pattern)

Dokumentacja jest powiązana z pozostałymi specyfikacjami:

z AUTO-TESTING-CI-SPEC – testy nie mogą być „czarną skrzynką”: kluczowy behavior ma być opisany,

z ZERO-DRIFT-BENCHMARKS – metryki wydajności i driftu mają sekcję w dokumentacji,

z TELEMETRY-GUIDELINES – opis dostępnych metryk i ich znaczenia,

z SECURITY-GUIDELINES – wyjaśnienie ograniczeń i wymogów dla użytkowników.

9. Rola agentów AI w dokumentacji

Agenty AI mogą:

generować szkielety dokumentów,

uzupełniać opisy na podstawie docstringów,

tworzyć diagramy tekstowe (np. mermaid),

proponować lepszą strukturę.

Agenty NIE mogą:

wymyślać fikcyjnych funkcji / endpointów,

zmieniać znaczenia parametrów,

deklarować zgodności lub certyfikacji, których nie ma.

Każda zmiana dokumentacji wykonana przez AI:

powinna być oznaczona jako ai-generated,

wymaga review człowieka.

10. Wersjonowanie i eksport

Dokumentacja:

powinna mieć wersję zgodną z wersją systemu (np. v1.2.3),

musi dać się wyeksportować w formatach:

HTML,

PDF (dla administracji i audytorów),

Markdown / tekst (dla repo).

11. Minimalne wymagania adopcji

Projekt uważa się za spełniający specyfikację, jeśli:

ma zautomatyzowany build dokumentacji w CI,

brak warningów z generatora dokumentacji,

ma przynajmniej:

Home, Getting Started, API Reference, Quality & CI, Changelog,

dokumentacja jest aktualna dla main.