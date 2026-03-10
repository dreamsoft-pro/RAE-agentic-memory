import asyncio
import io
import os
from typing import Any

import httpx
import structlog
from nicegui import events, ui

# Try to import PDF processing library
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

logger = structlog.get_logger(__name__)

API_URL = os.getenv("RAE_API_URL", "http://localhost:8001")


class RaeLiteUI:
    def __init__(self):
        self.stats = {}
        self.results = []
        self.procedural_instruction = ""
        self.status = "Idle"
        self.results_container = None
        self.assistant_mode = True # Default to Assistant Mode for Order Entry

    async def fetch_stats(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/statistics")
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
        ui.notify(f"Processing: {query}")
        self.update_results_display()
        
        try:
            async with httpx.AsyncClient() as client:
                if self.assistant_mode:
                    # SYSTEM 40.12: Procedural Oracle Call
                    response = await client.post(
                        f"{API_URL}/procedural/query",
                        json={"query": query, "project": "default"},
                        timeout=120.0,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        self.procedural_instruction = data.get("instruction", "")
                        self.results = data.get("results", [])
                    else:
                        ui.notify(f"Assistant error: {response.text}", type="negative")
                else:
                    # Standard Search
                    response = await client.post(
                        f"{API_URL}/memories/query",
                        json={"query": query, "project": "default", "k": 10},
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
        """Extract text from file bytes based on extension. Runs in background thread."""
        ext = os.path.splitext(filename)[1].lower()
        print(f"Processing file: {filename} ({ext})")
        
        try:
            if ext == '.pdf':
                if not PdfReader:
                    raise ImportError("pypdf not installed. Cannot process PDF.")
                
                # Wrap bytes in BytesIO for PdfReader
                file_stream = io.BytesIO(file_bytes)
                reader = PdfReader(file_stream)
                text = ""
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                print(f"Extracted {len(text)} chars from PDF")
                return text
            else:
                # Robust decoding for text files (especially Polish Windows-1250 vs UTF-8)
                try:
                    text = file_bytes.decode('utf-8-sig') # Handle UTF-8 with BOM
                except UnicodeDecodeError:
                    try:
                        text = file_bytes.decode('windows-1250') # Polish legacy encoding
                    except UnicodeDecodeError:
                        text = file_bytes.decode('utf-8', errors='ignore')
                
                print(f"Read {len(text)} chars from text file")
                return text
        except Exception as e:
            print(f"Extraction error for {filename}: {e}")
            raise e

    async def handle_upload(self, e: events.UploadEventArguments):
        print(f"DEBUG: Upload event attrs: {dir(e)}")
        
        file_obj = None
        filename = "unknown_file"

        # Try to find file object and filename
        if hasattr(e, 'content'):
            file_obj = e.content
            if hasattr(e, 'name'):
                filename = e.name
            elif hasattr(e.content, 'name'):
                filename = os.path.basename(e.content.name)
        elif hasattr(e, 'file'):
            if hasattr(e.file, 'read'):
                 file_obj = e.file
                 if hasattr(e.file, 'name'):
                     filename = os.path.basename(e.file.name)
            else:
                 file_obj = e.file
                 
        if filename == "unknown_file" and file_obj and hasattr(file_obj, 'name'):
             filename = os.path.basename(file_obj.name)

        print(f"Upload received: {filename}")
        
        if not file_obj:
             print("ERROR: Could not find file object in event arguments")
             ui.notify("Internal error: Could not process upload", type='negative')
             return

        try:
            # Read file content asynchronously in the main loop
            # NiceGUI file objects have async read()
            content_bytes = await file_obj.read()
            
            # Run extraction in a separate thread to avoid blocking the UI loop
            # Pass bytes, not the file object
            content = await asyncio.to_thread(self._extract_text, content_bytes, filename)
            
            if not content or len(content.strip()) == 0:
                msg = f"No text content found in {filename}. If this is a PDF, ensure it is not a scanned image."
                print(msg)
                ui.notify(msg, type='warning')
                return

            print(f"Sending content ({len(content)} chars) to API...")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/memories",
                    json={
                        "content": content,
                        "source": f"upload:{filename}",
                        "importance": 0.7,
                        "tags": ["uploaded", os.path.splitext(filename)[1][1:]]
                    },
                    timeout=180.0  # Increased timeout for large files/embeddings
                )
                print(f"API Response: {response.status_code} - {response.text}")
                
                try:
                    if response.status_code == 200:
                        ui.notify(f"Stored: {filename}", type='positive')
                        await self.fetch_stats()
                    else:
                        ui.notify(f"Failed to store: {response.text}", type='negative')
                except RuntimeError as re:
                    print(f"UI update failed (page closed?): {re}")

        except Exception as ex:
            print(f"Upload exception: {ex}")
            try:
                ui.notify(f"Upload error: {ex}", type='negative')
            except RuntimeError:
                pass # UI might be gone

    def update_results_display(self):
        if not self.results_container:
            return
            
        self.results_container.clear()
        with self.results_container:
            if self.status == "Thinking...":
                with ui.column().classes('w-full items-center py-12'):
                    ui.spinner(size='lg')
                    ui.label('RAE is analyzing procedures...').classes('text-gray-500 mt-4')
                return

            if self.procedural_instruction:
                with ui.card().classes('w-full mb-8 bg-blue-50 border-blue-200 shadow-md'):
                    with ui.row().classes('w-full items-center gap-2 mb-2'):
                        ui.icon('assignment', color='primary').classes('text-lg')
                        ui.label('Order Entry Assistant - Step-by-Step Instruction').classes('text-md font-bold text-blue-900')
                    
                    ui.markdown(self.procedural_instruction).classes('text-sm leading-relaxed')
                    
                    with ui.row().classes('w-full justify-end mt-4'):
                        ui.button('Correct?', icon='thumb_up', on_click=lambda: ui.notify("Reflective feedback saved")).props('flat dense')
                
                ui.label('Based on following fragments:').classes('text-xs text-gray-400 uppercase font-bold mb-2 ml-2')

            if not self.results and not self.procedural_instruction:
                ui.label("No results found or search not performed yet.").classes('text-gray-500 italic')
                return

            for r in self.results:
                with ui.card().classes('w-full mb-4 shadow-sm hover:shadow-md transition-shadow'):
                    with ui.row().classes('w-full items-center justify-between'):
                        ui.label(f"Score: {r['score']:.4f}").classes('text-xs font-bold text-blue-600')
                        ui.label(r['layer']).classes('text-xs bg-gray-100 px-2 py-1 rounded')

                    ui.markdown(r['content']).classes('text-sm mt-2')

                    if r.get('tags'):
                        with ui.row().classes('mt-2 gap-1'):
                            for tag in r['tags']:
                                ui.badge(tag, color='green').classes('text-[10px]')

    async def trigger_reflection(self):
        ui.notify("Starting reflection process...", type='info')
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{API_URL}/reflections", timeout=60.0)
                if response.status_code == 200:
                    data = response.json()
                    count = data.get("count", 0)
                    ui.notify(f"Reflection complete. Created {count} new insights.", type='positive')
                    await self.fetch_stats()
                else:
                    ui.notify(f"Reflection failed: {response.text}", type='negative')
        except Exception as e:
            ui.notify(f"Connection error: {e}", type='negative')

    def render(self):
        # Header
        with ui.header().classes('items-center justify-between bg-blue-900 text-white'):
            with ui.row().classes('items-center gap-4'):
                ui.label('Order Entry Oracle').classes('text-xl font-bold')
                ui.badge('Powered by RAE', color='blue-7').classes('text-[10px]')
            
            with ui.row().classes('items-center gap-2'):
                ui.label('Assistant Mode').classes('text-xs')
                ui.switch(value=True).bind_value(self, 'assistant_mode').props('dark')
                ui.button(icon='refresh', on_click=self.fetch_stats).props('flat color=white')

        # Sidebar / Left Panel: Upload
        with ui.left_drawer(value=True).classes('bg-gray-50 border-r'):
            ui.label('Ingest Procedures').classes('text-lg font-bold mb-4')
            ui.upload(on_upload=self.handle_upload, label='Upload OneNote PDF/TXT', auto_upload=True, max_file_size=20_000_000).classes('w-full')
            
            ui.separator().classes('my-4')
            ui.button('Synthesize Knowledge', on_click=self.trigger_reflection, icon='auto_awesome').props('outline color=primary').classes('w-full')

            ui.separator().classes('my-6')
            ui.label('System Health').classes('text-md font-bold mb-2')
            with ui.column().classes('gap-1'):
                # Dynamic labels will be updated via binding or manual update
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Total Manifold: {s.get('total_count', 0)} nodes")
                ui.label().bind_text_from(self, 'status', backward=lambda s: f"Status: {s}")

        # Main Content: Search
        with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
            with ui.row().classes('w-full items-center gap-4'):
                search_input = ui.input(label='How do I handle situation X in Y...', placeholder='Type your procedural question...').classes('flex-grow')
                ui.button('Ask Oracle', on_click=lambda: self.search(search_input.value)).props('elevated color=blue-9 rounded')

            ui.separator().classes('my-8')

            self.results_container = ui.column().classes('w-full')
            self.update_results_display()

        # Initial data fetch - use timer to ensure loop is running
        ui.timer(0.1, self.fetch_stats, once=True)

@ui.page('/')
def main_page():
    rae_ui = RaeLiteUI()
    rae_ui.render()

if __name__ in {"__main__", "rae_lite.ui.app"}:
    ui.run(title="RAE-Lite Desktop", port=8080, reload=False)