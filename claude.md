# Claude CLI - Instrukcje Implementacji RAE Roadmap

## Kontekst Projektu
RAE (Reflective Agentic-memory Engine) to zaawansowany system pamięci dla agentów AI z architekturą wielowarstwową (episodic, working, semantic, long-term memory). Projekt jest napisany w Pythonie z FastAPI, PostgreSQL+pgvector/Qdrant, Redis i Celery.

## Twoje Zadanie
Zaimplementuj funkcjonalności opisane w pliku WORKING.md, iteracyjnie przechodząc przez każdy kierunek rozwoju.

---

## KIERUNEK 1: GraphRAG - Ewolucja w stronę Grafów Wiedzy

### Zadanie 1.1: Automatyczna Ekstrakcja Encji (The "Triples" Extractor)

**Cel:** Rozszerz `ReflectionEngine` o ekstrakcję trójek (Subject-Relation-Object) z epizodów pamięci.

**Kroki:**

1. **Utwórz nowy moduł ekstrakcji encji:**
   ```
   apps/memory-api/services/graph_extraction.py
   ```

2. **Zaimplementuj Pydantic models dla struktury grafu:**
   ```python
   from pydantic import BaseModel
   from typing import List, Optional

   class GraphTriple(BaseModel):
       source: str
       relation: str
       target: str
       confidence: Optional[float] = 1.0
       metadata: Optional[dict] = {}

   class GraphExtractionResult(BaseModel):
       triples: List[GraphTriple]
       extracted_entities: List[str]
   ```

3. **Dodaj metodę ekstrakcji do LLMProvider:**
   - W `apps/memory-api/services/llm/base.py` dodaj:
   ```python
   async def generate_structured(
       self, 
       model: str, 
       response_model: Type[BaseModel], 
       prompt: str
   ) -> BaseModel:
       """Generate structured output conforming to Pydantic model"""
       pass
   ```

4. **Zaimplementuj metodę dla każdego providera:**
   - OpenAI: Użyj `response_format={"type": "json_object"}` + prompt engineering
   - Gemini: Użyj `generation_config` z JSON schema
   - Ollama: Użyj JSON mode jeśli dostępny, w przeciwnym razie parsuj output

5. **Rozszerz ReflectionEngine:**
   - W `apps/memory-api/services/reflection_engine.py` dodaj:
   ```python
   async def extract_knowledge_graph(
       self, 
       project_id: str, 
       tenant_id: str,
       limit: int = 50
   ) -> GraphExtractionResult:
       """Extract graph triples from episodic memories"""
       # 1. Fetch recent episodic memories
       # 2. Create extraction prompt
       # 3. Call LLM with GraphExtractionResult as response_model
       # 4. Return structured triples
   ```

6. **Prompt template dla ekstrakcji:**
   ```python
   GRAPH_EXTRACTION_PROMPT = """
   Analyze the following memories and extract relationships in the form of triples.
   
   Memories:
   {memories_text}
   
   Extract:
   - Entities (people, projects, modules, concepts)
   - Relationships between them (REPORTED_BUG, FIXED_BY, DEPENDS_ON, etc.)
   
   Return ONLY valid JSON with structure:
   {
     "triples": [
       {"source": "Entity1", "relation": "RELATION_TYPE", "target": "Entity2"}
     ],
     "extracted_entities": ["Entity1", "Entity2"]
   }
   """
   ```

7. **Utwórz endpoint API:**
   ```
   POST /graph/extract
   - Request: { "project_id": str, "tenant_id": str, "limit": int }
   - Response: GraphExtractionResult
   ```

8. **Zapisz do bazy danych:**
   - Wykorzystaj istniejące tabele `knowledge_graph_nodes` i `knowledge_graph_edges`
   - W `apps/memory-api/db/operations.py` dodaj:
   ```python
   async def store_graph_triple(
       pool, 
       tenant_id: str, 
       project_id: str,
       triple: GraphTriple
   ):
       # Insert nodes if not exist
       # Insert edge
   ```

