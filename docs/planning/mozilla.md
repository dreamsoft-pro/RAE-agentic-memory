Poniżej masz gotowy szkic flow modelowego wdrożenia RAE dla Mozilla Foundation. Ułożyłem go tak, żeby pasował do małej organizacji obywatelskiej, watchdoga albo lokalnej redakcji.

Modelowe wdrożenie RAE dla Mozilla Foundation
1. Cel wdrożenia

Celem wdrożenia jest zbudowanie lokalnego lub kontrolowanego przez użytkownika systemu AI, który pomaga organizacji pracować z informacją publiczną w sposób:

bardziej przejrzysty,

bardziej weryfikowalny,

mniej zależny od zamkniętych platform,

bezpieczniejszy dla danych i procesu myślenia.

RAE nie ma zastępować człowieka. Ma działać jako warstwa pamięci, retrievalu i refleksji, która wspiera ludzi w analizie materiałów publicznych i pilnuje jakości odpowiedzi AI.

2. Typowy użytkownik

Modelowy odbiorca:

mała organizacja obywatelska,

watchdog lokalny,

niezależna redakcja,

grupa społeczna analizująca dokumenty publiczne,

badacz lub mały zespół monitorujący decyzje instytucji.

To ważne, bo taki użytkownik zwykle:

nie ma dużego budżetu,

nie ma własnego zespołu ML,

potrzebuje prostego wdrożenia,

chce zachować kontrolę nad danymi,

potrzebuje odpowiedzi, które można sprawdzić.

3. Modelowy scenariusz użycia

Przykład:

organizacja monitoruje decyzje samorządu, zamówienia publiczne, uchwały, protokoły, sprawozdania, pisma urzędowe i lokalne materiały prasowe.

Chce móc zapytać system:

„Jak zmieniał się argument urzędu w tej sprawie w ostatnich 8 miesiącach?”

„Które dokumenty potwierdzają tę tezę?”

„Pokaż streszczenie, ale zaznacz miejsca o niskiej pewności.”

„Czy ta odpowiedź ma pokrycie w źródłach?”

„Jakie dokumenty są kluczowe, a jakie tylko pomocnicze?”

4. Flow wdrożenia end-to-end
Etap 1: Zbieranie materiałów

Do systemu trafiają:

dokumenty publiczne PDF,

uchwały i protokoły,

materiały z BIP,

raporty i sprawozdania,

artykuły i notatki prasowe,

własne notatki zespołu,

lokalne archiwa dokumentów.

Na tym etapie ważna jest zasada:
RAE nie zaczyna od generowania odpowiedzi. Zaczyna od budowy kontrolowanej bazy wiedzy z zachowanym pochodzeniem danych.

Etap 2: Ingestia i normalizacja

System:

importuje dokumenty,

dzieli je logicznie na fragmenty,

zapisuje metadane,

zachowuje provenance,

tworzy warstwę pamięci semantycznej i roboczej,

przygotowuje dane do retrievalu.

Każdy fragment powinien zachować informacje typu:

źródło,

data,

typ dokumentu,

instytucja,

poziom zaufania lub status,

powiązania z innymi materiałami.

To jest kluczowe dla Mozilli, bo pokazuje, że system nie działa jak „chat znikąd”, tylko jak środowisko pracy ze śledzeniem pochodzenia informacji.

Etap 3: Budowa pamięci RAE

Tutaj uruchamiasz właściwy sens RAE.

Pamięć epizodyczna

Przechowuje historię interakcji, pytań, wcześniejszych analiz, decyzji użytkownika.

Pamięć robocza

Trzyma aktywny kontekst bieżącej sprawy: wybrane dokumenty, najważniejsze hipotezy, aktualne pytanie.

Pamięć semantyczna

Przechowuje trwałe relacje, pojęcia, streszczenia, wzorce i wiedzę uogólnioną wynikającą z dokumentów.

Pamięć refleksyjna

Przechowuje wnioski o jakości wcześniejszych odpowiedzi, błędach, brakach źródeł, powtarzających się problemach.

To bardzo dobrze brzmi grantowo, ale też technicznie:
RAE nie tylko „pamięta”, ale uczy się ostrożności i jakości pracy z informacją.

Etap 4: Zapytanie użytkownika

Użytkownik zadaje pytanie w języku naturalnym.

Przykład:

„Czy w dokumentach miasta są rozbieżności między uzasadnieniem podwyżki a wcześniejszymi obietnicami?”

System nie odpowiada od razu.
Najpierw:

analizuje intencję,

identyfikuje potrzebny zakres źródeł,

pobiera odpowiednie fragmenty z pamięci i repozytorium,

buduje zestaw dowodów.

Etap 5: Retrieval i budowa szkicu odpowiedzi

Na tym etapie model AI:

przegląda dobrane źródła,

tworzy szkic odpowiedzi,

przypisuje odpowiedzi do materiału źródłowego,

zaznacza niepewność,

może tworzyć kilka wariantów szkicu.

To ważne:
odpowiedź jeszcze nie jest finalna.

Etap 6: Refleksja i audyt odpowiedzi

To jest serce modelowego wdrożenia dla Mozilli.

RAE uruchamia warstwę refleksji, która sprawdza:

czy odpowiedź ma wystarczające pokrycie w źródłach,

czy model nie wyszedł poza dowody,

