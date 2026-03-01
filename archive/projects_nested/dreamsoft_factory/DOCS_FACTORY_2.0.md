# 🏭 Dreamsoft Pro 2.0 - Factory Documentation

## 🏗️ Infrastruktura (Architecture)
System działa w modelu rozproszonym:
1. **RAE-Core (The Black Box)**: Baza wiedzy (Postgres/SQL) przechowująca kod legacy i postępy prac.
2. **RAE-API Gateway**: Naprawiony endpoint `/v2/memories` działający jako inteligentny most do modeli SaaS (Gemini Pro/Flash).
3. **Feniks (The Orchestrator)**: Silnik logiczny (v74.5) zarządzający cyklem modernizacji.
4. **Lumina (Node 1)**: Główny węzeł obliczeniowy (RTX 4080) wykonujący fizyczne operacje i hostujący bazę.
5. **Supervisor**: Autonomiczny proces pilnujący zacięć i autorestarcji fabryki.

## 🧠 Opracowane Strategie Modernizacji

| Strategia | Kiedy używamy? | Opis |
| :--- | :--- | :--- |
| **Standard Path** | Pliki < 20kB | Bezpośrednia modernizacja pliku AngularJS -> React TSX. |
| **Context-Aware** | Wszystkie pliki | Automatyczne wstrzykiwanie kontraktów zmodernizowanych serwisów (Auth, Cart) do komponentów UI. |
| **Hierarchical Decomposition** | Giganty 20-100kB | Podział dużego kontrolera na logiczne sub-moduły (hooks, components, utils) w osobnych folderach. |
| **Atomic Slicing** | Giganty > 100kB | Modernizacja fragment po fragmencie (chunka) bezpośrednio z dysku, aby omijać limity tokenów. |
| **SQL Powerhouse** | Krytyczne zacięcia | Pobieranie kodu bezpośrednio z bazy danych SQL zamiast filtrów API (odporność na błędy serializacji). |

## 🏁 Co zostało zrobione?
- **259/287 plików (.tsx)** zmodernizowanych na poziomie Senior.
- **Mózg systemu**: `AuthService`, `CartWidgetService`, `routes.js`, `DeliveryService` zmodernizowane ręcznie/premium.
- **Serce systemu**: `CalcCtrl.js` i `calc.html` (łącznie ~2MB) zdekomponowane na moduły.
- **Infrastruktura**: Pełna telemetria Jaeger i automatyczny Supervisor.

## 📝 TODO: Do zrobienia w następnej sesji
1. **Stitching (Faza 3)**: Sklejenie atomowych fragmentów `CalcCtrl` w jeden działający system React Context.
2. **CSS Migration**: Zamiana resztek klas AngularJS na pełny Tailwind CSS.
3. **Mirror Test**: Uruchomienie `npm run dev` i sprawdzenie, czy nowy front wyświetla dane z API Luminy.
4. **Cleanup**: Usunięcie "pustych" plików-raportów z wcześniejszych faz.
