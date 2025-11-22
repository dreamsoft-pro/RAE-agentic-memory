# MCP Improvement Plan for RAE
### (Model Context Protocol Integration Hardening & Cleanup)

Ten dokument opisuje kompletny proces uporządkowania, doprecyzowania i wzmocnienia obsługi protokołu **MCP (Model Context Protocol)** w projekcie RAE.

Aktualna implementacja MCP jest dobra architektonicznie, ale wymaga dopracowania w obszarach:
- nazewnictwa,
- struktury katalogów,
- spójności dokumentacji,
- rozdzielenia dwóch różnych serwisów,
- testów,
- payloadów API i enumów,
- UX integracji z IDE (Claude, Cursor, Cline).

Celem jest uzyskanie **krystalicznie jasnej**, w pełni udokumentowanej i produkcyjnie spójnej implementacji MCP.

---

# 1. Executive Summary – Co trzeba poprawić

1. **Rozdzielić dwa różne serwisy**, które dziś są myląco nazwane „MCP”:
   - właściwy MCP dla IDE (STDIO JSON-RPC)  
   - file-watcher / context-provider (HTTP)

2. **Uporządkować dokumentację**:
   - osobny dokument dla IDE MCP server  
   - osobny dokument dla file-watcher daemon  
   - spójna terminologia: MCP = *tylko Model Context Protocol*

3. **Ujednolicić nazwy katalogów i modułów**:
   - `integrations/mcp-server` → tylko MCP (IDE)  
   - `integrations/context-watcher` → HTTP daemon (przeniesiony z mcp-server/main.py)

4. **Ujednolicić endpointy API** (`/v1/memory/...`)

5. **Dodać testy MCP**:
   - JSON-RPC → narzędzia (tools) → RAE API  
   - test integracji end-to-end

6. **Naprawić placeholders w README**  
   (linki „your-org”, placeholder docs, nieistniejące domeny)

---

# 2. Ujednolicenie Nazewnictwa i Architektury

## 2.1. Obecny stan (problem)

W katalogu `integrations/mcp-server/` znajdują się dwa różne byty, oba nazywane „MCP”:

### 1. MCP STDIO Server (prawdziwy Model Context Protocol)
Lokalizacja:
integrations/mcp-server/src/rae_mcp_server/

yaml
Skopiuj kod
To serwer MCP używany przez:
- Claude Desktop
- Cursor IDE
- Cline

Komunikacja: **STDIO JSON-RPC**  
→ To jest **właściwy MCP** i powinien zachować skrót MCP.

---

### 2. HTTP File-Watcher (Memory Context Provider)
Lokalizacja:
integrations/mcp-server/main.py

yaml
Skopiuj kod
To jest:
- daemon HTTP
- endpoint `/projects`
- watcher zmian plików
- wysyła treści plików do RAE API przez RAEClient

To **nie jest Model Context Protocol**.

---

## 2.2. Proponowany nowy układ katalogów

### 🔵 MCP (Model Context Protocol, STDIO JSON-RPC)
integrations/mcp/
├── README.md
├── pyproject.toml
└── src/
└── rae_mcp/
├── main.py
├── server.py
├── client.py
├── tools/
└── resources/

shell
Skopiuj kod

### 🟡 Context Watcher (HTTP File Watcher)
integrations/context-watcher/
├── README.md
├── pyproject.toml (opcjonalnie)
└── src/context_watcher/
├── main.py
├── api.py (FastAPI)
├── watcher.py
└── rae_client.py

markdown
Skopiuj kod

### 🔴 Migracja
- przenieść `integrations/mcp-server/main.py` → `integrations/context-watcher/api.py`
- przenieść cały watcher logic → `watcher.py`
- pozostawić w MCP tylko STDIO JSON-RPC server

---

# 3. Standaryzacja Dokumentacji

Obecnie dokumenty „mieszają” dwa różne protokoły.

## 3.1. Nowe dokumenty

### **docs/integrations/mcp_protocol_server.md**
Zawiera:
- co to jest MCP
- jak działa STDIO JSON-RPC
- jak działa `rae_mcp` server
- lista tools / resources
- konfiguracja Claude / Cursor / Cline
- jak uruchomić (`rae-mcp-server`)
- troubleshooting dla IDE

### **docs/integrations/context_watcher_daemon.md**
Zawiera:
- czym jest watcher
- endpoint `/projects`
- struktura JSON dla projektów
- sekwencje: file update → RAE → memory API
- jak uruchomić: `python -m context_watcher`
- integracje CI/FS watcher

## 3.2. README główne
Dodać tabelę:

