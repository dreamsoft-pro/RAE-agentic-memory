# CI_FIX_PLAN.md
Plan naprawy błędów w CI (lint, testy, Docker build) dla projektu **RAE-agentic-memory**

---

## 1. Szybki przegląd problemów

Z logów GitHub Actions wynikają trzy główne grupy błędów:

1. **Docker Build**
   - Błąd: `failed to read dockerfile: open Dockerfile: no such file or directory`
   - W CI oczekiwany jest `Dockerfile` w katalogu, z którego odpalany jest build.

2. **Lint (black)**
   - `black --check apps/ sdk/ integrations/`
   - 144 pliki wymagają formatowania.
   - Jeden plik powoduje błąd parsowania:
     ```text
     error: cannot format .../integrations/mcp-server/main.py: Cannot parse: 122:0:         return {"message": f"Stopped watching project '{project_id}'."}
     ```

3. **Testy (pytest)**
   - Podczas kolekcji testów brakuje szeregu zależności:
     - `instructor`
     - `scipy`
     - `spacy`
     - `sentence_transformers`
     - `slowapi`
     - `presidio_analyzer`
     - `sklearn` (scikit-learn)
     - `mcp`
   - Przez to 11 testów kończy się błędem importu i cała sesja pytest jest przerywana.

Poniżej szczegółowy plan naprawy krok po kroku.

---

## 2. Naprawa Docker Build

### 2.1. Sprawdź, gdzie znajduje się Dockerfile w repo

Lokalnie w katalogu projektu:

