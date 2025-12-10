# 🌍 PUBLIC REPO STRATEGY - Strategia dla Publicznego Repo

> **Cel**: Bezpieczne zarządzanie publicznym repozytorium open source
>
> **Status**: MANDATORY dla RAE jako publiczne repo

---

## 🎯 Model Branchów dla Open Source

```
ZEWNĘTRZNI KONTRYBUTORZY:
fork → feature/* → PR do develop (TYLKO!)
                     ↓
                  Code Review
                     ↓
                  Merge do develop

MAINTAINERS (Wewnętrzni):
feature/* → develop → release → main
```

**Kluczowa zasada**: Zewnętrzni mogą targetować TYLKO `develop`, NIGDY `main` ani `release`.

---

## 🔐 BEZPIECZEŃSTWO

### 1. Secrets i Klucze API

| Element | Status | Ochrona |
|---------|--------|---------|
| API Keys | ❌ NIGDY w repo | `.env` + `.gitignore` |
| Passwords | ❌ NIGDY w repo | Secrets management |
| Private keys | ❌ NIGDY w repo | Vault/GitHub Secrets |
| `.env.example` | ✅ OK | Bez wartości, tylko keys |
| Test fixtures | ⚠️ Ostrożnie | Użyj fake data |

### 2. Automatyczne Sprawdzania

```yaml
# .github/workflows/pr-security-check.yml
name: PR Security Check

on:
  pull_request_target:  # Bezpieczne dla external PRs
    types: [opened, synchronize]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}

      - name: Check for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.pull_request.base.sha }}
          head: ${{ github.event.pull_request.head.sha }}

      - name: Check for large files
        run: |
          find . -type f -size +10M | while read file; do
            echo "❌ Large file: $file"
            exit 1
          done

      - name: Check for sensitive paths
        run: |
          if git diff --name-only ${{ github.event.pull_request.base.sha }} | grep -E '\.env$|\.pem$|\.key$'; then
            echo "❌ Sensitive file detected"
            exit 1
          fi
```

---

## 🚪 ZEWNĘTRZNI KONTRYBUTORZY

### Wymagania dla PR

| Wymaganie | Obowiązkowe? | Sprawdzane przez |
|-----------|-------------|------------------|
| DCO sign-off | ✅ TAK | dcoapp/app |
| Target = develop | ✅ TAK | PR check workflow |
| Passing CI | ✅ TAK | GitHub Actions |
| Code review | ✅ TAK | Maintainers |
| CONTRIBUTING.md | ✅ TAK | Manual check |
| Conventional commits | ✅ TAK | commitlint |

### DCO (Developer Certificate of Origin)

```bash
# Każdy commit musi być signed
git commit -s -m "feat: add feature X"

# Dodaje do commit message:
Signed-off-by: Jan Kowalski <jan@example.com>
```

**Workflow sprawdzania DCO**:
```yaml
# .github/workflows/dco.yml
name: DCO Check

on: [pull_request]

jobs:
  dco:
    runs-on: ubuntu-latest
    steps:
      - uses: dcoapp/app@v1
```

### Workflow dla Zewnętrznych

```bash
# 1. Fork repo
https://github.com/dreamsoft-pro/RAE-agentic-memory
[Click "Fork"]

# 2. Clone fork
git clone https://github.com/your-username/RAE-agentic-memory
cd RAE-agentic-memory

# 3. Dodaj upstream
git remote add upstream https://github.com/dreamsoft-pro/RAE-agentic-memory

# 4. Utwórz feature branch
git checkout develop
git pull upstream develop
git checkout -b feature/my-contribution

# 5. Implementuj
# [kod...]

# 6. Commit z DCO
git commit -s -m "feat: add my feature"

# 7. Push do fork
git push origin feature/my-contribution

# 8. Utwórz PR (przez GitHub UI)
# Base: dreamsoft-pro/RAE-agentic-memory:develop
# Head: your-username/RAE-agentic-memory:feature/my-contribution
```

---

## ⚠️ ZABRONIONE ZMIANY (Zewnętrzni)

### NIE Akceptujemy PR które:

| Zmiana | Dlaczego zabronione |
|--------|---------------------|
| `.github/workflows/*` | Security risk - CI/CD manipulation |
| `/apps/memory_api/security/*` | Security-sensitive code |
| `/infra/*` | Infrastructure changes require deep review |
| `CRITICAL_AGENT_RULES.md` | Core policies - internal only |
| Direct to `main` or `release` | Only maintainers via release process |
| Large binary files (>10MB) | Bloats repository |
| Secrets/credentials | Security violation |

### Automatyczna Blokada