| Integracja | Protokół | Lokalizacja | Dokument |
|-----------|----------|-------------|----------|
| MCP Server (IDE) | Model Context Protocol (JSON-RPC/STDIO) | `integrations/mcp/` | `mcp_protocol_server.md` |
| Context Watcher | HTTP + FileWatcher | `integrations/context-watcher/` | `context_watcher_daemon.md` |

---

# 4. Uporządkowanie API i payloadów

## 4.1. Endpointy
Sprawdzić, czy wszystkie wywołania z MCP używają najnowszych endpointów:

### Powinno być:
POST /v1/memory/store
POST /v1/memory/query
POST /v1/memory/delete
POST /v1/graph/extract

shell
Skopiuj kod

### W dokumentacji nadal występują:
/memory/store
/memory/add

yaml
Skopiuj kod
→ naprawić w docs, README, przykładach Claude/Cursor.

---

# 5. Testy – MCP End-to-End

Obecnie testy MCP testują tylko częściowo klienta i bibliotekę. Brakuje testów, które symulują prawdziwe wywołanie MCP.

## 5.1. Dodać test MCP JSON-RPC

Nowy katalog:
integrations/mcp/tests/test_mcp_e2e.py

yaml
Skopiuj kod

### Testy do dodania:
1. **`test_mcp_save_memory()`**
   - JSON-RPC input: `{"method": "tool/save_memory", ...}`
   - symuluje STDIO input
   - oczekuje wywołania RAE API i poprawnego outputu

2. **`test_mcp_search_memory()`**
   - wywołanie `tool/search_memory`
   - mock MLServiceClient + MemoryRepository

3. **`test_mcp_get_related_context()`**

4. **test zasobów MCP (`/resources/*`)**

---

# 6. Usunięcie placeholderów

Z README i docs:

- `your-org/rae-agentic-memory` → `dreamsoft-pro/RAE-agentic-memory`
- `https://docs.rae-memory.dev` → poprawny link (lub usuń)
- `support@rae-memory.dev` → jeśli maila nie ma → wyrzucić

---

# 7. Poprawa UX integracji z IDE

## 7.1. Claude Desktop

Dodać pełną przykładową konfigurację:
{
"mcpServers": {
"rae": {
"command": "rae-mcp-server",
"args": ["--config", "/home/user/.rae/config.json"]
}
}
}

yaml
Skopiuj kod

## 7.2. Cursor IDE

Dodać przykład z absolutnymi ścieżkami.

## 7.3. Cline

Dodać informację, że Cline wymaga nazwy servera zgodnej z `providerId`.

---

# 8. Prometheus / Logging

## 8.1. MCP Server
Dodać:
- log połączeń JSON-RPC,
- licznik `mcp_tools_called_total`,
- licznik błędów MCP-json.

## 8.2. Context Watcher
- logi watchera (plik zwięzłych zmian),
- metryka: `files_synced_total`,
- metryka: `watched_projects_total`.

---

# 9. Final Checklist (Ready for MCP v1.1)

## Architektura
- [ ] MCP i watcher rozdzielone katalogowo  
- [ ] MCP dokumentacja jednoznaczna  
- [ ] watcher dokumentacja jednoznaczna  

## Kod
- [ ] MCP STDIO server w `integrations/mcp/`  
- [ ] watcher w `integrations/context-watcher/`  
- [ ] poprawione ścieżki `/v1/...`  

## Testy
- [ ] testy JSON-RPC E2E  
- [ ] testy zasobów MCP  
- [ ] testy file watcher → RAE API  

## Dokumentacja
- [ ] dwa nowe pliki docs  
- [ ] README z tabelą integracji  
- [ ] usunięte placeholders  

## Release
- [ ] tag `v1.1.0-mcp`  
- [ ] pełny opis w RELEASE_NOTES  
- [ ] gotowe konfigi dla IDE  

---

# 10. Podsumowanie

Po wdrożeniu wszystkich elementów z tego dokumentu będziesz miał:

### ✔ Najbardziej kompletne wdrożenie Model Context Protocol w świecie OSS  
### ✔ Idealną przejrzystość dla developerów (brak pomyłek MCP vs watcher)  
### ✔ Wysokiej jakości dokumentację integracji z Claude/Cursor/Cline  
### ✔ Testy E2E zapewniające stabilność  
### ✔ Produkcyjne, skalowalne, czyste integracje  

RAE stanie się wtedy **referencyjnym wdrożeniem MCP** — nie tylko działającym, ale **wzorcowym**.

Jeśli chcesz, mogę teraz przygotować: