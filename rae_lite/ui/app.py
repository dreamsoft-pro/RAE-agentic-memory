import asyncio
import io
import os
import re
from typing import Any, List, Dict

import httpx
import structlog
from nicegui import events, ui

# Try to import PDF processing library
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

logger = structlog.get_logger(__name__)

# SYSTEM 40.15: Dynamic API and Model Configuration
API_URL = os.getenv("RAE_API_URL", "http://smallai.printdisplay.pl/api")

class RaeLiteUI:
    def __init__(self):
        self.stats = {}
        self.results = []
        self.procedural_instruction = ""
        self.status = "Idle"
        self.results_container = None
        self.assistant_mode = True 
        
        # New: Model selection
        self.available_models = [
            {"label": "Qwen 2.5 3B (Fast)", "value": "local_qwen"},
            {"label": "Llama 3 8B (Smart)", "value": "local_llama"},
            {"label": "Mistral 7B", "value": "mistral"},
            {"label": "Phi-3 3.8B", "value": "phi3"}
        ]
        self.selected_model = "local_qwen"

    async def fetch_stats(self):
        try:
            async with httpx.AsyncClient() as client:
                # Use standard V2 statistics endpoint
                response = await client.get(f"{API_URL}/v2/statistics", timeout=5.0)
                if response.status_code == 200:
                    self.stats = response.json()
                    ui.update()
        except Exception as e:
            print(f"Stats fetch error: {e}")

    async def search(self, query: str):
        if not query:
            return

        self.status = "Thinking..."
        self.procedural_instruction = ""
        ui.notify(f"Using Model: {self.selected_model}")
        self.update_results_display()
        
        try:
            async with httpx.AsyncClient() as client:
                if self.assistant_mode:
                    # SYSTEM 40.12: Procedural Oracle Call with Model Selection
                    response = await client.post(
                        f"{API_URL}/procedural/query",
                        json={
                            "query": query, 
                            "project": "default",
                            "model": self.selected_model
                        },
                        timeout=180.0, 
                    )
                    if response.status_code == 200:
                        data = response.json()
                        self.procedural_instruction = data.get("instruction", "")
                        self.results = data.get("results", [])
                    else:
                        ui.notify(f"Assistant error: {response.text}", type="negative")
                else:
                    response = await client.post(
                        f"{API_URL}/v2/memories/query",
                        json={"query": query, "project": "default", "limit": 10},
                        timeout=30.0,
                    )
                    if response.status_code == 200:
                        self.results = response.json().get("results", [])
                        self.procedural_instruction = ""
                    else:
                        ui.notify(f"Search failed: {response.text}", type="negative")
                
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
                if not PdfReader: return "pypdf not installed"
                file_stream = io.BytesIO(file_bytes)
                reader = PdfReader(file_stream)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted: text += extracted + "\n"
                return text
            else:
                try: text = file_bytes.decode('utf-8-sig')
                except UnicodeDecodeError:
                    try: text = file_bytes.decode('windows-1250')
                    except UnicodeDecodeError: text = file_bytes.decode('utf-8', errors='ignore')
                return text
        except Exception as e:
            return f"Error: {str(e)}"

    async def handle_upload(self, e: events.UploadEventArguments):
        filename = e.name
        ui.notify(f"Uploading: {filename}")
        try:
            content_bytes = await e.content.read()
            content = await asyncio.to_thread(self._extract_text, content_bytes, filename)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/v2/memories",
                    json={
                        "content": content,
                        "source": f"upload:{filename}",
                        "importance": 0.7,
                        "layer": "episodic",
                        "tags": ["uploaded", "doc"]
                    },
                    timeout=180.0
                )
                if response.status_code == 200:
                    ui.notify(f"Stored: {filename}", type='positive')
                    await self.fetch_stats()
                else:
                    ui.notify(f"Failed: {response.text}", type='negative')
        except Exception as ex:
            ui.notify(f"Upload error: {ex}", type='negative')

    def update_results_display(self):
        if not self.results_container: return
        self.results_container.clear()
        with self.results_container:
            if self.status == "Thinking...":
                with ui.column().classes('w-full items-center py-12'):
                    ui.spinner(size='lg')
                    ui.label('RAE is analyzing production data...').classes('text-gray-500 mt-4')
                return

            if self.procedural_instruction:
                with ui.card().classes('w-full mb-8 bg-blue-50 border-blue-200 shadow-md'):
                    with ui.row().classes('w-full items-center gap-2 mb-2'):
                        ui.icon('analytics', color='primary').classes('text-lg')
                        ui.label('Silicon Oracle - Performance Analysis').classes('text-md font-bold text-blue-900')
                    ui.markdown(self.procedural_instruction).classes('text-sm leading-relaxed')
                
            if not self.results and not self.procedural_instruction:
                ui.label("Waiting for your production query...").classes('text-gray-500 italic')
                return

            for r in self.results:
                with ui.card().classes('w-full mb-4 shadow-sm'):
                    with ui.row().classes('w-full items-center justify-between'):
                        ui.label(f"Context Source").classes('text-xs font-bold text-blue-600')
                        ui.label(r.get('layer', 'N/A')).classes('text-xs bg-gray-100 px-2 py-1 rounded')
                    ui.markdown(r.get('content', '')[:1000]).classes('text-sm mt-2')

    def render(self):
        # Header
        with ui.header().classes('items-center justify-between bg-blue-900 text-white p-4'):
            with ui.row().classes('items-center gap-4'):
                ui.label('Silicon Oracle').classes('text-xl font-bold')
                ui.badge('v3.6.1-LTS', color='blue-7').classes('text-[10px]')
            
            with ui.row().classes('items-center gap-4'):
                ui.label('Model:').classes('text-xs font-bold')
                ui.select(
                    options={m['value']: m['label'] for m in self.available_models},
                    value=self.selected_model
                ).bind_value(self, 'selected_model').props('dark dense standout').classes('w-48 text-xs')
                
                ui.button(icon='refresh', on_click=self.fetch_stats).props('flat color=white')

        # Sidebar
        with ui.left_drawer(value=True).classes('bg-gray-50 border-r'):
            ui.label('Industrial Data Ingest').classes('text-lg font-bold mb-4')
            ui.upload(on_upload=self.handle_upload, label='Upload Production Logs', auto_upload=True).classes('w-full')
            
            ui.separator().classes('my-6')
            ui.label('System Health').classes('text-md font-bold mb-2')
            with ui.column().classes('gap-1'):
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Total Memories: {s.get('total_count', 0)}")
                ui.label().bind_text_from(self, 'status', backward=lambda s: f"Status: {s}")

        # Main Content
        with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
            with ui.row().classes('w-full items-center gap-4'):
                search_input = ui.input(label='Ask about efficiency, downtime, machines...', placeholder='e.g. Wydajność M01 wczoraj').classes('flex-grow')
                ui.button('Ask Oracle', on_click=lambda: self.search(search_input.value)).props('elevated color=blue-9 rounded')

            ui.separator().classes('my-8')
            self.results_container = ui.column().classes('w-full')
            self.update_results_display()

        ui.timer(0.1, self.fetch_stats, once=True)

@ui.page('/')
def main_page():
    rae_ui = RaeLiteUI()
    rae_ui.render()

if __name__ in {"__main__", "rae_lite.ui.app"}:
    ui.run(title="Silicon Oracle", port=8080, reload=False)