```yaml
# .github/workflows/pr-validation.yml
name: PR Validation

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Check target branch
        if: |
          github.event.pull_request.base.ref != 'develop' &&
          github.event.sender.login != 'dreamsoft-pro'
        run: |
          echo "❌ External PRs must target 'develop' branch"
          echo "Current target: ${{ github.event.pull_request.base.ref }}"
          exit 1

      - name: Check forbidden paths
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - run: |
          CHANGED=$(git diff --name-only HEAD^ HEAD)

          FORBIDDEN=(
            ".github/workflows/"
            "apps/memory_api/security/"
            "infra/"
            "CRITICAL_AGENT_RULES.md"
          )

          for path in "${FORBIDDEN[@]}"; do
            if echo "$CHANGED" | grep -q "^$path"; then
              if [ "${{ github.event.sender.login }}" != "dreamsoft-pro" ]; then
                echo "❌ Forbidden path for external contributors: $path"
                exit 1
              fi
            fi
          done
```

---

## 👥 CODEOWNERS (Wzmocniona dla Public Repo)

```
# .github/CODEOWNERS

# Wszystko domyślnie
* @dreamsoft-pro/maintainers

# Krytyczne pliki - TYLKO core team
/.github/workflows/* @dreamsoft-pro/core-maintainers
/CRITICAL_AGENT_RULES.md @dreamsoft-pro/core-maintainers
/AI_AGENT_MANIFEST.md @dreamsoft-pro/core-maintainers
/SESSION_START.md @dreamsoft-pro/core-maintainers
/AUTONOMOUS_OPERATIONS.md @dreamsoft-pro/core-maintainers
/BRANCH_STRATEGY.md @dreamsoft-pro/core-maintainers

# Security - TYLKO security team
/apps/memory_api/security/* @dreamsoft-pro/security-team
/apps/memory_api/middleware/auth.py @dreamsoft-pro/security-team

# Infrastructure - TYLKO devops
/infra/* @dreamsoft-pro/devops
/docker-compose*.yml @dreamsoft-pro/devops

# Core services - review przez core team
/apps/memory_api/services/* @dreamsoft-pro/core-maintainers
/apps/memory_api/repositories/* @dreamsoft-pro/core-maintainers

# Public contributions welcome (dokumentacja, testy)
/docs/* @dreamsoft-pro/maintainers
/tests/* @dreamsoft-pro/maintainers
/examples/* @dreamsoft-pro/maintainers
```

---

## 📋 REVIEW PROCESS (Zewnętrzne PR)

### Checklist dla Reviewers

Przed approval zewnętrznego PR, sprawdź:

- [ ] ✅ Target branch = `develop`
- [ ] ✅ DCO sign-off present
- [ ] ✅ Conventional commit format
- [ ] ✅ All CI checks passing
- [ ] ✅ No secrets in code
- [ ] ✅ No large binary files
- [ ] ✅ No changes to forbidden paths
- [ ] ✅ Tests added for new code
- [ ] ✅ Documentation updated
- [ ] ✅ Code quality (follows CONVENTIONS.md)
- [ ] ✅ No malicious code
- [ ] ✅ License compatible (MIT)

### Czas Review

| PR Size | Expected Review Time |
|---------|---------------------|
| Trivial (<10 lines) | 1-2 dni |
| Small (<100 lines) | 2-3 dni |
| Medium (<500 lines) | 3-5 dni |
| Large (>500 lines) | 5-10 dni |

**Uwaga**: Large PRs są trudniejsze do review. Zachęcamy do mniejszych, częstszych PR!

---

## 🏷️ LABEL SYSTEM

### Labels dla PR

| Label | Kiedy | Kto ustawia |
|-------|-------|-------------|
| `external-contribution` | PR od non-maintainer | Automatyczne (bot) |
| `needs-review` | Czeka na review | Automatyczne |
| `changes-requested` | Wymaga poprawek | Reviewer |
| `approved` | Zatwierdzony | Reviewer |
| `security-review` | Wymaga security review | Automatyczne (jeśli security paths) |
| `breaking-change` | Łamie API | Author lub reviewer |
| `documentation` | Tylko docs | Author |

### Automatyczne Labelling

```yaml
# .github/workflows/auto-label.yml
name: Auto Label

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v4
        with:
          configuration-path: .github/labeler.yml
```

```yaml
# .github/labeler.yml
'external-contribution':
  - '!maintainers/**'

'documentation':
  - 'docs/**'
  - '*.md'

'security-review':
  - 'apps/memory_api/security/**'
  - 'apps/memory_api/middleware/auth.py'

'tests':
  - 'tests/**'
  - '**/*_test.py'
  - '**/test_*.py'
```