### Zadanie 1.2: Wyszukiwanie Hybrydowe 2.0

**Cel:** Połącz wyszukiwanie wektorowe z traversalem grafu.

**Kroki:**

1. **Utwórz nowy moduł:**
   ```
   apps/memory-api/services/hybrid_search.py
   ```

2. **Zaimplementuj HybridSearchService:**
   ```python
   class HybridSearchService:
       def __init__(self, pool, vector_store):
           self.pool = pool
           self.vector_store = vector_store
       
       async def search(
           self, 
           query: str,
           tenant_id: str,
           project_id: str,
           graph_depth: int = 2,
           top_k_vector: int = 5
       ) -> List[dict]:
           # 1. Vector search - znajdź najbliższe węzły startowe
           # 2. Graph traversal - przejdź po grafie (BFS/DFS)
           # 3. Merge results - połącz kontekst
           # 4. Rerank by relevance
   ```

3. **Implementacja graph traversal:**
   ```python
   async def traverse_graph(
       self,
       start_node_ids: List[str],
       depth: int = 2
   ) -> List[dict]:
       """BFS traversal from start nodes"""
       # Użyj rekurencyjnego SQL lub iteracyjnego BFS
       # Zwróć wszystkie osiągnięte węzły i krawędzie
   ```

4. **SQL query dla traversal (PostgreSQL):**
   ```sql
   WITH RECURSIVE graph_traverse AS (
       -- Base case: start nodes
       SELECT node_id, 0 as depth
       FROM knowledge_graph_nodes
       WHERE node_id = ANY($1)
       
       UNION
       
       -- Recursive case
       SELECT e.target_id, gt.depth + 1
       FROM graph_traverse gt
       JOIN knowledge_graph_edges e ON gt.node_id = e.source_id
       WHERE gt.depth < $2
   )
   SELECT DISTINCT * FROM graph_traverse;
   ```

5. **Rozszerz endpoint `/memory/query`:**
   - Dodaj parametry: `use_graph=True`, `graph_depth=2`
   - Jeśli `use_graph=True`, użyj HybridSearchService zamiast prostego vector search

6. **Context synthesis:**
   ```python
   async def synthesize_context(
       self,
       vector_results: List[dict],
       graph_results: List[dict]
   ) -> str:
       """Merge vector and graph context for LLM"""
       # Format: "Vector Context: ... \n\n Graph Relations: ..."
   ```

---

## KIERUNEK 2: Quick Wins - Code Level Improvements

### Zadanie 2.1: Structured Outputs (JSON Mode)

**Cel:** Wymuszenie strukturalnych outputów z LLM.

**Kroki:**

1. **Zmodyfikuj `apps/memory-api/services/llm/base.py`:**
   ```python
   class LLMProvider(Protocol):
       async def generate(self, model: str, prompt: str) -> LLMResult:
           ...
       
       async def generate_structured(
           self, 
           model: str, 
           response_model: Type[BaseModel], 
           prompt: str
       ) -> BaseModel:
           """Generate structured output conforming to Pydantic schema"""
           ...
   ```

2. **Implementuj dla OpenAI (`llm/openai.py`):**
   ```python
   async def generate_structured(
       self, 
       model: str, 
       response_model: Type[BaseModel], 
       prompt: str
   ) -> BaseModel:
       schema = response_model.model_json_schema()
       
       response = await self.client.chat.completions.create(
           model=model,
           messages=[{"role": "user", "content": prompt}],
           response_format={
               "type": "json_schema",
               "json_schema": {
                   "name": response_model.__name__,
                   "schema": schema
               }
           }
       )
       
       json_str = response.choices[0].message.content
       return response_model.model_validate_json(json_str)
   ```

