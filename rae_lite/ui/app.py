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
        self.debug_trace = {}
        self.status = "Idle"
        self.results_container = None
        
        self.available_models = [
            {"label": "Qwen 2.5 3B (Fast)", "value": "local_qwen"},
            {"label": "Llama 3 8B (Smart)", "value": "local_llama"},
            {"label": "Mistral 7B", "value": "mistral"},
            {"label": "Phi-3 3.8B", "value": "phi3"}
        ]
        self.selected_model = "local_qwen"
        
        self.available_sources = [
            {"label": "📊 Raporty OEE (Szybkie)", "value": "processed_oee"},
            {"label": "👁️ Surowy OCR (Głębokie)", "value": "raw_ocr"},
            {"label": "📚 Dokumentacja PDF", "value": "documentation"}
        ]
        self.selected_source = "processed_oee"
        self.registry_scope = "Cała Firma"

    async def fetch_stats(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/v2/statistics", timeout=5.0)
                if response.status_code == 200:
                    self.stats = response.json()
                    ui.update()
        except Exception as e:
            print(f"Stats error: {e}")

    async def search(self, query: str):
        if not query: return
        self.status = "Thinking..."
        self.procedural_instruction = ""
        self.debug_trace = {}
        self.update_results_display()
        
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                payload = {
                    "query": query, 
                    "project": "default",
                    "model": self.selected_model,
                    "source": self.selected_source
                }
                response = await client.post(f"{API_URL}/procedural/query", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    self.procedural_instruction = data.get("instruction", "No answer.")
                    self.debug_trace = data.get("debug", {})
                else:
                    self.procedural_instruction = f"Błąd API: {response.text}"
                
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
                with ui.column().classes('w-full items-center py-12'):
                    ui.spinner(size='lg', color='blue-9')
                    ui.label('Silicon Oracle is reasoning...').classes('text-gray-500 mt-4')
                return

            if self.procedural_instruction:
                # Main Answer
                with ui.card().classes('w-full mb-4 bg-white border-blue-200 shadow-lg'):
                    with ui.row().classes('w-full items-center gap-2 mb-2 bg-blue-50 p-2 rounded'):
                        ui.icon('analytics', color='primary')
                        ui.label('Analysis Result').classes('font-bold text-blue-900')
                    ui.markdown(self.procedural_instruction).classes('p-4 text-sm leading-relaxed')
                
                # Debug Trace (Reasoning visibility)
                if self.debug_trace:
                    with ui.expansion('🔍 Reasoning Trace (Internal Steps)', icon='visibility').classes('w-full bg-gray-50 border rounded text-xs'):
                        with ui.column().classes('p-4 gap-1'):
                            for k, v in self.debug_trace.items():
                                with ui.row().classes('gap-2'):
                                    ui.label(f"{k.replace('_', ' ').capitalize()}:").classes('font-bold text-gray-600')
                                    ui.label(str(v)).classes('text-gray-800')

            if not self.procedural_instruction:
                ui.label("Waiting for your production query...").classes('text-gray-500 italic text-center w-full py-12')

    def render(self):
        with ui.header().classes('items-center justify-between bg-blue-950 text-white p-4'):
            with ui.row().classes('items-center gap-4'):
                ui.label('Silicon Oracle').classes('text-2xl font-black')
                ui.badge('v3.0 Hybrid, powered by RAE', color='orange-7').classes('text-[10px] font-bold')
            
            with ui.row().classes('items-center gap-6'):
                ui.select(options={s['value']: s['label'] for s in self.available_sources}, value=self.selected_source).bind_value(self, 'selected_source').props('dark dense standout').classes('w-56 text-xs')
                ui.select(options={m['value']: m['label'] for m in self.available_models}, value=self.selected_model).bind_value(self, 'selected_model').props('dark dense standout').classes('w-48 text-xs')
                ui.button(icon='refresh', on_click=self.fetch_stats).props('flat color=white')

        with ui.left_drawer(value=True).classes('bg-gray-50 border-r'):
            ui.label('Struktura Firmy (Registry)').classes('text-lg font-bold mb-4')
            with ui.tree([
                {'id': 'pd', 'label': 'PrintDisplay', 'children': [
                    {'id': 'prod', 'label': 'Wydział Produkcji', 'children': [
                        {'id': 'tj', 'label': 'Gniazdo TrueJet'},
                        {'id': 'ks', 'label': 'Gniazdo Kongsberg'},
                    ]},
                ]},
            ], label_key='label', on_select=lambda e: setattr(self, 'registry_scope', e.value)) as tree:
                tree.expand()
            
            ui.separator().classes('my-6')
            ui.label('Selected Scope:').classes('text-xs font-bold text-gray-400 uppercase')
            ui.label().bind_text_from(self, 'registry_scope').classes('text-sm font-bold text-blue-900')

        with ui.column().classes('w-full max-w-5xl mx-auto p-12'):
            with ui.row().classes('w-full items-center gap-4'):
                search_input = ui.input(label='Ask Oracle...', placeholder='np. Wydajność M01 wczoraj').classes('flex-grow shadow-sm').props('outlined')
                ui.button('ASK ORACLE', on_click=lambda: self.search(search_input.value)).props('elevated color=blue-9 size=lg rounded').classes('px-8')

            ui.separator().classes('my-8 opacity-50')
            self.results_container = ui.column().classes('w-full')
            self.update_results_display()

@ui.page('/')
def main_page():
    rae_ui = RaeLiteUI()
    rae_ui.render()

if __name__ in {"__main__", "rae_lite.ui.app"}:
    ui.run(title="Silicon Oracle 3.0", port=8080, reload=False, dark=False)
