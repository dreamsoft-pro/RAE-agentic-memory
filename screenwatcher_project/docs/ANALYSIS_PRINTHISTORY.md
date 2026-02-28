# Analiza Potencjału Danych z Historii Druku (PrintHistory)

Dzięki inżynierii wstecznej pliku `PrintHistory` uzyskaliśmy dostęp do **"Czarnej Skrzynki"** drukarki. Połączyliśmy te dane z systemem ScreenWatcher, co pozwala na następujące analizy:

## 1. Precyzyjna Kalkulacja Kosztów (Job Costing)
To najważniejsza wartość biznesowa. Do tej pory znaliśmy tylko czas pracy maszyny. Teraz znamy fizyczne zużycie surowców na każde zlecenie.
*   **Koszt Tuszu na Zlecenie:** Mamy dokładną liczbę kropel (`TotalCount`). Znając objętość kropli (pikolitry) i cenę tuszu za litr, możemy wyliczyć koszt farby dla każdego pliku `.prt` co do grosza.
*   **Koszt Mediów:** Mamy precyzyjną powierzchnię (`FinishArea` w m²). Możemy automatycznie wyliczać zużycie materiału (folia, papier, baner).
*   **Rentowność Zlecenia:** Zestawiając powyższe koszty z ceną sprzedaży, system może generować raport marżowości per plik.

## 2. Analiza Technologiczna Druku (Ink Density)
Mamy unikalny wgląd w to, *jak* maszyna drukuje, dzięki rozbiciu na wielkości kropel (`Big`, `Middle`, `Small`).
*   **Analiza Nasycenia (Ink Coverage):** Stosunek liczby kropel do powierzchni (Drops / m²). Pozwala zidentyfikować pliki "tuszernie", które schną wolniej i kosztują więcej.
*   **Profilowanie Jakości:**
    *   Dużo `SmallPoints`: Druk wysokiej jakości, detale (wolniejszy).
    *   Dużo `BigPoints`: Druk apli, tła (szybszy, ale większe zużycie tuszu).
    *   *Wniosek:* Możemy optymalizować kolejkowanie zleceń (grupować "mokre" wydruki).

## 3. Wykrywanie "Ukrytych" Przestojów (Micro-Stops)
Dane z `TelemetryPoint` (prędkość) mówią nam, kiedy maszyna stoi. Dane z `PrintHistory` mówią nam, *dlaczego* (lub co działo się tuż przedtem).
*   **Czas Międzyzleceniowy (Changeover Time):** Analizując czas między końcem jednego pliku a startem kolejnego (Timestamp z `PrintHistory`), wyliczymy, ile czasu operator traci na załadowanie nowego pliku/rolki.
*   **Korelacja Błędów:** Jeśli widzimy na wykresie Multi-Series, że po plikach o nazwie `*TEST*` lub `*Kalibracja*` następuje długi przestój, wiemy, że proces kalibracji jest wąskim gardłem.

## 4. Weryfikacja Planu vs Rzeczywistość
*   **Długość Roli:** Mamy parametr `PrintLength` (długość wydruku w metrach). Możemy sumować długości zleceń i przewidywać, kiedy skończy się rolka materiału (np. "Za 15 metrów koniec roli - przygotuj zmianę").
*   **Oszacowanie czasu:** Porównanie `FinishArea` z czasem trwania pozwala wyznaczyć rzeczywistą prędkość średnią (m²/h) dla różnych typów grafik, co pozwala lepiej planować przyszłe zlecenia.

---

## Konfiguracja Multi-Series Chart

Aby zwizualizować te dane:

1.  Utwórz Widget typu **Multi-Series Chart**.
2.  Dodaj serię 1: **Prędkość** (z telemetrii bieżącej).
3.  Dodaj serię 2: **Zużycie Tuszu** (metryka `ink_drops`, typ Bar, oś Prawa).
4.  Dodaj serię 3: **Powierzchnia** (metryka `area_m2`, typ Scatter, oś Lewa).

Dzięki temu zobaczysz korelację między prędkością maszyny, wielkością zlecenia a zużyciem atramentu.