3. **Implementuj dla Gemini (`llm/gemini.py`):**
   ```python
   async def generate_structured(
       self, 
       model: str, 
       response_model: Type[BaseModel], 
       prompt: str
   ) -> BaseModel:
       schema = response_model.model_json_schema()
       
       generation_config = genai.GenerationConfig(
           response_mime_type="application/json",
           response_schema=schema
       )
       
       model_obj = genai.GenerativeModel(model)
       response = await model_obj.generate_content_async(
           prompt,
           generation_config=generation_config
       )
       
       return response_model.model_validate_json(response.text)
   ```

4. **Implementuj dla Ollama (fallback parsing):**
   ```python
   async def generate_structured(
       self, 
       model: str, 
       response_model: Type[BaseModel], 
       prompt: str
   ) -> BaseModel:
       # Ollama może nie wspierać schema
       # Dodaj do promptu JSON schema i parsuj output
       schema = response_model.model_json_schema()
       enhanced_prompt = f"""
       {prompt}
       
       IMPORTANT: Respond ONLY with valid JSON matching this schema:
       {json.dumps(schema, indent=2)}
       """
       
       response = await self.generate(model, enhanced_prompt)
       
       # Clean markdown code blocks if present
       text = response.text.strip()
       text = text.replace("```json", "").replace("```", "").strip()
       
       return response_model.model_validate_json(text)
   ```

### Zadanie 2.2: Recursive Summarization w ReflectionEngine

**Cel:** Hierarchiczne podsumowanie dla dużej liczby epizodów.

**Kroki:**

1. **W `apps/memory-api/services/reflection_engine.py` dodaj:**
   ```python
   async def generate_hierarchical_reflection(
       self,
       project_id: str,
       tenant_id: str,
       bucket_size: int = 10
   ) -> str:
       """
       Hierarchical (Map-Reduce) summarization of episodes
       """
       # 1. Fetch all episodes
       episodes = await self._fetch_episodes(project_id, tenant_id)
       
       if len(episodes) <= bucket_size:
           return await self._summarize_episodes(episodes)
       
       # 2. Split into buckets
       buckets = [
           episodes[i:i+bucket_size] 
           for i in range(0, len(episodes), bucket_size)
       ]
       
       # 3. Summarize each bucket (Map phase)
       summaries = []
       for bucket in buckets:
           summary = await self._summarize_episodes(bucket)
           summaries.append(summary)
       
       # 4. Summarize summaries (Reduce phase)
       if len(summaries) <= bucket_size:
           return await self._summarize_summaries(summaries)
       else:
           # Recursive call for deep hierarchies
           return await self._recursive_reduce(summaries, bucket_size)
   
   async def _summarize_episodes(self, episodes: List[dict]) -> str:
       """Summarize a small batch of episodes"""
       prompt = f"""
       Analyze these events and extract key insights:
       
       {self._format_episodes(episodes)}
       
       Provide a concise summary of patterns, decisions, and important events.
       """
       result = await self.llm_provider.generate(
           model=settings.RAE_LLM_MODEL_DEFAULT,
           prompt=prompt
       )
       return result.text
   
   async def _recursive_reduce(
       self, 
       summaries: List[str], 
       bucket_size: int
   ) -> str:
       """Recursively reduce summaries"""
       if len(summaries) <= bucket_size:
           return await self._summarize_summaries(summaries)
       
       buckets = [
           summaries[i:i+bucket_size]
           for i in range(0, len(summaries), bucket_size)
       ]
       
       meta_summaries = []
       for bucket in buckets:
           meta = await self._summarize_summaries(bucket)
           meta_summaries.append(meta)
       
       return await self._recursive_reduce(meta_summaries, bucket_size)
   ```

2. **Dodaj endpoint:**
   ```
   POST /reflection/hierarchical
   ```

### Zadanie 2.3: Dekorator @rae.trace (SDK Improvement)

**Cel:** Automatyczne logowanie wykonania funkcji.

**Kroki:**

1. **Utwórz plik:**
   ```
   sdk/python/rae_memory_sdk/decorators.py
   ```

