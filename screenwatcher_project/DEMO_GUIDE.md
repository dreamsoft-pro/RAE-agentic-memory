# ScreenWatcher Demo Guide - Factory Launch 🚀

Ta instrukcja pozwoli Ci błyskawicznie uruchomić system w trybie prezentacyjnym, nawet na czystym serwerze.

## 1. Start Systemu (Docker)

Otwórz terminal w katalogu projektu i wpisz:

```bash
# Uruchomienie kontenerów w tle
docker-compose up --build -d
```

Poczekaj ok. 30-60 sekund aż baza danych wstanie.

## 2. Inicjalizacja Danych i Kont

Musisz utworzyć strukturę fabryki oraz użytkownika dla symulatora. Wykonaj to polecenie wewnątrz kontenera:

```bash
# Aplikacja migracji (struktura bazy)
docker-compose exec web python manage.py migrate

# Utworzenie SuperAdmina (login: admin, hasło: admin123) - opcjonalnie, jeśli chcesz własnego
docker-compose exec web python manage.py createsuperuser --username admin --email admin@factory.com --noinput
docker-compose exec web python manage.py shell -c "from django.contrib.auth.models import User; u=User.objects.get(username='admin'); u.set_password('admin123'); u.save()"

# ⭐️ KLUCZOWE: Automatyczna konfiguracja Fabryki i Konta Symulatora
docker-compose exec web python tools/init_simulation_data.py
```

## 3. Uruchomienie Symulacji ("Show Mode")

Aby Dashboard ożył, musisz włączyć symulator. Najlepiej zrób to w **osobnym oknie terminala**, aby widzieć logi:

```bash
# Uruchamia symulator wewnątrz kontenera (dzięki temu ma dostęp do sieci wewnętrznej Dockera)
docker-compose exec web python tools/simulator.py
```

Powinieneś widzieć logi typu: `[14:30:05] RUNNING | Temp: 75.4C | Prod: 3`.

## 4. Dostęp do Dashboardu

1. Otwórz przeglądarkę na komputerze (lub innym urządzeniu w sieci).
2. Adres: `http://<IP_SERWERA>:8000/dashboard/` (lub `localhost:8000` jeśli to ten sam PC).
3. Zaloguj się danymi Admina (`admin` / `admin123`).
4. **Ciesz się widokiem!** Dane powinny spływać na żywo (WebSockets).

## 5. Prezentacja Funkcji (Scenariusz)

1. **Live Data:** Pokaż, że widgety (gauge, wykresy) ruszają się same bez odświeżania strony.
2. **Alert:** Poczekaj chwilę, aż symulator wylosuje wysoką temperaturę (>90C) lub błąd. Powinien wyskoczyć "Toast" w prawym dolnym rogu, a na liście alertów pojawi się wpis.
3. **Historia:** Przełącz widget na "Last 7 Days" i pokaż, że dane się agregują.

---
**Awaryjneatrzymanie:**
`docker-compose down`