czy niepewność nie jest zbyt wysoka,

czy w odpowiedzi nie ma pozornej pewności,

czy należy ją dopuścić, poprawić, czy zablokować.

Najprostszy flow decyzji:

draft -> review -> pass / revise / block

To daje bardzo mocny przekaz dla Mozilli:
system nie tylko generuje treść, ale ma mechanizm samoograniczania, kiedy odpowiedź nie jest wystarczająco dobrze ugruntowana.

Etap 7: Human in the loop

Jeżeli odpowiedź przejdzie warstwę refleksji, trafia do człowieka z dodatkowymi informacjami:

źródła wykorzystane do odpowiedzi,

poziom pewności,

miejsca niejednoznaczne,

brakujące dane,

ewentualne ostrzeżenia.

Człowiek może:

zaakceptować odpowiedź,

poprawić ją,

poprosić o wersję bardziej ostrożną,

zawęzić zakres źródeł,

odrzucić wynik.

To jest bardzo ważne, bo podkreśla, że projekt wzmacnia ludzki osąd, a nie go zastępuje.

Etap 8: Publikacja lub użycie wewnętrzne

Wynik może zostać użyty jako:

streszczenie dokumentów,

nota robocza,

materiał do artykułu,

briefing dla organizacji,

analiza porównawcza,

lista pytań do instytucji,

pomoc w przygotowaniu wniosku o dostęp do informacji publicznej.

Ważne jest, że RAE może generować nie tylko odpowiedź, ale też:

listę źródeł,

wskazanie luk,

listę twierdzeń wymagających weryfikacji,

mapę zależności między dokumentami.

Etap 9: Zapis do pamięci i uczenie jakościowe

Po zakończeniu pracy:

zapisywana jest historia zapytania,

wynik refleksji trafia do pamięci refleksyjnej,

system zapamiętuje, które typy odpowiedzi były dobre,

które wymagały poprawek,

gdzie najczęściej pojawiał się brak pokrycia źródłami.

Dzięki temu kolejne odpowiedzi mogą być ostrożniejsze i bardziej dopasowane do praktyki danej organizacji.

5. Model architektoniczny wdrożenia
Wariant A — Local-first

Najmocniejszy pod Mozillę.

całość działa lokalnie,

lokalny storage,

lokalny model albo kontrolowany provider,

brak obowiązkowej chmury,

pełna kontrola nad danymi.

To jest idealny wariant do opisu grantowego jako profil bazowy.

Wariant B — Local + controlled sync

Dobry dla kilkuosobowej organizacji.

pamięć lokalna,

synchronizacja tylko za zgodą,

współdzielenie wybranych zasobów,

audyt przepływu danych.

Wariant C — Federated civic deployment

Na późniejszy etap.

kilka organizacji ma własne instancje,

współdzielą tylko wybrane zasoby,

zachowują autonomię,

nie ma jednej centralnej platformy.

To jest bardzo dobre jako future vision, ale nie jako pierwszy pilot.

6. Minimalny flow pilotażowy pod grant

Jeśli chcesz to pokazać prosto, to najlepiej tak:

Pilot 1

Mała organizacja obywatelska lub lokalny watchdog
↓
Import publicznych dokumentów
↓
Budowa lokalnej pamięci RAE
↓
Zadawanie pytań o dokumenty i sprawy publiczne
↓
Draft odpowiedzi generowany przez AI
↓
Audyt odpowiedzi przez warstwę refleksji
↓
Wynik: pass / revise / block
↓
Człowiek zatwierdza lub poprawia
↓
Wynik trafia do dalszej pracy i pamięci systemu

To jest bardzo czytelny flow do formularza, decku albo 2-minutowego video.

7. Co Mozilla chce tu zobaczyć

W tym flow najmocniejsze dla Mozilli są cztery rzeczy:

1. AI jest potrzebne do skali

Bo trzeba szybko pracować na dużych zbiorach treści.

2. RAE ogranicza ryzyka AI

Bo nie pozwala bezkrytycznie ufać pierwszej odpowiedzi.

3. Projekt wzmacnia autonomię

Bo może działać lokalnie i nie wymaga oddania danych platformie.

4. Projekt ma sens obywatelski

Bo dotyczy informacji publicznej, przejrzystości i jakości wiedzy wspólnotowej.

8. Najkrótsza wersja tego flow do wniosku

Możesz użyć takiego skrótu po angielsku albo po polsku:

Modelowe wdrożenie RAE polega na uruchomieniu lokalnego systemu AI dla organizacji obywatelskiej lub niezależnej redakcji. Organizacja importuje dokumenty publiczne i własne materiały robocze, RAE buduje warstwę pamięci z zachowaniem pochodzenia danych, a użytkownicy zadają pytania w języku naturalnym. Model generuje szkic odpowiedzi, po czym warstwa refleksji ocenia pokrycie źródłami, poziom niepewności i ryzyko błędu. Odpowiedź może zostać zaakceptowana, skierowana do poprawy albo zablokowana. Człowiek zachowuje kontrolę nad decyzją końcową, a system uczy się jakościowo na podstawie wcześniejszych interakcji.

To już jest prawie gotowy opis „deployment flow”.

9. Moja rekomendacja

Do Mozilli pokazałbym jeden modelowy pilot:

local watchdog / local newsroom / civic NGO
a nie kilka naraz.