2. **Implementuj dekorator:**
   ```python
   import functools
   import asyncio
   import inspect
   from typing import Callable, Optional
   from .client import MemoryClient
   
   def trace_memory(
       client: MemoryClient,
       layer: str = "episodic",
       tags: Optional[list] = None,
       capture_args: bool = True,
       capture_result: bool = True
   ):
       """
       Decorator to automatically trace function execution to RAE memory.
       
       Usage:
           @trace_memory(client, layer="episodic", tags=["api-call"])
           def my_function(x, y):
               return x + y
       """
       def decorator(func: Callable):
           @functools.wraps(func)
           def sync_wrapper(*args, **kwargs):
               # Execute function
               result = func(*args, **kwargs)
               
               # Build memory content
               content = f"Function '{func.__name__}' executed"
               if capture_args:
                   content += f" with args={args}, kwargs={kwargs}"
               if capture_result:
                   content += f". Result: {result}"
               
               # Store asynchronously in background
               asyncio.create_task(
                   client.store_memory(
                       content=content,
                       layer=layer,
                       source=f"trace/{func.__module__}.{func.__name__}",
                       tags=tags or []
                   )
               )
               
               return result
           
           @functools.wraps(func)
           async def async_wrapper(*args, **kwargs):
               # Execute function
               result = await func(*args, **kwargs)
               
               # Build memory content
               content = f"Async function '{func.__name__}' executed"
               if capture_args:
                   content += f" with args={args}, kwargs={kwargs}"
               if capture_result:
                   content += f". Result: {result}"
               
               # Store in background task
               asyncio.create_task(
                   client.store_memory(
                       content=content,
                       layer=layer,
                       source=f"trace/{func.__module__}.{func.__name__}",
                       tags=tags or []
                   )
               )
               
               return result
           
           # Return appropriate wrapper
           if asyncio.iscoroutinefunction(func):
               return async_wrapper
           else:
               return sync_wrapper
       
       return decorator
   ```

3. **Dodaj przykład użycia do README:**
   ```python
   from rae_memory_sdk import MemoryClient
   from rae_memory_sdk.decorators import trace_memory
   
   client = MemoryClient(api_url="http://localhost:8000")
   
   @trace_memory(client, layer="episodic", tags=["business-logic"])
   def process_payment(amount: float, user_id: str):
       # Business logic here
       return {"status": "success", "transaction_id": "123"}
   
   # Function execution is automatically logged to RAE
   result = process_payment(99.99, "user-456")
   ```

---

## KIERUNEK 3: MCP First - Model Context Protocol Integration

### Zadanie 3.1: Rozbudowa `integrations/mcp-server`

**Cel:** Przekształć pasywny watcher w aktywny MCP server.

**Kroki:**

1. **Przeanalizuj obecny kod:**
   ```
   integrations/mcp-server/src/rae_mcp_server/server.py
   ```

2. **Dodaj MCP Tools definitions:**
   ```python
   from mcp.server.models import Tool
   from mcp.server import Server
   import mcp.types as types
   
   # Define tools
   TOOLS = [
       Tool(
           name="save_memory",
           description="Store a memory in RAE for later retrieval",
           inputSchema={
               "type": "object",
               "properties": {
                   "content": {
                       "type": "string",
                       "description": "The content to remember"
                   },
                   "tags": {
                       "type": "array",
                       "items": {"type": "string"},
                       "description": "Tags for categorization"
                   },
                   "layer": {
                       "type": "string",
                       "enum": ["episodic", "working", "semantic", "ltm"],
                       "default": "episodic"
                   }
               },
               "required": ["content"]
           }
       ),
       Tool(
           name="search_memory",
           description="Search RAE memory for relevant information",
           inputSchema={
               "type": "object",
               "properties": {
                   "query": {
                       "type": "string",
                       "description": "Search query"
                   },
                   "top_k": {
                       "type": "integer",
                       "default": 5
                   }
               },
               "required": ["query"]
           }
       ),
       Tool(
           name="get_related_context",
           description="Get historical context about a file or module",
           inputSchema={
               "type": "object",
               "properties": {
                   "file_path": {
                       "type": "string",
                       "description": "Path to the file"
                   }
               },
               "required": ["file_path"]
           }
       )
   ]
   ```