```bash
ls
ls apps
ls infra
Sprawdź, czy istnieje plik:

Dockerfile w katalogu głównym lub

jakiś inny Dockerfile używany wcześniej (np. infra/docker/Dockerfile, docker/Dockerfile, apps/memory_api/Dockerfile itp.).

2.2. Dopasuj ścieżkę w workflow CI
Otwórz .github/workflows/ci.yml i znajdź job Docker Build. Szukaj kroku typu:

yaml
Skopiuj kod
- name: Build Docker image
  uses: docker/build-push-action@v5
  with:
    context: .
    file: Dockerfile
    ...
Dostosuj:

Jeśli Dockerfile ma być w katalogu głównym:

Upewnij się, że plik istnieje w repo (commit + push).

W workflow:

yaml
Skopiuj kod
context: .
file: ./Dockerfile
Jeśli Dockerfile jest np. w infra/docker/Dockerfile:

Ustaw:

yaml
Skopiuj kod
context: .
file: ./infra/docker/Dockerfile
Jeżeli miałeś wcześniej kilka Dockerfile (np. osobno dla memory_api i dla ml_service), rozważ:

Jeden główny Dockerfile dla apps/memory_api

Oddzielne workflow lub matrix build, ale w aktualnym jobie używany powinien być realnie istniejący plik.

Po zmianie:

bash
Skopiuj kod
git add .github/workflows/ci.yml Dockerfile* infra/docker/Dockerfile*  # wg rzeczywistej ścieżki
git commit -m "Fix CI Docker build path to Dockerfile"
git push
3. Naprawa Lint (black)
3.1. Napraw syntax error w integrations/mcp-server/main.py
Błąd black:

text
Skopiuj kod
Cannot parse: 122:0:         return {"message": f"Stopped watching project '{project_id}'."}
Oznacza, że plik ma niepoprawną składnię Pythona (np. zły wcięcie, brakujący nawias lub : wyżej w pliku).

Otwórz plik:

bash
Skopiuj kod
nano integrations/mcp-server/main.py
# lub w ulubionym edytorze
Sprawdź okolice linii ~122:

Upewnij się, że return {"message": ...} jest wewnątrz poprawnie zdefiniowanej funkcji / metody.

Sprawdź, czy wyżej nie brakuje : po definicji funkcji/if/for itp.

Sprawdź, czy nawiasy ()[]{} są domknięte.

Możesz dodatkowo sprawdzić składnię:

bash
Skopiuj kod
python -m py_compile integrations/mcp-server/main.py
Jeśli komenda przejdzie bez błędów, składnia jest poprawna.

Zapisz poprawiony plik i dodaj do commita:

bash
Skopiuj kod
git add integrations/mcp-server/main.py
3.2. Sformatuj kod blackiem lokalnie
Ponieważ CI używa:

bash
Skopiuj kod
black --check apps/ sdk/ integrations/
lokalnie uruchom dokładnie to samo, ale bez --check:

bash
Skopiuj kod
# w katalogu głównym repo
black apps/ sdk/ integrations/
Black automatycznie sformatuje wszystkie wymagające pliki.

Jeśli chcesz sprawdzić, które pliki zmienił:

bash
Skopiuj kod
git status
Powinieneś zobaczyć zmiany w ~144 plikach.

3.3. Commit zmian formatowania
bash
Skopiuj kod
git add apps/ sdk/ integrations/
git commit -m "Apply black formatting across apps, sdk and integrations"
git push
Po tym kroku job Lint w CI powinien przechodzić (zakładając brak nowych zmian łamiących style).

4. Naprawa testów – brakujące zależności
Testy używają wielu „ciężkich” bibliotek, które nie są zainstalowane w środowisku CI. Z logów:

instructor

scipy

spacy

sentence_transformers

slowapi

presidio_analyzer

sklearn (scikit-learn)

mcp (MCP server library)

4.1. Ustal, z jakiego pliku CI instaluje zależności
Otwórz .github/workflows/ci.yml i znajdź sekcję instalacji:

Przykłady:

yaml
Skopiuj kod
- name: Install dependencies
  run: pip install -r apps/memory_api/requirements-base.txt -r apps/memory_api/requirements-dev.txt
albo:

yaml
Skopiuj kod
- name: Install dependencies
  run: pip install -r requirements.txt
Zanotuj, który plik (lub pliki) są używane w CI dla jobów Test (Python 3.10/3.11/3.12).

4.2. Dodaj brakujące paczki do pliku wymagań testowych
Załóżmy, że CI używa apps/memory_api/requirements-dev.txt. W takim wypadku:

Otwórz odpowiedni plik:

bash
Skopiuj kod
nano apps/memory_api/requirements-dev.txt
Dodaj tam brakujące zależności (jeśli nie są jeszcze obecne):

text
Skopiuj kod
instructor
scipy
spacy
sentence-transformers
slowapi
presidio-analyzer
scikit-learn
mcp  # lub pełna nazwa pakietu MCP używanego w projekcie
Uwaga:

Nazwy mogą wymagać doprecyzowania (np. mcp[cli], mcp-server, itp., zależnie od faktycznego pakietu w integrations/mcp-server).

Jeśli masz już osobny requirements-ml.txt lub requirements-mcp.txt, możesz:

albo wciągnąć go w CI dodatkową linią pip install -r ...,

albo dopisać paczki do pliku dev.

Zapisz plik i dodaj do commita:

bash
Skopiuj kod
git add apps/memory_api/requirements-dev.txt
Jeżeli CI używa innego pliku (np. requirements.txt w katalogu głównym), wykonaj analogiczne kroki dla tego pliku.

4.3. (Opcjonalnie) Podział testów na „core” i „heavy”
Jeżeli instalacja powyższych bibliotek za bardzo spowalnia CI, rozważ w kolejnym kroku:

Podział testów na:

Core – bez zależności ML (szybkie, odpalane przy każdym pushu).

Heavy/ML – z ciężkimi bibliotekami, uruchamiane np. tylko na main lub na żądanie.

Realizacja:

Oznacz testy wymagające ML markerem, np. @pytest.mark.ml.

W CI:

domyślny job:

yaml
Skopiuj kod
run: pytest -m "not integration and not ml" ...
osobny job ML Tests z pełnym zestawem zależności i:

yaml
Skopiuj kod
run: pytest -m "ml" ...
Na razie jednak priorytetem jest przejście aktualnego joba – dlatego dodanie brakujących paczek do wymagań jest najszybszą drogą.

4.4. Lokalne uruchomienie testów
Po zaktualizowaniu wymagań:

bash
Skopiuj kod
# w świeżym virtualenv z tymi samymi wersjami Pythona (np. 3.11)
pip install -r <ten_sam_plik_co_CI>
pytest -m "not integration" --cov --cov-report=xml --cov-report=term
Jeżeli lokalnie przechodzą, to jest duża szansa, że CI również przejdzie po kolejnym pushu.

5. Sekwencja działań – co po kolei zrobić
Napraw syntax error w integrations/mcp-server/main.py.

Uruchom lokalnie:

bash
Skopiuj kod
black apps/ sdk/ integrations/
Commit + push formatowania + poprawki MCP main.py.

Popraw ścieżkę do Dockerfile w .github/workflows/ci.yml + zadbaj, żeby Dockerfile był w repo.

Dodaj brakujące zależności do pliku wymagań używanego przez CI (requirements-dev/requirements.txt) i commit+push.

Lokalnie zweryfikuj:

bash
Skopiuj kod
pytest -m "not integration" --cov --cov-report=xml --cov-report=term
Push i obserwuj kolejne uruchomienie CI na GitHubie.

Po wykonaniu powyższego zestawu kroków trzy główne joby:

Lint

Test (Python 3.10/3.11/3.12)

Docker Build

powinny zacząć przechodzić lub przynajmniej wyjść z fazy „brakujące zależności / brak Dockerfile” i ujawnić ewentualne realne błędy logiczne w kodzie.