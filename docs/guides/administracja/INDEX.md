# Portal Dokumentacji dla Administracji Publicznej

**Witamy w dokumentacji RAE dla sektora publicznego!** 🏛️

Ten portal został stworzony specjalnie dla jednostek administracji publicznej, w tym JST (Jednostek Samorządu Terytorialnego), urzędów centralnych i instytucji państwowych. Znajdziesz tu wszystkie informacje dotyczące wdrożenia, bezpieczeństwa, zgodności prawnej i obsługi systemu RAE.

## 🚀 Szybki Start (10 minut)

**Nowy w RAE?** Zacznij tutaj:

1. **[Instalacja i Konfiguracja](#-wdrożenie-i-instalacja)**
   - Wdrożenie on-premise (zalecane dla sektora publicznego)
   - Wymagania sprzętowe i systemowe
   - Konfiguracja bezpieczeństwa

2. **[Zgodność z RODO/GDPR](#-zgodność-z-regulacjami)**
   - Przetwarzanie danych osobowych
   - Prawa osób, których dane dotyczą
   - Zabezpieczenia techniczne i organizacyjne

3. **[Wielodostępność (Multi-tenancy)](#-wielodostępność-multi-tenancy)**
   - Izolacja danych między jednostkami
   - Zarządzanie dostępem
   - Audyt działań użytkowników

## 📋 Dokumentacja Kluczowa

### Bezpieczeństwo i Zgodność

| Temat | Opis | Link |
|-------|------|------|
| **RODO/GDPR** | Zgodność z rozporządzeniem o ochronie danych | [RODO Guide](../../compliance/GDPR.md) |
| **ISO 42001** | Zarządzanie systemami AI | [ISO 42001](../../compliance/ISO_42001_SPEC.md) |
| **Bezpieczeństwo danych** | Szyfrowanie, kopie zapasowe, disaster recovery | [Security Guide](../../reference/deployment/security.md) |
| **Audyt i logi** | Śledzenie działań, compliance reporting | [Audit Logs](../../reference/services/audit-service.md) |

### Wdrożenie i Administracja

| Temat | Opis | Link |
|-------|------|------|
| **Instalacja On-Premise** | Wdrożenie w infrastrukturze własnej | [Deployment Guide](../../reference/deployment/on-premise.md) |
| **Konfiguracja systemu** | Ustawienia środowiska, bazy danych | [Configuration](../../reference/deployment/configuration.md) |
| **Backup i Recovery** | Polityka kopii zapasowych | [Backup Guide](../../reference/deployment/backup-recovery.md) |
| **Monitoring i utrzymanie** | Monitorowanie zdrowia systemu | [Monitoring](../../reference/deployment/monitoring.md) |

### Zarządzanie Dostępem

| Temat | Opis | Link |
|-------|------|------|
| **Wielodostępność** | Separacja danych między jednostkami | [Multi-tenancy](#-wielodostępność-multi-tenancy) |
| **Kontrola dostępu** | Role, uprawnienia, autoryzacja | [Access Control](../../reference/security/access-control.md) |
| **Integracja z Active Directory** | LDAP, SSO, federation | [AD Integration](../../reference/integrations/active-directory.md) |

## 🔒 Zgodność z Regulacjami

### RODO/GDPR

**RAE jest w pełni zgodny z RODO.** Kluczowe aspekty:

#### 1. Minimalizacja danych
```yaml
# Konfiguracja retencji danych
data_retention:
  episodic_memory: 30d  # Dane tymczasowe
  working_memory: 7d    # Kontekst sesji
  semantic_memory: 365d # Wiedza długoterminowa
  auto_delete: true     # Automatyczne usuwanie
```

#### 2. Prawo do usunięcia danych (Right to be Forgotten)
```python
# API do usuwania danych osoby
DELETE /api/v2/tenants/{tenant_id}/data-subjects/{subject_id}

# Kasuje wszystkie dane związane z daną osobą
# Zgodnie z Art. 17 RODO
```

#### 3. Prawo do przenoszenia danych (Data Portability)
```python
# Eksport danych osoby w formacie maszynowym
GET /api/v2/tenants/{tenant_id}/data-subjects/{subject_id}/export

# Zwraca JSON zgodny z Art. 20 RODO
```

#### 4. Szyfrowanie danych

- **W spoczynku:** AES-256 dla bazy danych i plików
- **W tranzycie:** TLS 1.3 dla wszystkich połączeń
- **Klucze:** Zarządzane przez HSM lub KMS

**Więcej:** [Compliance Guide - RODO](../../compliance/GDPR.md)

### ISO 42001 - Zarządzanie Systemami AI

RAE implementuje wymagania ISO 42001:

| Wymaganie | Implementacja | Status |
|-----------|---------------|--------|
| **Risk Management** | Ocena ryzyka LLM, bias detection | ✅ Zaimplementowane |
| **Transparency** | Logi decyzji AI, explainability | ✅ Zaimplementowane |
| **Human Oversight** | Human-in-the-loop dla krytycznych decyzji | ✅ Zaimplementowane |
| **Data Governance** | Polityki retencji, access control | ✅ Zaimplementowane |

**Więcej:** [ISO 42001 Compliance](../../compliance/ISO_42001_SPEC.md)

### Inne Regulacje

- **Ustawa o ochronie danych osobowych** - Pełna zgodność
- **KSI (Krajowe Standardy Interoperacyjności)** - Zgodność z wymogami interoperacyjności
- **ePUAP** - Możliwość integracji z platformą ePUAP

## 🏗️ Wdrożenie i Instalacja

### Wymagania Systemowe

**Minimalne:**
- CPU: 4 rdzenie
- RAM: 16 GB
- Dysk: 100 GB SSD
- System: Ubuntu 20.04 LTS / RHEL 8+

**Zalecane (produkcja):**
- CPU: 8+ rdzeni
- RAM: 32+ GB
- Dysk: 500 GB NVMe SSD
- System: Ubuntu 22.04 LTS
- Backup: Codzienne kopie zapasowe

### Instalacja On-Premise

#### Krok 1: Przygotowanie środowiska

```bash
# Instalacja Docker i Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalacja Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker compose
sudo chmod +x /usr/local/bin/docker compose
```

#### Krok 2: Konfiguracja

```bash
# Sklonuj repozytorium
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory.git
cd RAE-agentic-memory

# Skopiuj przykładową konfigurację
cp .env.example .env

# WAŻNE: Zmień domyślne hasła i klucze API!
nano .env
```

**Kluczowe zmienne w .env:**

```bash
# Bezpieczeństwo
POSTGRES_PASSWORD=<silne-haslo>
REDIS_PASSWORD=<silne-haslo>
API_SECRET_KEY=<klucz-256-bit>

# Multi-tenancy
TENANCY_ENABLED=true

# RODO/GDPR
ENABLE_GDPR_COMPLIANCE=true
DATA_RETENTION_DAYS=365
AUTO_DELETE_EXPIRED=true

# Szyfrowanie
ENABLE_ENCRYPTION_AT_REST=true
ENCRYPTION_KEY=<klucz-aes-256>

# Audit
ENABLE_AUDIT_LOGS=true
AUDIT_RETENTION_DAYS=2555  # 7 lat (wymóg prawny)
```

#### Krok 3: Uruchomienie

```bash
# Uruchom wszystkie usługi
docker compose up -d

# Sprawdź status
docker compose ps

# Sprawdź logi
docker compose logs -f

# Weryfikacja zdrowia systemu
curl http://localhost:8000/health
```

### Konfiguracja Firewall

```bash
# Otwórz tylko niezbędne porty
sudo ufw allow 8000/tcp  # API (tylko z sieci wewnętrznej!)
sudo ufw allow 8501/tcp  # Dashboard (opcjonalnie)
sudo ufw deny from any to any  # Zablokuj resztę

# NIE otwieraj portów baz danych na zewnątrz:
# - PostgreSQL: 5432 (tylko localhost)
# - Redis: 6379 (tylko localhost)
# - Qdrant: 6333 (tylko localhost)
```

## 🔐 Wielodostępność (Multi-tenancy)

RAE zapewnia **pełną izolację danych** między jednostkami (tenantami).

### Architektura Multi-tenancy

```
┌─────────────────────────────────────────┐
│         RAE API Gateway                 │
│   (automatyczna identyfikacja tenant)   │
└─────────────────────────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼────┐  ┌────▼───┐  ┌──────▼──┐
│ Tenant │  │ Tenant │  │ Tenant  │
│   A    │  │   B    │  │   C     │
│ (UM)   │  │ (US)   │  │ (MON)   │
└────────┘  └────────┘  └─────────┘

UM - Urząd Miasta
US - Urząd Skarbowy
MON - Ministerstwo
```

### Tworzenie Nowego Tenanta

```python
# Jako administrator systemu
POST /api/v2/admin/tenants

{
  "name": "Urząd Miasta Warszawa",
  "tenant_id": "um-warszawa",
  "settings": {
    "data_retention_days": 365,
    "max_users": 100,
    "enable_audit": true,
    "gdpr_contact": "iod@um.warszawa.pl"
  }
}
```

### Izolacja Danych

**Każde zapytanie SQL automatycznie zawiera `tenant_id`:**

```sql
-- ✅ POPRAWNIE - Automatycznie dodawane przez RAE
SELECT * FROM memories
WHERE tenant_id = 'um-warszawa'
  AND id = '123'

-- ❌ NIEMOŻLIWE - Brak dostępu do danych innych tenantów
SELECT * FROM memories WHERE id = '123'
-- Zwróci tylko dane tenant_id użytkownika
```

**Gwarancje bezpieczeństwa:**
- Tenant nie może zobaczyć danych innego tenanta
- Próba dostępu zwróci 404 (nie 403 - zero information leakage)
- Wszystkie operacje logowane w audit log

## 📊 Audyt i Monitoring

### Logi Audytu

**RAE rejestruje wszystkie operacje:**

```json
{
  "timestamp": "2025-12-06T10:30:00Z",
  "tenant_id": "um-warszawa",
  "user_id": "jan.kowalski@um.warszawa.pl",
  "action": "memory.read",
  "resource_id": "mem-12345",
  "ip_address": "10.0.1.50",
  "user_agent": "RAE-SDK/1.0",
  "status": "success"
}
```

**Eksport logów audytu:**

```bash
# Pobierz logi z ostatnich 7 dni
GET /api/v2/admin/audit-logs?from=2025-11-29&to=2025-12-06

# Eksport do CSV (dla celów compliance)
GET /api/v2/admin/audit-logs/export?format=csv
```

### Monitoring Systemu

**Metryki do monitorowania:**

| Metryka | Próg ostrzeżenia | Próg krytyczny |
|---------|------------------|----------------|
| CPU Usage | > 70% | > 90% |
| Memory Usage | > 80% | > 95% |
| Disk Usage | > 75% | > 90% |
| API Response Time | > 500ms | > 2s |
| Error Rate | > 1% | > 5% |

**Sprawdzanie zdrowia:**

```bash
# Health check
curl http://localhost:8000/health

# Szczegółowe metryki
curl http://localhost:8000/metrics
```

## 🆘 Wsparcie i Pomoc Techniczna

### Typowe Problemy

#### Problem: Użytkownik nie może się zalogować

**Objawy:**
- 401 Unauthorized
- "Invalid credentials"

**Rozwiązanie:**
1. Sprawdź czy użytkownik istnieje w systemie
2. Zresetuj hasło przez panel administratora
3. Sprawdź logi audytu: `docker compose logs -f rae-api`

#### Problem: Dane nie są usuwane automatycznie

**Objawy:**
- Stare dane wciąż w bazie po upływie okresu retencji

**Rozwiązanie:**
```bash
# Sprawdź konfigurację
grep DATA_RETENTION .env
grep AUTO_DELETE .env

# Uruchom manualnie cleanup
docker compose exec rae-api python scripts/cleanup_expired_data.py

# Sprawdź logi cleanup job
docker compose logs celery-worker | grep cleanup
```

#### Problem: Wysoka latencja API

**Objawy:**
- Odpowiedzi API > 2s
- Timeouty

**Rozwiązanie:**
1. Sprawdź CPU/Memory: `docker stats`
2. Sprawdź indeksy bazy danych
3. Rozważ skalowanie poziome (więcej instancji API)

### Kontakt z Wsparciem

- **GitHub Issues:** [Zgłoś problem](https://github.com/dreamsoft-pro/RAE-agentic-memory/issues)
- **Dokumentacja:** Ten portal
- **Email:** support@rae-memory.ai

## 📚 Dokumentacja Techniczna

### Dla Administratorów

- [Deployment Guide](../../reference/deployment/on-premise.md) - Wdrożenie on-premise
- [Configuration Reference](../../reference/deployment/configuration.md) - Wszystkie opcje konfiguracji
- [Backup & Recovery](../../reference/deployment/backup-recovery.md) - Polityka kopii zapasowych
- [Monitoring](../../reference/deployment/monitoring.md) - Metryki i alerty

### Dla Zespołów Bezpieczeństwa

- [Security Architecture](../../reference/security/architecture.md) - Architektura bezpieczeństwa
- [Encryption](../../reference/security/encryption.md) - Szyfrowanie danych
- [Access Control](../../reference/security/access-control.md) - Kontrola dostępu
- [Penetration Testing Guide](../../reference/security/pentesting.md) - Testy penetracyjne

### Zgodność Prawna

- [RODO/GDPR Compliance](../../compliance/GDPR.md) - Pełna zgodność z RODO
- [ISO 42001](../../compliance/ISO_42001_SPEC.md) - Zarządzanie systemami AI
- [Data Processing Agreement](../../compliance/DPA.md) - Wzór umowy powierzenia

## 🗺️ Roadmapa

**Aktualna wersja:** 1.0.0

**Planowane funkcje:**
- Integracja z ePUAP
- Podpis elektroniczny (kwalifikowany)
- Moduł workflow dla procesów urzędowych
- Moduł do obsługi interpelacji i petycji
- Dashboard analityczny dla kierownictwa

Zobacz [TODO.md](../../../TODO.md) dla pełnej roadmapy.

## 📖 Linki Przydatne

### Dokumentacja Podstawowa

- [README.md](../../README.md) - Przegląd projektu
- [Architektura Systemu](../../reference/architecture/README.md)
- [API Reference](http://localhost:8000/docs)

### Compliance

- [RODO/GDPR](../../compliance/GDPR.md)
- [ISO 42001](../../compliance/ISO_42001_SPEC.md)
- [Security Guidelines](../../reference/security/architecture.md)

### Deployment

- [On-Premise Deployment](../../reference/deployment/on-premise.md)
- [Configuration](../../reference/deployment/configuration.md)
- [Backup & Recovery](../../reference/deployment/backup-recovery.md)

---

**Potrzebujesz pomocy?** Skontaktuj się przez [GitHub Issues](https://github.com/dreamsoft-pro/RAE-agentic-memory/issues) lub sprawdź [sekcję wsparcia](#-wsparcie-i-pomoc-techniczna).

**Ostatnia aktualizacja:** 2025-12-06