3. **Implementuj tool handlers:**
   ```python
   @server.call_tool()
   async def handle_call_tool(
       name: str, 
       arguments: dict
   ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
       
       if name == "save_memory":
           result = await rae_client.store_memory(
               content=arguments["content"],
               tags=arguments.get("tags", []),
               layer=arguments.get("layer", "episodic")
           )
           return [types.TextContent(
               type="text",
               text=f"Memory stored with ID: {result['id']}"
           )]
       
       elif name == "search_memory":
           results = await rae_client.query_memory(
               query=arguments["query"],
               top_k=arguments.get("top_k", 5)
           )
           formatted = "\n\n".join([
               f"[Score: {r['score']:.2f}] {r['content']}"
               for r in results
           ])
           return [types.TextContent(
               type="text",
               text=formatted
           )]
       
       elif name == "get_related_context":
           # Query by file path in tags or source
           results = await rae_client.query_memory(
               query=f"file:{arguments['file_path']}",
               top_k=10
           )
           # Format as context
           context = format_file_context(results)
           return [types.TextContent(
               type="text",
               text=context
           )]
       
       raise ValueError(f"Unknown tool: {name}")
   ```

4. **Dodaj MCP Resource dla "Project Memory":**
   ```python
   @server.list_resources()
   async def handle_list_resources() -> list[types.Resource]:
       return [
           types.Resource(
               uri="rae://project/reflection",
               name="Project Reflection",
               description="Current reflective insights about the project",
               mimeType="text/plain"
           )
       ]
   
   @server.read_resource()
   async def handle_read_resource(uri: str) -> str:
       if uri == "rae://project/reflection":
           # Fetch latest reflection
           reflection = await rae_client.get_latest_reflection()
           return reflection
       raise ValueError(f"Unknown resource: {uri}")
   ```

5. **Zaktualizuj konfigurację dla IDE:**
   ```json
   // For Claude Desktop / Cursor
   {
     "mcpServers": {
       "rae-memory": {
         "command": "python",
         "args": ["-m", "rae_mcp_server"],
         "env": {
           "RAE_API_URL": "http://localhost:8000",
           "RAE_PROJECT_ID": "my-project"
         }
       }
     }
   }
   ```

### Zadanie 3.2: Continuous Context Injection

**Cel:** Automatyczne wstrzykiwanie kluczowych wspomnień do kontekstu IDE.

**Kroki:**

1. **W MCP server dodaj:**
   ```python
   @server.list_prompts()
   async def handle_list_prompts() -> list[types.Prompt]:
       return [
           types.Prompt(
               name="project-guidelines",
               description="Key project guidelines from RAE memory",
               arguments=[]
           )
       ]
   
   @server.get_prompt()
   async def handle_get_prompt(
       name: str, 
       arguments: dict
   ) -> types.GetPromptResult:
       if name == "project-guidelines":
           # Fetch high-importance semantic memories
           guidelines = await rae_client.query_memory(
               query="coding guidelines project conventions",
               layer="semantic",
               top_k=10
           )
           
           formatted = "PROJECT GUIDELINES:\n\n"
           for g in guidelines:
               formatted += f"- {g['content']}\n"
           
           return types.GetPromptResult(
               messages=[
                   types.PromptMessage(
                       role="user",
                       content=types.TextContent(
                           type="text",
                           text=formatted
                       )
                   )
               ]
           )
   ```

---

## KIERUNEK 4: Wizualizacja UI - Human-in-the-Loop

### Zadanie 4.1: Stworzenie Dashboard w Streamlit

**Cel:** Lekki dashboard do wizualizacji i edycji pamięci.

