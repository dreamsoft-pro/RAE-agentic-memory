import asyncio
import io
import os
from nicegui import ui, events
from utils.api_client import RAESuiteClient

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

class ProceduralWizard:
    def __init__(self, client: RAESuiteClient):
        self.client = client
        self.project = "corp_procedures"
        self.results_container = None
        self.instruction = ""
        self.status = "Idle"

    async def handle_upload(self, e: events.UploadEventArguments):
        ui.notify(f"Ingesting Procedure: {e.name}...")
        try:
            content_bytes = e.content.read()
            text = await asyncio.to_thread(self._extract_text, content_bytes, e.name)
            if text:
                success = await self.client.ingest_text(text, project=self.project, source=f"proc:{e.name}")
                if success:
                    ui.notify(f"Document Digested (Project: {self.project})", type="positive")
        except Exception as ex:
            ui.notify(f"Upload error: {ex}", type="negative")

    def _extract_text(self, b, f):
        ext = os.path.splitext(f)[1].lower()
        if ext == '.pdf' and PdfReader:
            return "\n".join([p.extract_text() for p in PdfReader(io.BytesIO(b)).pages if p.extract_text()])
        return b.decode('utf-8', errors='ignore')

    async def generate_steps(self, query: str, model: str):
        if not query: return
        self.status = "Analyzing Procedures..."
        self.instruction = ""
        ui.notify("Wizard is searching 400+ pages of regulations...")
        self.update_display()
        
        response = await self.client.execute_agent(
            prompt=query, 
            project=self.project, 
            model=model, 
            mode="procedural"
        )
        self.instruction = response.get("answer", "No procedure could be formulated.")
        self.status = "Idle"
        self.update_display()

    def update_display(self):
        if not self.results_container: return
        self.results_container.clear()
        with self.results_container:
            if self.status == "Analyzing Procedures...":
                with ui.column().classes('w-full items-center py-12'):
                    ui.spinner('cube', size='lg', color='amber-9')
                    ui.label('Building Step-by-Step Guide...').classes('text-amber-900 font-bold mt-4')
                return

            if self.instruction:
                with ui.card().classes('w-full bg-amber-50 border-amber-200 shadow-lg p-8'):
                    with ui.row().classes('items-center gap-2 mb-4'):
                        ui.icon('assignment', color='amber-9', size='md')
                        ui.label('OFFICIAL PROCEDURE GUIDE').classes('text-xl font-black text-amber-900')
                    ui.markdown(self.instruction).classes('text-md leading-relaxed')

    def render(self, model_selector):
        with ui.row().classes('w-full gap-8'):
            # Left: Procedure Ingestion
            with ui.card().classes('w-80 p-6 bg-amber-50/30'):
                ui.label('KNOWLEDGE SOURCE').classes('text-xs font-black text-amber-700 mb-4 tracking-widest')
                ui.label('Upload 400+ Page Docs').classes('text-sm font-bold mb-2')
                ui.upload(on_upload=self.handle_upload, label='Upload Procedure PDF', auto_upload=True).classes('w-full').props('flat bordered color=amber-9')
                ui.label('RAE will split and index documents for step-by-step retrieval.').classes('text-[10px] text-amber-800 mt-4 italic')

            # Right: Generation Interface
            with ui.column().classes('flex-grow'):
                ui.label('Procedural Wizard').classes('text-3xl font-black text-slate-800 mb-2')
                ui.label('Transform complex documents into actionable steps.').classes('text-slate-500 mb-8')
                
                with ui.row().classes('w-full items-center gap-4 mb-12 bg-white p-6 rounded-2xl shadow-sm border'):
                    query_input = ui.input(
                        label='What do you need to organize?', 
                        placeholder='e.g. Visa process for an employee in Germany'
                    ).classes('flex-grow text-lg')
                    ui.button('GENERATE GUIDE', 
                        on_click=lambda: self.generate_steps(query_input.value, model_selector.value)
                    ).props('elevated color=amber-9 size=lg rounded')

                self.results_container = ui.column().classes('w-full')
                self.update_display()
