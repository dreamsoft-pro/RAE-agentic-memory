# RAE Strategic Roadmap: From Memory Store to Cognitive Engine

Ten dokument definiuje strategiczne kierunki rozwoju projektu RAE (Reflective Agentic-memory Engine). Celem jest transformacja projektu z "zaawansowanej bazy wektorowej" w pełnoprawny, kognitywny system operacyjny dla agentów AI, atrakcyjny dla społeczności Open Source.

## Spis treści
1. [Kierunek 1: GraphRAG – Ewolucja w stronę Grafów Wiedzy](#kierunek-1-graphrag--od-wektorów-do-grafów)
2. [Kierunek 3: MCP First – Integracja z IDE i Agentami](#kierunek-3-mcp-first--model-context-protocol)
3. [Kierunek 4: Wizualizacja i Obserwowalność](#kierunek-4-wizualizacja-ui--human-in-the-loop)
4. [Quick Wins – Natychmiastowe ulepszenia w kodzie](#quick-wins--code-level-improvements)

---

## Kierunek 1: GraphRAG – Od wektorów do grafów

Obecne systemy RAG (Retrieval Augmented Generation) cierpią na brak zrozumienia relacji między odległymi fragmentami wiedzy. RAE posiada już szkielet tabel grafowych (`knowledge_graph_nodes`, `edges`), ale nie wykorzystuje ich aktywnie.

### Cel
Wdrożenie **GraphRAG**, aby RAE mógł odpowiadać na pytania typu: *"Jakie jest powiązanie między projektem X a błędami zgłaszanymi przez zespół Y w zeszłym kwartale?"* – czego czyste wektory często nie wyłapują.

### Plan Implementacji

#### 1.1. Automatyczna Ekstrakcja Encji (The "Triples" Extractor)
Zmiana w `ReflectionEngine`. Zamiast generować tylko tekstowe podsumowanie, silnik refleksji powinien ekstrahować trójki: `(Podmiot) -> [RELACJA] -> (Obiekt)`.

* **Input:** Epizody z pamięci (np. "Użytkownik zgłosił błąd w module płatności").
* **Process:** LLM z wymuszonym outputem JSON.
* **Output:**
    ```json
    [
      {"source": "User", "relation": "REPORTED_BUG", "target": "PaymentModule"},
      {"source": "PaymentModule", "relation": "STATUS", "target": "Unstable"}
    ]
    ```
* **Storage:** Zapis do tabel `knowledge_graph_nodes` i `knowledge_graph_edges` w Postgres.

#### 1.2. Wyszukiwanie Hybrydowe 2.0 (Vector + Graph Traversal)
Rozszerzenie endpointu `/memory/query`.
1.  **Vector Step:** Znajdź węzły startowe w grafie najbardziej podobne semantycznie do zapytania.
2.  **Graph Step:** Wykonaj "spacer" (traversal) po grafie (np. 2 skoki w głąb), aby zebrać kontekst relacyjny.
3.  **Synthesis:** Połącz tekst z wektorów i relacje z grafu w jeden kontekst dla LLM.

---

## Kierunek 3: MCP First – Model Context Protocol

Model Context Protocol (MCP) staje się standardem komunikacji między LLM a światem zewnętrznym (promowanym m.in. przez Anthropic). RAE ma potencjał stać się domyślnym "Serwerem Pamięci" dla narzędzi takich jak Cursor, Windsurf czy Claude Desktop.

### Cel
Umożliwić agentom działającym w IDE programisty nie tylko "czytanie plików", ale **aktywne zapamiętywanie decyzji projektowych** i odpytywanie o nie w przyszłości.

### Plan Implementacji

#### 3.1. Rozbudowa `integrations/mcp-server`
Obecny serwer jest pasywny (nasłuchuje zmian plików). Należy go przekształcić w pełnoprawny serwer MCP udostępniający **Narzędzia (Tools)**.

#### 3.2. Definicja Narzędzi (MCP Tools)
Agent po podłączeniu do RAE powinien widzieć następujące tools:

* `save_memory(content: str, tags: list[str])` – Agent w IDE może jawnie zapisać: "Zdecydowaliśmy się użyć biblioteki X zamiast Y, bo jest szybsza".
* `search_memory(query: str)` – Agent przed napisaniem kodu może sprawdzić: "Czy mamy jakieś ustalone wzorce dla obsługi błędów?".
* `get_related_context(file_path: str)` – "Co wiemy o tym module z przeszłości?".

#### 3.3. Kontekst "Resource"
Udostępnienie "Reflective Memory" jako zasobu MCP, który jest stale wstrzykiwany do kontekstu rozmowy (np. jako `system prompt` w IDE), zawierający najważniejsze zasady projektu.

---

## Kierunek 4: Wizualizacja UI – Human-in-the-Loop

Pamięć AI jest "czarną skrzynką". Użytkownicy nie ufają systemom, których stanu nie widzą. Grafana jest dla adminów, a deweloperzy potrzebują wglądu w "mózg" agenta.

### Cel
Stworzenie lekkiego dashboardu, który pozwala zrozumieć, co RAE wie, i korygować błędy (np. halucynacje).

### Plan Implementacji

#### 4.1. Stack Technologiczny
Zalecany: **Streamlit** lub **NiceGUI** (Python).
* Dlaczego? Pozwala utrzymać cały projekt w Pythonie, łatwy do modyfikacji przez społeczność Data Science/AI.

#### 4.2. Kluczowe Widoki
1.  **Memory Timeline:** Oś czasu pokazująca epizody (zdarzenia). Możliwość filtrowania po `session_id` lub tagach.
2.  **Knowledge Graph Visualizer:** Interaktywny graf (np. biblioteka `agraph` lub `pyvis`) pokazujący węzły i krawędzie z Postgresa.
3.  **Memory Editor:** Tabela z możliwością edycji treści wspomnień lub ich "zapominania" (soft-delete).
4.  **Inspection Mode:** Wklejasz Prompt użytkownika -> Widzisz co RAE zwróci (Retrieve + Rerank score).

---

## Quick Wins – Code Level Improvements

Zmiany, które można wdrożyć w 1-2 dni, a które drastycznie podniosą jakość kodu i UX dewelopera (`DX`).

### 1. Structured Outputs (JSON Mode)
**Problem:** W `apps/memory-api/services/llm/base.py` zwracasz czysty tekst (`str`). Parsowanie tego jest podatne na błędy.
**Rozwiązanie:** Wykorzystaj natywne tryby JSON modeli (OpenAI/Gemini) i Pydantic.

```python
# Sugerowana zmiana w interfejsie LLMProvider
from pydantic import BaseModel

class LLMProvider(Protocol):
    async def generate_structured(self, model: str, response_model: Type[BaseModel], prompt: str) -> BaseModel:
        ...
Ułatwi to implementację GraphRAG (ekstrakcja trójek) i Reflection.

2. Recursive Summarization w ReflectionEngine
Problem: Przy dużej liczbie epizodów, wrzucenie wszystkiego w jeden prompt przekroczy context window lub obniży jakość ("lost in the middle"). Rozwiązanie: Zaimplementuj algorytm Map-Reduce lub hierarchicznego podsumowania w apps/memory-api/services/reflection_engine.py.

Grupuj epizody w "koszyki" (np. po 10).

Podsumuj każdy koszyk.

Podsumuj podsumowania, aby uzyskać "Meta-Insight".

3. Dekorator @rae.trace (SDK Improvement)
Problem: Deweloperzy muszą ręcznie wołać client.store_memory. To duży narzut pracy. Rozwiązanie: Dodaj do sdk/python/rae_memory_sdk dekorator, który automatycznie loguje wejście i wyjście funkcji.

Python

# sdk/python/rae_memory_sdk/decorators.py

def trace_memory(client: MemoryClient, layer="episodic"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Async background task:
            client.store_memory(
                content=f"Function {func.__name__} called with {args}. Result: {result}",
                layer=layer,
                source="code_trace"
            )
            return result
        return wrapper
    return decorator
To "Killer Feature" dla szybkiej adopcji SDK.