**Kroki:**

1. **Utwórz nowy katalog:**
   ```
   tools/memory-dashboard/
   ```

2. **Struktura:**
   ```
   tools/memory-dashboard/
   ├── app.py (main Streamlit app)
   ├── pages/
   │   ├── 1_Timeline.py
   │   ├── 2_Knowledge_Graph.py
   │   ├── 3_Memory_Editor.py
   │   └── 4_Query_Inspector.py
   ├── utils/
   │   ├── api_client.py
   │   └── visualizations.py
   └── requirements.txt
   ```

3. **Implementuj `app.py`:**
   ```python
   import streamlit as st
   from utils.api_client import RAEClient
   
   st.set_page_config(
       page_title="RAE Memory Dashboard",
       page_icon="🧠",
       layout="wide"
   )
   
   st.title("🧠 RAE Memory Dashboard")
   st.markdown("Visualize and manage your agent's memory")
   
   # Sidebar configuration
   with st.sidebar:
       st.header("Configuration")
       api_url = st.text_input("API URL", "http://localhost:8000")
       tenant_id = st.text_input("Tenant ID", "default")
       project_id = st.text_input("Project ID", "main")
       
       if st.button("Connect"):
           st.session_state.client = RAEClient(
               api_url=api_url,
               tenant_id=tenant_id,
               project_id=project_id
           )
           st.success("Connected!")
   
   # Main content
   if "client" in st.session_state:
       client = st.session_state.client
       
       # Overview metrics
       col1, col2, col3, col4 = st.columns(4)
       
       stats = client.get_stats()
       
       with col1:
           st.metric("Total Memories", stats.get("total", 0))
       with col2:
           st.metric("Episodic", stats.get("episodic", 0))
       with col3:
           st.metric("Semantic", stats.get("semantic", 0))
       with col4:
           st.metric("LTM", stats.get("ltm", 0))
   else:
       st.info("👈 Configure connection in sidebar")
   ```

4. **Implementuj Timeline Page:**
   ```python
   # pages/1_Timeline.py
   import streamlit as st
   import pandas as pd
   import plotly.express as px
   from datetime import datetime, timedelta
   
   st.title("📅 Memory Timeline")
   
   if "client" not in st.session_state:
       st.error("Not connected to RAE")
       st.stop()
   
   client = st.session_state.client
   
   # Filters
   col1, col2 = st.columns(2)
   with col1:
       layer_filter = st.multiselect(
           "Memory Layer",
           ["episodic", "working", "semantic", "ltm"],
           default=["episodic"]
       )
   with col2:
       days_back = st.slider("Days back", 1, 90, 7)
   
   # Fetch memories
   memories = client.get_memories(
       layers=layer_filter,
       since=datetime.now() - timedelta(days=days_back)
   )
   
   if memories:
       df = pd.DataFrame(memories)
       df['timestamp'] = pd.to_datetime(df['timestamp'])
       
       # Timeline chart
       fig = px.scatter(
           df,
           x='timestamp',
           y='layer',
           color='layer',
           hover_data=['content'],
           title="Memory Timeline"
       )
       st.plotly_chart(fig, use_container_width=True)
       
       # Table view
       st.dataframe(df, use_container_width=True)
   else:
       st.info("No memories found")
   ```