---

## 🤝 CONTRIBUTOR LICENSE AGREEMENT (CLA)

### Czy potrzebujemy CLA?

**Dla MIT License: NIE**

MIT license jest wystarczająco permissive. CLA nie jest wymagany.

Jednak wymagamy **DCO (Developer Certificate of Origin)** który jest lżejszą alternatywą.

### DCO vs CLA

| Aspekt | DCO | CLA |
|--------|-----|-----|
| Złożoność | Prosty | Skomplikowany |
| Sign-off | Każdy commit | Jednorazowo |
| Prawne | Wystarczające | Kompletne |
| Dla MIT | ✅ Zalecane | ❌ Overkill |

---

## 📊 STATYSTYKI I TRANSPARENTNOŚĆ

### Public Dashboard

Udostępniamy publicznie:
- ✅ Test coverage (codecov badge)
- ✅ CI status (GitHub Actions badge)
- ✅ Security scan results (Snyk/GitHub)
- ✅ License (MIT badge)
- ✅ Release notes (CHANGELOG.md)

### README Badges

```markdown
[![Tests](https://github.com/dreamsoft-pro/RAE-agentic-memory/workflows/CI/badge.svg)](https://github.com/dreamsoft-pro/RAE-agentic-memory/actions)
[![Coverage](https://codecov.io/gh/dreamsoft-pro/RAE-agentic-memory/branch/main/graph/badge.svg)](https://codecov.io/gh/dreamsoft-pro/RAE-agentic-memory)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

---

## 🎓 ONBOARDING ZEWNĘTRZNYCH

### CONTRIBUTING.md (Kluczowy dokument)

Musi zawierać:
1. **How to contribute** - krok po kroku
2. **Code of conduct** - zasady zachowania
3. **Development setup** - jak uruchomić lokalnie
4. **Testing** - jak testować zmiany
5. **PR process** - jak utworzyć dobry PR
6. **Review timeline** - czego się spodziewać

### Good First Issues

Label `good-first-issue` dla prostych zadań:
- Documentation fixes
- Test coverage improvement
- Small bug fixes
- Code formatting

```yaml
# .github/workflows/label-good-first-issues.yml
# Automatycznie label prostych issues
```

---

## ⚖️ LICENSE ENFORCEMENT

### MIT License

RAE używa MIT License - bardzo permissive.

**Wymagania**:
- ✅ Zachowaj copyright notice
- ✅ Zachowaj license text
- ✅ Możesz użyć komercyjnie
- ✅ Możesz modyfikować
- ✅ Możesz dystrybuować

**Nie wymagane**:
- ❌ Share source code (możesz closed-source fork)
- ❌ Same license dla derivative works

### License Check

```yaml
# .github/workflows/license-check.yml
name: License Check

on: [pull_request]

jobs:
  license:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check license headers
        run: |
          # Sprawdź czy każdy .py ma license header
          python scripts/check_license_headers.py
```

---

## 🚨 SECURITY POLICY

### `SECURITY.md`

```markdown
# Security Policy

## Reporting a Vulnerability

**DO NOT** open a public issue for security vulnerabilities.

Instead, email security@dreamsoft-pro.com with:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours.

## Security Update Process

1. Receive report → Verify (48h)
2. Develop fix → Test (1 week)
3. Private security advisory (GitHub)
4. Release hotfix
5. Public disclosure (after fix deployed)

## Supported Versions

| Version | Supported |
|---------|-----------|
| main    | ✅        |
| develop | ⚠️ Beta   |
| < 1.0   | ❌        |
```

---

## ✅ CHECKLIST - Setup Public Repo

### Initial Setup

- [ ] Repository set to Public on GitHub
- [ ] LICENSE file added (MIT)
- [ ] CODE_OF_CONDUCT.md added
- [ ] CONTRIBUTING.md added
- [ ] SECURITY.md added
- [ ] README badges added
- [ ] .github/CODEOWNERS configured
- [ ] Branch protection enabled (main, release)
- [ ] GitHub Teams created (maintainers, core-maintainers, security)

### CI/CD dla External PR

- [ ] PR validation workflow (target branch check)
- [ ] DCO check workflow
- [ ] Security scan (TruffleHog)
- [ ] Forbidden paths check
- [ ] Auto-labelling workflow
- [ ] License check

### Documentation

- [ ] PUBLIC_REPO_STRATEGY.md (ten dokument)
- [ ] Contributor guidelines clear
- [ ] Setup instructions in README
- [ ] API documentation published

---

**Wersja**: 1.0.0
**Data**: 2025-12-10
**Status**: 🔴 MANDATORY - Dla publicznych repo
**License**: MIT
