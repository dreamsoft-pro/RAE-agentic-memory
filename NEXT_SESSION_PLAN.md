# 📋 Plan Następnej Sesji: Operacja "Strangler Fig" (Dreamsoft Next.js)

## 🎯 Cel Główny
Zbudowanie stabilnego, nowoczesnego frontendu Next.js 14 od podstaw, wykorzystując stary kod AngularJS jako "Złotą Wyrocznię" i Graf Wiedzy RAE jako mapę drogową. Odrzucamy automatycznie wygenerowany, błędny kod na rzecz rygorystycznego, ręcznego przepisywania moduł po module z zachowaniem zasady "Zero Errors Policy" w TypeScript.

## 🛠️ Lista Zadań (Roadmap - 6 Faz)

### Faza 1: Oczyszczenie Przedpola (Tabula Rasa)
- [ ] Skasować wszystkie 400+ błędnych plików w `next-frontend/src/services` na Node 1.
- [ ] Upewnić się, że struktura Next.js buduje się bez żadnych błędów kompilacji (`npx tsc --noEmit`).
- [ ] Pozostawić tylko poprawne szkielety (App Router, Tailwind, Zustand, `Header.tsx`, `Footer.tsx`).

### Faza 2: Fundament Komunikacyjny (The Bridge)
- [ ] Zbudować centralny `ApiClient.ts` (na bazie Axios).
- [ ] Zaimplementować globalną obsługę błędów, CORS oraz wstrzykiwanie nowego uniwersalnego paszportu JWT do nagłówków.
- [ ] Odtworzyć i przetestować endpointy logowania (`AuthService`).

### Faza 3: Drzewo Treści (Katalog i Statyka)
- [ ] Odtworzyć logikę struktury: *Kategoria -> Podkategoria -> Grupa -> Produkt* z użyciem Server Components (SEO-friendly).
- [ ] Zaimplementować `DpCategoryService` z wykorzystaniem React Query do cachowania.
- [ ] Przenieść logikę stron statycznych i bloga (`StaticContentService`, `NewsService`).

### Faza 4: Złote Serce (Silnik Kalkulacyjny i Konfigurator)
- [ ] Odtworzyć UI konfiguratora produktu (wymiary, nakłady, papiery) i zarządzać jego stanem lokalnie (lub przez `Zustand`).
- [ ] Zbudować komunikację z API PHP dla wyliczeń cenowych ("Backend for Frontend").
- [ ] Połączyć konfigurator z globalnym koszykiem (`cartStore.ts`).

### Faza 5: Koszyk i Przepływ Zamówienia (Checkout)
- [ ] Zaimplementować `CartService` i `DeliveryService` w nowej architekturze.
- [ ] Zbudować przepływ Checkout: formularze adresowe, wybór kuriera, wybór płatności.
- [ ] Zintegrować walidację zamówienia z API.

### Faza 6: Panel Klienta (Client Zone)
- [ ] Odtworzyć widoki historii zamówień, faktur i reklamacji dla zalogowanego użytkownika.
- [ ] Zintegrować logowanie Social (Google, Apple) z uniwersalnym JWT.

## 📍 Infrastruktura (MANDATORY HUB: NODE 1)
- **Środowisko:** Node 1 (`100.68.166.117`)
- **Katalog Główny:** `~/dreamsoft_factory/next-frontend`
- **Asystent Kognitywny:** Graf Wiedzy RAE (tenant: `DREAMSOFT-FRONTEND-ASSEMBLY`) działający w głównej bazie `rae-postgres` na Node 1.
