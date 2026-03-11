# 📋 Plan Następnej Sesji: Operacja "Smart Assembly" (Dreamsoft Next.js)

## 🎯 Cel Główny
Poskładanie frontendu Next.js w spójną całość przy wykorzystaniu Grafu Wiedzy RAE na Node 1.

## 🛠️ Lista Zadań (Roadmap)

### 1. Faza Diagnostyczna (Deep Symbol Extraction)
- [ ] **Naprawa Ingestu Symboli:** Zdiagnozować brak symboli dla `CalculationService` (sprawdzić klucze `methods`/`functions` w `symbols.json`).
- [ ] **Re-Ingest Grafu:** Ponownie zasilić tenant `DREAMSOFT-FRONTEND-ASSEMBLY` kompletnymi danymi o 307 komponentach.

### 2. Faza Mapowania Zależności
- [ ] **Automatyczny Import-Fixer:** Wygenerować mapę brakujących importów w `src/services` na podstawie powiązań w grafie.
- [ ] **Analiza "Martwego Kodu":** Usunąć nieużywane serwisy, które nie mają relacji w Grafie Wiedzy.

### 3. Faza Montażu Core (The Brain)
- [ ] **Integracja Kalkulacji:** Połączyć `CalculationController.ts` z `CalculationEngine.tsx`.
- [ ] **Stitching Koszyka:** Podpiąć `CartService` pod `CartContext.tsx` i zwalidować komunikację z API (port 18000).

### 4. Faza UX & Visual Mirroring
- [ ] **Layout Integration:** Złożyć `RootLayout.tsx` (Header, Footer, Nav) zgodnie z Master Planem.
- [ ] **CSS Calibration:** Przeniesienie rygorystyczne stylów z AngularJS do Tailwinda (Operacja Lustro).

### 5. Walidacja ISO
- [ ] **E2E Traceability:** Test zamówienia z zapisem śladu w `ISO_AUDIT_GENEALOGY.jsonl`.
- [ ] **Performance Check:** Pomiary szybkości na Node 1.

## 📍 Infrastruktura (Node 1)
- **Katalog:** `~/rae-v5` oraz `~/dreamsoft_factory/next-frontend`
- **Tenant:** `6ad8b5a5-d61c-566d-98f9-8a131ab304a7` (DREAMSOFT-FRONTEND-ASSEMBLY)
- **Database:** `postgresql://rae:rae_password@localhost:5432/rae`
