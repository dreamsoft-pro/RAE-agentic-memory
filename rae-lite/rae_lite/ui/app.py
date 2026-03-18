import asyncio
import io
import os
from typing import Any

import httpx
import structlog
from nicegui import events, ui

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

logger = structlog.get_logger(__name__)

API_URL = os.getenv("RAE_API_URL", "http://localhost:8001")
# TENANT ID is critical for data access
TENANT_ID = "66435998-b1d9-5521-9481-55a9fd10e014"

class RaeLiteUI:
    def __init__(self):
        self.stats = {}
        self.results = []
        self.procedural_instruction = ""
        self.status = "Idle"
        self.active_model_name = "QWEN 3.5"
        self.results_container = None
        self.assistant_mode = True

    async def fetch_stats(self):
        try:
            async with httpx.AsyncClient() as client:
                proj = getattr(self, 'project_select', None)
                proj_val = proj.value if proj else "default"
                headers = {"X-Tenant-Id": TENANT_ID}
                response = await client.get(f"{API_URL}/v2/memories/stats?project={proj_val}", headers=headers)
                if response.status_code == 200:
                    self.stats = response.json()
                    ui.update()
        except Exception as e:
            print(f"Stats fetch error: {e}")

    async def search(self, query: str):
        if not query: return
        self.status = "Thinking..."
        self.active_model_name = self.model_select.value.replace("ollama/", "").upper()
        self.procedural_instruction = ""
        ui.notify(f"RAE {self.active_model_name} is processing query...")
        self.update_results_display()
        
        try:
            headers = {"X-Tenant-Id": TENANT_ID, "Content-Type": "application/json"}
            async with httpx.AsyncClient() as client:
                if self.assistant_mode:
                    payload = {
                        "prompt": query, 
                        "project": self.project_select.value, 
                        "metadata": {
                            "llm_model": self.model_select.value,
                            "mode": "procedural"
                        }
                    }
                    response = await client.post(f"{API_URL}/v2/agent/execute", json=payload, headers=headers, timeout=180.0)
                    if response.status_code == 200:
                        data = response.json()
                        self.procedural_instruction = data.get("answer", "")
                        self.results = []
                    else: 
                        ui.notify(f"Assistant error: {response.status_code}", type="negative")
                else:
                    payload = {"query": query, "project": self.project_select.value, "k": 10}
                    response = await client.post(f"{API_URL}/v2/memories/query", json=payload, headers=headers, timeout=60.0)
                    if response.status_code == 200: 
                        self.results = response.json().get("results", [])
                    else: 
                        ui.notify(f"Search failed", type="negative")
                
                self.status = "Idle"
                self.update_results_display()
        except Exception as e:
            ui.notify(f"Connection error: {e}", type="negative")
            self.status = "Idle"
            self.update_results_display()

    def _extract_text(self, file_bytes: bytes, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lower()
        try:
            if ext == '.pdf':
                if not PdfReader: raise ImportError("pypdf not installed")
                file_stream = io.BytesIO(file_bytes)
                reader = PdfReader(file_stream)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted: text += extracted + "\n"
                return text
            else:
                try: text = file_bytes.decode('utf-8-sig')
                except: 
                    try: text = file_bytes.decode('windows-1250')
                    except: text = file_bytes.decode('utf-8', errors='ignore')
                return text
        except Exception as e:
            print(f"Extraction error: {e}")
            raise e

    async def handle_upload(self, e: events.UploadEventArguments):
        file_obj = getattr(e, 'content', getattr(e, 'file', None))
        filename = getattr(e, 'name', "unknown_file")
        if not file_obj: return
        try:
            content_bytes = await file_obj.read()
            content = await asyncio.to_thread(self._extract_text, content_bytes, filename)
            if not content: return
            headers = {"X-Tenant-Id": TENANT_ID}
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{API_URL}/v2/memories/", 
                    json={
                        "content": content, 
                        "source": f"upload:{filename}", 
                        "importance": 0.7, 
                        "project": self.project_select.value,
                        "tags": ["uploaded"]
                    }, 
                    headers=headers,
                    timeout=180.0)
                if response.status_code == 200:
                    ui.notify(f"Stored: {filename}", type="positive")
                    await self.fetch_stats()
        except Exception as ex:
            ui.notify(f"Upload error: {ex}", type="negative")

    def update_results_display(self):
        if not self.results_container: return
        self.results_container.clear()
        with self.results_container:
            if self.status == "Thinking...":
                with ui.column().classes("w-full items-center py-12"):
                    ui.spinner(size='lg', color='blue-9')
                    ui.label(f"{self.active_model_name} is analyzing data...").classes("text-blue-900 font-bold mt-4")
                return
            
            if self.procedural_instruction:
                with ui.card().classes("w-full mb-8 bg-blue-50 border-blue-200 shadow-md p-6"):
                    with ui.row().classes("w-full items-center gap-2 mb-4"):
                        ui.icon('psychology', color='primary', size='md')
                        ui.label('Analysis Result').classes('text-xl font-bold text-blue-900')
                    ui.markdown(self.procedural_instruction).classes("text-md leading-relaxed")
            
            if not self.results and not self.procedural_instruction:
                ui.label("Oracle is ready for your questions.").classes("text-gray-400 italic text-center w-full py-8")
                return

            for r in self.results:
                with ui.card().classes("w-full mb-4 shadow-sm border-l-4 border-blue-300"):
                    ui.markdown(r['content']).classes("text-xs mt-1")

    async def trigger_reflection(self):
        try:
            ui.notify("Deep synthesis in progress...")
            headers = {"X-Tenant-Id": TENANT_ID}
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{API_URL}/v2/memories/reflections", 
                    json={"project": self.project_select.value}, 
                    headers=headers,
                    timeout=120.0)
                if response.status_code == 200:
                    ui.notify("Synthesis complete!", type="positive")
                    await self.fetch_stats()
        except Exception as e:
            ui.notify(f"Connection error: {e}", type="negative")

    def render(self):
        # Header
        with ui.header().classes("items-center justify-between bg-blue-900 text-white p-4 shadow-lg"):
            with ui.row().classes("items-center gap-6"):
                ui.label("RAE Oracle").classes("text-2xl font-black tracking-tight")
                
                # Models including PHI and DEEPSEEK
                models = [
                    "ollama/qwen3.5:9b", 
                    "gpt-4o-mini", 
                    "gpt-4o",
                    "ollama/llama3:8b", 
                    "ollama/phi3",
                    "ollama/mistral",
                    "ollama/qwen2.5:7b",
                    "ollama/deepseek-v2:16b"
                ]
                self.model_select = ui.select(
                    options=models, 
                    value="ollama/qwen3.5:9b", 
                    label="Active Model"
                ).classes("w-64").props('dark dense outlined color=white')
                
                # Sources
                sources = {
                    "default": "Core System",
                    "grafana_analytics": "Machine M01/M02 Data",
                    "screenwatcher_logs": "ScreenWatcher Logs",
                    "billboard-marker": "Billboard Marker",
                    "billboard-splitter": "Billboard Splitter"
                }
                self.project_select = ui.select(
                    options=sources, 
                    value="default", 
                    label="Knowledge Source"
                ).classes("w-64").props('dark dense outlined color=white')

            with ui.row().classes("items-center gap-4"):
                ui.button(icon='refresh', on_click=self.fetch_stats).props('flat color=white')
                ui.switch(value=True).bind_value(self, 'assistant_mode').props('dark')
                ui.label("Oracle Mode").classes("text-xs font-bold")

        with ui.left_drawer(value=True).classes("bg-slate-50 border-r p-4"):
            ui.label("Data Ingestion").classes("text-lg font-bold mb-4")
            ui.upload(on_upload=self.handle_upload, auto_upload=True).classes("w-full")
            ui.button("Synthesize", on_click=self.trigger_reflection, icon='bolt').props('elevated color=amber-9').classes("w-full mt-6")
            
            ui.separator().classes("my-8")
            ui.label("Status").classes("text-xs font-bold text-slate-400 uppercase")
            ui.label().bind_text_from(self, 'status', backward=lambda s: f"Current: {s}").classes("text-xs")

        with ui.column().classes("w-full max-w-5xl mx-auto p-12"):
            with ui.row().classes("w-full items-center gap-4 mb-12 bg-white p-6 rounded-2xl shadow-sm border"):
                search_input = ui.input(label='Query machine performance or procedures...', placeholder='Ask M01 performance on Feb 24?').classes('flex-grow')
                ui.button('ANALYSIS', on_click=lambda: self.search(search_input.value)).props('elevated color=blue-9 size=lg rounded')
            
            self.results_container = ui.column().classes("w-full")
            self.update_results_display()
            
        ui.timer(0.1, self.fetch_stats, once=True)

@ui.page('/')
def main_page():
    RaeLiteUI().render()

if __name__ in {"__main__", "rae_lite.ui.app"}:
    ui.run(title="RAE Oracle Industrial", port=8080, reload=False, dark=False)