5. **Implementuj Knowledge Graph Visualizer:**
   ```python
   # pages/2_Knowledge_Graph.py
   import streamlit as st
   from pyvis.network import Network
   import streamlit.components.v1 as components
   
   st.title("🕸️ Knowledge Graph")
   
   if "client" not in st.session_state:
       st.error("Not connected to RAE")
       st.stop()
   
   client = st.session_state.client
   
   # Fetch graph data
   with st.spinner("Loading graph..."):
       graph_data = client.get_knowledge_graph()
   
   if graph_data:
       nodes = graph_data.get("nodes", [])
       edges = graph_data.get("edges", [])
       
       # Create PyVis network
       net = Network(
           height="600px",
           width="100%",
           bgcolor="#222222",
           font_color="white"
       )
       
       # Add nodes
       for node in nodes:
           net.add_node(
               node["id"],
               label=node["label"],
               title=node.get("type", "")
           )
       
       # Add edges
       for edge in edges:
           net.add_edge(
               edge["source"],
               edge["target"],
               label=edge.get("relation", "")
           )
       
       # Physics settings
       net.set_options("""
       {
         "physics": {
           "enabled": true,
           "barnesHut": {
             "gravitationalConstant": -8000,
             "springLength": 250,
             "springConstant": 0.001
           }
         }
       }
       """)
       
       # Save and display
       net.save_graph("graph.html")
       with open("graph.html", "r") as f:
           html = f.read()
       components.html(html, height=600)
       
       # Stats
       col1, col2 = st.columns(2)
       with col1:
           st.metric("Nodes", len(nodes))
       with col2:
           st.metric("Edges", len(edges))
   else:
       st.info("No graph data available")
   ```

6. **Implementuj Memory Editor:**
   ```python
   # pages/3_Memory_Editor.py
   import streamlit as st
   
   st.title("✏️ Memory Editor")
   
   if "client" not in st.session_state:
       st.error("Not connected to RAE")
       st.stop()
   
   client = st.session_state.client
   
   # Search for memory to edit
   search_query = st.text_input("Search for memory to edit")
   
   if search_query:
       results = client.search_memories(search_query)
       
       if results:
           memory_id = st.selectbox(
               "Select memory",
               options=[m["id"] for m in results],
               format_func=lambda x: next(
                   m["content"][:100] for m in results if m["id"] == x
               )
           )
           
           selected = next(m for m in results if m["id"] == memory_id)
           
           # Edit form
           with st.form("edit_form"):
               new_content = st.text_area(
                   "Content",
                   value=selected["content"],
                   height=200
               )
               new_tags = st.multiselect(
                   "Tags",
                   options=client.get_all_tags(),
                   default=selected.get("tags", [])
               )
               
               col1, col2 = st.columns(2)
               with col1:
                   if st.form_submit_button("💾 Save Changes"):
                       client.update_memory(
                           memory_id,
                           content=new_content,
                           tags=new_tags
                       )
                       st.success("Memory updated!")
               with col2:
                   if st.form_submit_button("🗑️ Delete", type="secondary"):
                       if st.checkbox("Confirm deletion"):
                           client.delete_memory(memory_id)
                           st.success("Memory deleted!")
                           st.rerun()
       else:
           st.info("No results found")
   ```

7. **Implementuj Query Inspector:**
   ```python
   # pages/4_Query_Inspector.py
   import streamlit as st
   import json
   
   st.title("🔍 Query Inspector")
   
   if "client" not in st.session_state:
       st.error("Not connected to RAE")
       st.stop()
   
   client = st.session_state.client
   
   st.markdown("""
   Test how RAE retrieves and ranks memories for a given query.
   """)
   
   # Query input
   query = st.text_area("Enter your query", height=100)
   
   col1, col2 = st.columns(2)
   with col1:
       top_k = st.slider("Top K results", 1, 20, 5)
   with col2:
       use_rerank = st.checkbox("Use reranking", value=True)
   
   if st.button("🔍 Search", type="primary"):
       with st.spinner("Searching..."):
           results = client.query_memory(
               query=query,
               top_k=top_k,
               use_rerank=use_rerank
           )
       
       if results:
           st.success(f"Found {len(results)} results")
           
           for i, result in enumerate(results, 1):
               with st.expander(
                   f"#{i} - Score: {result['score']:.4f} - {result['layer']}"
               ):
                   st.markdown(f"**Content:**\n{result['content']}")
                   st.markdown(f"**Source:** {result.get('source', 'N/A')}")
                   st.markdown(f"**Tags:** {', '.join(result.get('tags', []))}")
                   
                   # Show raw data
                   if st.checkbox(f"Show raw data #{i}"):
                       st.json(result)
       else:
           st.warning("No results found")
   ```

