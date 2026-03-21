# 🪞 Operacja Lustro: Roadmap Modernizacji Dreamsoft Pro 2.0

## 📍 Stan Infrastruktury (Node 1 - Lumina)
- **Frontend (Next.js):** Port 3005 (Healthy). Build-args: `NEXT_PUBLIC_API_URL=http://localhost:8000`.
- **Backend (PHP 8.1):** Port 8000 (Responding with 500). 
- **Static (Originals):** Port 8080 (Apache). Mount: `./data` -> `htdocs`.
- **RAE Core:** Port 8100 (Python 3.14).

## 🛠️ Najbliższe Zadania (Krok po Kroku):
1. **Naprawa Błędu 500 (Priorytet):** 
   - Przywrócenie poprawnej logiki `ConnectionFactory` i `ConnectionMasterFactory` (RAE ma specyfikację w pamięci semantycznej).
   - Weryfikacja połączenia z MySQL przez TCP (127.0.0.1) zamiast socketu.
2. **Weryfikacja Kategorii:** 
   - Po naprawie 500, sprawdzenie czy `DpCategoryService` poprawnie pobiera dane na front.
3. **Modernizacja Logowania (A2A):**
   - Implementacja zunifikowanego paszportu JWT (likwidacja dualizmu MySQL-Mongo).
4. **System Marż:** 
   - Analiza kalkulacji i ich „lustrzane” odbicie w nowym frontendzie.

## 🛡️ Rygory Techniczne:
- Zmiany w PHP robimy bezpośrednio na Node 1.
- Każda zmiana architektury musi być zapisana przez **RAE Bridge** (Tenant: 53717286-fe94-4c8f-baf9-c4d2758eb672).
- Zero Warning Policy dla kodu Next.js.
