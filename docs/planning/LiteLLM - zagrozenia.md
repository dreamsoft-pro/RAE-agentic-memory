LiteLLM - biblioteka z ~97 milionami pobrań miesięcznie - została skompromitowana. Wersje 1.82.7 i 1.82.8 na PyPI zawierały malware:
↳ Kradł klucze SSH, tokeny AWS/GCP/Azure, pliki .env, portfele krypto
↳ Rozprzestrzeniał się po Kubernetes
↳ Instalował trwały backdoor
↳ Uruchamiał się automatycznie - wystarczył pip install, zero importu

Konto maintainera zostało w pełni przejęte.
GitHub issue zamknięto jako "not planned" - bo atakujący kontrolował już repo.
160+ commitów w kilka minut. Setki botów zalewających dyskusję.

Malware wykryto, bo... miał buga. Tworzył fork bomb, który crashował maszynę.
Gdyby nie ten błąd w złośliwym kodzie - działałby po cichu znacznie dłużej.
To nie teoria. To się wydarzyło wczoraj.

Ale ten post nie jest o LiteLLM.
Jest o pytaniu, które zadaję od lat.

Po co? Po co dodawać zależność, która:
↳ Opakowuje coś, co możesz wywołać bezpośrednio?
↳ Wprowadza tysiące linii kodu, których nigdy nie czytasz?
↳ Staje się single point of failure dla wszystkich Twoich kluczy API?

LiteLLM to "uniwersalny proxy" do 100+ modeli LLM.
Jedno miejsce, przez które przechodzą Twoje klucze do OpenAI, Anthropic, Google, AWS.

Wygodne? Być może.
Ale wygoda to nie to samo co kontrola.

I tutaj jest szerszy problem.
LiteLLM to nie tylko standalone.
To zależność w DSPy, CrewAI i 2300+ innych pakietach.
88% z nich miało luźne specyfikacje wersji.

Złośliwa wersja wchodziła cicho - jako transitive dependency.

Jeden z przypadków: malware wszedł przez plugin MCP uruchomiony w Cursorze. MCP → LiteLLM → Twoje klucze.

W świecie AI pomieszały się przyczyny ze skutkami.
Duże biblioteki miały dawać "wygodę" i "przyspieszenie".

W praktyce? 
Tracisz kontrolę nad kontekstem. Dodajesz ryzyko. I nie wiesz nawet, co dokładnie działa pod spodem.

A potem pytanie: jaką realną wartość to dodaje?

czy powinniśmy używać LiteLLM. Ani LangChain. Ani X (inny kombajn).
Nie dlatego, że przewidzieliśmy ten konkretny atak.
Ale dlatego, że nasz filtr jest prosty:
jeśli coś dodaje złożoność — a wartość da się osiągnąć prościej — nie wchodzi do stacka.
Mniej zależności = mniejsza powierzchnia ataku.
Mniej abstrakcji = więcej kontroli.

Oczywiście - security issue może się przydarzyć każdej bibliotece.
Nawet jądro Linuksa miało swoje. Ale jest różnica między zależnością konieczną a zależnością, która jest tam, bo "wszyscy tego używają".

Co zrobić teraz — konkretnie:
↳ Sprawdź: "pip show litellm" - jeśli 1.82.7 lub 1.82.8, działaj natychmiast
↳ Pamiętaj: LiteLLM bywa transitive dependency - sprawdź "pip list" 
↳ Szukaj: `~/.config/sysmon/sysmon.py` — persistence backdoor
↳ Zrotuj WSZYSTKIE credentials, które były na tej maszynie
↳ Pinuj wersje w zależności - zawsze, nie tylko teraz