8. **Requirements:**
   ```
   streamlit
   pandas
   plotly
   pyvis
   httpx
   ```

---

## Plan Wykonania

### Faza 1: Foundation (Tydzień 1-2)
1. ✅ Structured Outputs implementation (Zadanie 2.1)
2. ✅ @rae.trace decorator (Zadanie 2.3)
3. ✅ Test i dokumentacja

### Faza 2: GraphRAG Core (Tydzień 3-4)
1. ✅ Graph extraction (Zadanie 1.1)
2. ✅ Hybrid search (Zadanie 1.2)
3. ✅ Test end-to-end

### Faza 3: MCP Integration (Tydzień 5-6)
1. ✅ MCP tools (Zadanie 3.1)
2. ✅ Context injection (Zadanie 3.2)
3. ✅ Test z IDE (Cursor/Claude Desktop)

### Faza 4: UI Dashboard (Tydzień 7-8)
1. ✅ Streamlit pages (Zadanie 4.1)
2. ✅ Graph visualizer
3. ✅ Memory editor

### Faza 5: Advanced Features (Tydzień 9-10)
1. ✅ Recursive summarization (Zadanie 2.2)
2. ✅ Performance optimization
3. ✅ Dokumentacja użytkownika

---

## Wytyczne Implementacyjne

### Quality Standards:
- **Type hints:** Wszystkie funkcje muszą mieć pełne type hints
- **Docstrings:** Google style docstrings dla każdej funkcji
- **Tests:** Minimum 80% code coverage dla nowych funkcji
- **Error handling:** Proper exception handling z logging
- **Async/await:** Preferuj async gdzie możliwe

### Struktura commitów:
```
feat(graphrag): Add triple extraction from episodic memory
fix(mcp): Handle connection timeout in MCP server
docs(api): Update GraphRAG endpoint documentation
test(hybrid-search): Add integration tests for graph traversal
```

### Przed każdym PR:
1. Uruchom testy: `pytest`
2. Sprawdź typing: `mypy apps/`
3. Format code: `black apps/ && isort apps/`
4. Lint: `ruff check apps/`

---

## Dodatkowe Zasoby

### Przydatne linki:
- MCP Specification: https://spec.modelcontextprotocol.io/
- Pydantic v2: https://docs.pydantic.dev/latest/
- FastAPI async: https://fastapi.tiangolo.com/async/
- Streamlit: https://docs.streamlit.io/

### Przykładowe pytania do mnie:
- "Jak chcesz obsługiwać konflikty w grafie wiedzy?"
- "Jakie metryki chcesz śledzić w dashboardzie?"
- "Czy mam priorytetyzować szybkość czy dokładność w hybrid search?"

---

## Monitoring Postępu

Po zakończeniu każdego zadania:
1. ✅ Stwórz PR z opisem zmian
2. ✅ Zaktualizuj dokumentację API
3. ✅ Dodaj entry do CHANGELOG.md
4. ✅ Oznacz w tym pliku jako "DONE ✅"

**Status Template:**
```markdown
## Zadanie X.Y: [Nazwa] - STATUS: [IN PROGRESS / DONE / BLOCKED]
- Started: YYYY-MM-DD
- Completed: YYYY-MM-DD
- Blockers: None / [opis]
- Notes: [ważne obserwacje]
```

---

## Pytania do Clarification

Przed rozpoczęciem pracy nad każdym kierunkiem, upewnij się że rozumiesz:
1. Priorytety użytkownika (szybkość vs dokładność vs łatwość użycia)
2. Środowisko deployment (local/cloud, hardware constraints)
3. Czy istniejące dane w bazie muszą być zachowane (migration strategy)
4. Czy są jakieś security requirements (auth, encryption)

---

Powodzenia! 🚀
