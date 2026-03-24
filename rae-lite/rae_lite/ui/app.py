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

API_URL = "http://rae-api-dev:8000"
TENANT_ID = "66435998-b1d9-5521-9481-55a9fd10e014"

class RaeLiteUI:
    def __init__(self):
        self.stats = {}
        self.results = []
        self.procedural_instruction = ""
        self.status = "Idle"
        self.results_container = None

    async def fetch_stats(self):
        try:
            headers = {"X-Tenant-Id": TENANT_ID}
            proj = self.project_select.value
            response = await client.get(f"{API_URL}/v2/memories/stats?project={proj}", headers=headers)
            if response.status_code == 200:
                self.stats = response.json()
                ui.update()
        except Exception as e:
            print(f"Stats fetch error: {e}")

    async def search(self, query: str):
        if not query: return
        self.status = "Thinking..."
        self.procedural_instruction = ""
        ui.notify(f"Querying RAE: {query}")
        self.update_results_display()
        try:
            async with httpx.AsyncClient() as client:
                payload_v2 = {
                    "prompt": query, 
                    "project": self.project_select.value, 
                    "metadata": {
                        "llm_model": self.model_select.value, 
                        "mode": "procedural"
                    }
                }
                headers = {"X-Tenant-Id": TENANT_ID, "Content-Type": "application/json"}
                response = await client.post(f"{API_URL}/v2/agent/execute", json=payload_v2, headers=headers, timeout=300.0)
                if response.status_code == 200:
                    data = response.json()
                    self.procedural_instruction = data.get("answer", "")
                else: 
                    ui.notify(f"Assistant error: {response.status_code}", type="negative")
                self.status = "Idle"
                self.update_results_display()
        except Exception as e:
            ui.notify(f"Connection error: {e}", type="negative")
            self.status = "Idle"
            self.update_results_display()

    def update_results_display(self):
        if not self.results_container: return
        self.results_container.clear()
        with self.results_container:
            if self.status == "Thinking...":
                with ui.column().classes("w-full items-center py-12"):
                    ui.spinner(size='lg')
                    ui.label("RAE is processing...").classes("text-gray-500 mt-4")
                return
            if self.procedural_instruction:
                with ui.card().classes("w-full mb-8 bg-blue-50 border-blue-200 shadow-md p-6"):
                    ui.markdown(self.procedural_instruction).classes("text-sm leading-relaxed")

    def render(self):
        with ui.header().classes("items-center justify-between bg-blue-900 text-white p-4 shadow-lg"):
            with ui.row().classes("items-center gap-4"):
                ui.label("SmallAI Oracle").classes("text-xl font-bold")
                
                # Models
                models = {
                    "local_qwen_optimized": "Local: QWEN 3.5 9B",
                    "premium_openai": "$ GPT-4o-mini",
                    "premium_anthropic": "$$ Claude 3.5",
                    "local_phi": "Local: Phi-3"
                }
                self.model_select = ui.select(options=models, value="local_qwen_optimized", label="Model").classes("w-64").props('dark dense outlined color=white')
                
                # Data Source (RESTORED)
                sources = {
                    "default": "Standard Knowledge",
                    "grafana_analytics": "Machine Data",
                    "screenwatcher_logs": "System Logs"
                }
                self.project_select = ui.select(options=sources, value="default", label="Source").classes("w-64").props('dark dense outlined color=white')
                
            ui.button(icon='refresh', on_click=self.fetch_stats).props('flat color=white')

        with ui.column().classes("w-full max-w-5xl mx-auto p-12"):
            with ui.row().classes("w-full items-center gap-4 mb-12 bg-white p-4 rounded-xl shadow-sm border"):
                search_input = ui.input(label='Ask Oracle...', placeholder='Type your question...').classes('flex-grow')
                ui.button('QUERY', on_click=lambda: self.search(search_input.value)).props('elevated color=blue-9 size=lg')
            self.results_container = ui.column().classes("w-full")
            self.update_results_display()

@ui.page('/')
def main_page(): RaeLiteUI().render()

if __name__ in {"__main__", "rae_lite.ui.app"}:
    ui.run(title="SmallAI Oracle", port=8080, reload=False)
