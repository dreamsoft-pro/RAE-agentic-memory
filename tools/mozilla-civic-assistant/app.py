import asyncio
import io
import os
from typing import List, Dict, Any

import trafilatura
from nicegui import events, ui
from utils.api_client import CivicRAEClient

# --- Configuration ---
API_URL = os.getenv("RAE_API_URL", "http://localhost:8001")
API_KEY = os.getenv("RAE_API_KEY", "test-key")

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

class MozillaCivicApp:
    def __init__(self):
        self.client = CivicRAEClient(API_URL, API_KEY)
        self.stats = {"total": 0, "sensory": 0, "episodic": 0, "working": 0, "semantic": 0, "reflective": 0}
        self.results = []
        self.current_instruction = ""
        self.audit_status = None
        self.status = "Disconnected"
        self.is_connected = False
        self.results_container = None
        self.web_url = ""

    async def connect(self):
        self.is_connected = await self.client.check_connection()
        if self.is_connected:
            self.status = "Active"
            await self.refresh_stats()
            ui.notify("RAE Civic Node Online", type="positive")
        else:
            self.status = "Connection Failed"

    async def refresh_stats(self):
        if not self.is_connected: return
        self.stats = await self.client.get_stats()
        # Fallback if API stats are not ready
        if self.stats.get("total", 0) == 0:
            res = await self.client.civic_query("*")
            mems = res.get("results", [])
            if mems:
                self.stats["total"] = len(mems)
                self.stats["semantic"] = len(mems)
        ui.update()

    async def handle_upload(self, e: events.UploadEventArguments):
        ui.notify(f"Auditing File: {e.name}...")
        try:
            content_bytes = e.content.read() if hasattr(e.content, 'read') else e.content
            text = await asyncio.to_thread(self._extract_text, content_bytes, e.name)
            if text:
                if await self.client.ingest_v5(text, source=f"file:{e.name}"):
                    ui.notify("Distributed to RAE Layers", type="positive")
                    await asyncio.sleep(2)
                    await self.refresh_stats()
        except Exception as ex:
            ui.notify(f"Upload error: {ex}", type="negative")

    def _extract_text(self, b, f):
        ext = os.path.splitext(f)[1].lower()
        if ext == '.pdf' and PdfReader:
            return "\n".join([p.extract_text() for p in PdfReader(io.BytesIO(b)).pages if p.extract_text()])
        return b.decode('utf-8', errors='ignore')

    async def handle_web_ingest(self):
        if not self.web_url: return
        ui.notify(f"Scraping Official Source...")
        try:
            dl = await asyncio.to_thread(trafilatura.fetch_url, self.web_url)
            text = await asyncio.to_thread(trafilatura.extract, dl) if dl else None
            if text and await self.client.ingest_v5(text, source=f"web:{self.web_url}"):
                ui.notify(f"Web Evidence Captured", type="positive")
                self.web_url = ""
                await asyncio.sleep(2)
                await self.refresh_stats()
        except Exception as e:
            ui.notify(f"Error: {e}", type="negative")

    async def run_forced_reflection(self):
        self.status = "Reflecting..."
        ui.update()
        res = await self.client.trigger_3layer_reflection()
        ui.notify("Reflection Cycle Complete", type="positive")
        self.status = "Active"
        await self.refresh_stats()

    async def ask_oracle(self, query: str):
        if not query: return
        self.status = "Auditing..."
        self.current_instruction = ""
        self.results = []
        self.audit_status = None
        self.update_results()
        
        response = await self.client.civic_query(query)
        self.current_instruction = response.get("instruction", "")
        self.results = response.get("results", [])
        self.audit_status = response.get("audit", {})
        
        # Detection of "No Data" or "Insufficient" states
        text_lower = self.current_instruction.lower()
        if not self.results or "error" in text_lower or "no information" in text_lower or "not found" in text_lower:
            if not self.audit_status: self.audit_status = {}
            self.audit_status["status"] = "insufficient"
            self.audit_status["reason"] = "Query exceeds current knowledge base bounds."

        self.status = "Active"
        self.update_results()

    def update_results(self):
        if not self.results_container: return
        self.results_container.clear()
        with self.results_container:
            if self.status == "Auditing...":
                with ui.column().classes('w-full items-center py-12'):
                    ui.spinner('gears', size='lg', color='primary')
                    ui.label('RAE is cross-referencing evidence...').classes('text-slate-500 mt-4 animate-pulse')
                return

            if self.current_instruction:
                # Spectacular Audit Header
                status = self.audit_status.get('status', 'grounded')
                bg_color = 'bg-emerald-50 border-emerald-500'
                icon = 'verified_user'
                label = 'VERIFIED BY AUDITOR'
                
                if status == 'insufficient':
                    bg_color = 'bg-amber-50 border-amber-500'
                    icon = 'warning'
                    label = 'INSUFFICIENT EVIDENCE'
                elif status == 'blocked':
                    bg_color = 'bg-red-50 border-red-500'
                    icon = 'block'
                    label = 'AUDIT FAILED / NO DATA'

                with ui.card().classes(f'w-full mb-8 {bg_color} border-l-8 shadow-xl p-0 overflow-hidden'):
                    with ui.row().classes('w-full items-center justify-between p-4 bg-white/50 border-b'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon(icon, color='primary' if status=='grounded' else 'warning').classes('text-2xl')
                            ui.label(label).classes('font-black text-slate-800 letter-spacing-1')
                        ui.badge('DEEPSEEK R1 AUDIT', color='slate-8').props('outline')

                    with ui.column().classes('p-6'):
                        ui.markdown(self.current_instruction).classes('text-lg leading-relaxed text-slate-800')
                        
                        if self.audit_status.get('reason'):
                            with ui.row().classes('mt-6 p-3 bg-white/80 rounded border border-dashed items-start gap-2'):
                                ui.icon('psychology', size='xs', color='slate-500')
                                ui.label(f"Auditor Rationale: {self.audit_status['reason']}").classes('text-xs italic text-slate-600')

                ui.label('Supporting Evidence (Semantic Grounding):').classes('text-xs text-slate-400 uppercase font-black mb-4 ml-2 tracking-widest')

            for r in self.results:
                with ui.card().classes('w-full mb-4 hover:shadow-md transition-all border-slate-100'):
                    with ui.row().classes('w-full items-center justify-between'):
                        score = r.get('score', 0.0)
                        ui.badge(f"Confidence: {score*100:.1f}%", color='blue-9')
                        meta = r.get('metadata', {})
                        ui.label(meta.get('provenance_source') or meta.get('source') or 'Public Record').classes('text-xs font-mono text-blue-600')
                    ui.markdown(r.get('content', '')[:500] + ('...' if len(r.get('content',''))>500 else '')).classes('text-sm mt-2 text-slate-600 italic border-l-2 pl-4')

    def render(self):
        ui.colors(primary='#0f172a', secondary='#64748b', accent='#f59e0b')
        ui.query('body').style('background-color: #f8fafc;')

        with ui.header().classes('items-center justify-between bg-slate-900 text-white p-6 shadow-2xl'):
            with ui.row().classes('items-center gap-4'):
                ui.icon('shield', size='lg', color='blue-400')
                with ui.column().classes('gap-0'):
                    ui.label('Mozilla Civic Assistant').classes('text-2xl font-black tracking-tight')
                    ui.label('RAE Reflective Audit Node v4.2').classes('text-xs text-blue-400 font-mono')
            
            with ui.row().classes('items-center gap-6'):
                with ui.row().classes('items-center gap-2 bg-slate-800 px-4 py-2 rounded-full border border-slate-700'):
                    ui.badge('', color='emerald').props('dot')
                    ui.label().bind_text_from(self, 'status', backward=lambda s: f"Node: {s}")
                ui.button(icon='refresh', on_click=self.connect).props('flat round color=white')

        with ui.left_drawer(value=True).classes('bg-white border-r p-8 shadow-inner'):
            ui.label('SYSTEM INGEST').classes('text-xs font-black text-slate-400 mb-6 tracking-widest')
            
            ui.label('1. Official Documents').classes('text-sm font-bold mb-2')
            ui.upload(on_upload=self.handle_upload, label='Upload Evidence', auto_upload=True).classes('w-full mb-8').props('flat bordered')
            
            ui.label('2. Web Intelligence').classes('text-sm font-bold mb-2')
            with ui.row().classes('w-full items-center gap-2 mb-8'):
                ui.input(label='Source URL', placeholder='https://mozillafoundation.org/...').classes('flex-grow').bind_value(self, 'web_url')
                ui.button(icon='add_link', on_click=self.handle_web_ingest).props('elevated round color=primary')
            
            ui.separator().classes('my-8')
            
            ui.label('MEMORY MANIFOLD').classes('text-xs font-black text-slate-400 mb-4 tracking-widest')
            with ui.column().classes('gap-3 p-4 bg-slate-50 rounded-xl border'):
                for key, icon in [('sensory', 'visibility'), ('episodic', 'history'), ('semantic', 'account_tree'), ('reflective', 'auto_awesome')]:
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon(icon, size='xs', color='slate-400')
                            ui.label(key.title()).classes('text-xs text-slate-600')
                        ui.label().bind_text_from(self, 'stats', backward=lambda s, k=key: str(s.get(k, 0))).classes('font-mono font-bold text-blue-600')
            
            ui.button('SYNTHESIZE KNOWLEDGE', on_click=self.run_forced_reflection, icon='bolt').props('elevated color=accent').classes('w-full mt-8 py-4 font-black')

        with ui.column().classes('w-full max-w-6xl mx-auto p-12'):
            with ui.row().classes('w-full items-center gap-6 bg-white p-4 rounded-2xl shadow-sm border'):
                query_input = ui.input(label='Perform Civic Audit Query...', placeholder='Ask about specific programs, budgets or ethics...').classes('flex-grow text-lg').props('borderless')
                ui.button('AUDIT', on_click=lambda: self.ask_oracle(query_input.value)).props('elevated color=primary rounded-xl px-8 py-3').classes('font-bold shadow-lg shadow-blue-200')

            self.results_container = ui.column().classes('w-full mt-12')
            self.update_results()

        ui.timer(0.1, self.connect, once=True)

@ui.page('/')
def main_page():
    app = MozillaCivicApp()
    app.render()

if __name__ in {"__main__", "app"}:
    ui.run(title="Mozilla Civic Assistant", port=8502, reload=False, dark=False)
