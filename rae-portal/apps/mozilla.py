import asyncio
import io
import os
try: import trafilatura
except ImportError: trafilatura = None
from nicegui import ui, events
from utils.api_client import RAESuiteClient

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

class MozillaApp:
    def __init__(self, client: RAESuiteClient):
        self.client = client
        self.project = "mozilla_civic"
        self.results_container = None
        self.answer = ""
        self.status = "Idle"
        self.web_url = ""

    async def handle_upload(self, e: events.UploadEventArguments):
        ui.notify(f"Processing Evidence: {e.name}...")
        try:
            content_bytes = e.content.read()
            text = await asyncio.to_thread(self._extract_text, content_bytes, e.name)
            if text:
                success = await self.client.ingest_text(text, project=self.project, source=f"file:{e.name}")
                if success:
                    ui.notify("Knowledge Distributed to Civic Layer", type="positive")
        except Exception as ex:
            ui.notify(f"Upload error: {ex}", type="negative")

    async def handle_web_ingest(self):
        if not self.web_url: return
        ui.notify(f"Scraping Source: {self.web_url}")
        try:
            dl = await asyncio.to_thread(trafilatura.fetch_url, self.web_url)
            text = await asyncio.to_thread(trafilatura.extract, dl) if dl else None
            if text:
                success = await self.client.ingest_text(text, project=self.project, source=f"web:{self.web_url}")
                if success:
                    ui.notify(f"Web Evidence Captured", type="positive")
                    self.web_url = ""
        except Exception as e:
            ui.notify(f"Scraping error: {e}", type="negative")

    def _extract_text(self, b, f):
        ext = os.path.splitext(f)[1].lower()
        if ext == '.pdf' and PdfReader:
            return "\n".join([p.extract_text() for p in PdfReader(io.BytesIO(b)).pages if p.extract_text()])
        return b.decode('utf-8', errors='ignore')

    async def run_audit(self, query: str, model: str):
        if not query: return
        self.status = "Auditing..."
        self.answer = ""
        ui.notify("Verifying against Ground Truth...")
        self.update_display()
        
        response = await self.client.execute_agent(
            prompt=query, 
            project=self.project, 
            model=model, 
            mode="procedural"
        )
        self.answer = response.get("answer", "Audit could not be completed.")
        self.status = "Idle"
        self.update_display()

    def update_display(self):
        if not self.results_container: return
        self.results_container.clear()
        with self.results_container:
            if self.status == "Auditing...":
                with ui.column().classes('w-full items-center py-12'):
                    ui.spinner('gears', size='lg', color='slate-9')
                    ui.label('RAE is cross-referencing evidence...').classes('text-slate-500 mt-4')
                return

            if self.answer:
                with ui.card().classes('w-full border-l-8 border-emerald-500 shadow-md p-6 bg-emerald-50'):
                    with ui.row().classes('items-center gap-2 mb-4'):
                        ui.icon('verified_user', color='emerald-500', size='md')
                        ui.label('CIVIC AUDIT RESULT').classes('text-xl font-bold text-emerald-900')
                    ui.markdown(self.answer).classes("text-sm leading-relaxed")

    def render(self, model_selector):
        with ui.row().classes('w-full gap-8'):
            # Left: Ingestion Controls
            with ui.card().classes('w-80 p-6 bg-slate-50'):
                ui.label('CIVIC INGEST').classes('text-xs font-black text-slate-400 mb-4 tracking-widest')
                
                ui.label('Documents').classes('text-sm font-bold mb-2')
                ui.upload(on_upload=self.handle_upload, label='Upload PDF/TXT', auto_upload=True).classes('w-full mb-6').props('flat bordered')
                
                ui.label('Web Sources').classes('text-sm font-bold mb-2')
                ui.input(label='URL', placeholder='https://...').classes('w-full mb-2').bind_value(self, 'web_url')
                ui.button('Scrape', icon='add_link', on_click=self.handle_web_ingest).props('elevated color=primary').classes('w-full')

            # Right: Audit Query
            with ui.column().classes('flex-grow'):
                ui.label('Mozilla Civic Assistant').classes('text-3xl font-black text-slate-900 mb-2')
                ui.label('Ethical AI and civic program verification.').classes('text-slate-500 mb-8')
                
                with ui.row().classes('w-full items-center gap-4 mb-12 bg-white p-6 rounded-2xl shadow-sm border'):
                    query_input = ui.input(
                        label='Enter audit query...', 
                        placeholder='e.g. Budget check for civic program X'
                    ).classes('flex-grow text-lg')
                    ui.button('AUDIT', 
                        on_click=lambda: self.run_audit(query_input.value, model_selector.value)
                    ).props('elevated color=blue-grey-10 size=lg rounded')

                self.results_container = ui.column().classes('w-full')
                self.update_display()
