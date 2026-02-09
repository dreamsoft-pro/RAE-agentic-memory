"""
RAE-Lite Desktop UI.
Built with NiceGUI for a modern, reactive experience.
"""

import asyncio
import os
import io
from typing import Optional

import httpx
from nicegui import events, ui
try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

# Configuration
API_URL = "http://127.0.0.1:8765"

class RaeLiteUI:
    def __init__(self):
        self.results = []
        self.status = "Idle"
        self.stats = {}
        self.results_container = None

    async def fetch_stats(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_URL}/statistics")
                if response.status_code == 200:
                    self.stats = response.json()
                    ui.notify("Stats updated", type='positive')
        except Exception as e:
            ui.notify(f"Connection failed: {e}", type='negative')

    async def search(self, query: str):
        if not query:
            return

        self.status = "Searching..."
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/memories/query",
                    json={"query": query, "k": 10}
                )
                if response.status_code == 200:
                    data = response.json()
                    self.results = data.get("results", [])
                    ui.notify(f"Found {len(self.results)} memories", type='positive')
                else:
                    ui.notify(f"Error: {response.text}", type='negative')
        except Exception as e:
            ui.notify(f"Search failed: {e}", type='negative')
        finally:
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
            if not self.results:
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
            ui.label('RAE-Lite Desktop').classes('text-xl font-bold')
            ui.button(icon='refresh', on_click=self.fetch_stats).props('flat color=white')

        # Sidebar / Left Panel: Upload
        with ui.left_drawer(value=True).classes('bg-gray-50 border-r'):
            ui.label('Ingest Memories').classes('text-lg font-bold mb-4')
            # Increased max_file_size to 20MB
            ui.upload(on_upload=self.handle_upload, label='Drop files here', auto_upload=True, max_file_size=20_000_000).classes('w-full')
            
            ui.separator().classes('my-4')
            ui.button('Reflect Now', on_click=self.trigger_reflection, icon='lightbulb').props('outline color=primary').classes('w-full')

            ui.separator().classes('my-6')
            ui.label('Statistics').classes('text-md font-bold mb-2')
            with ui.column().classes('gap-1'):
                # Dynamic labels will be updated via binding or manual update
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Total Memories: {s.get('total_count', 0)}")
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Working Layer: {s.get('layer_counts', {}).get('working', 0)}")
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Episodic Layer: {s.get('layer_counts', {}).get('episodic', 0)}")
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Semantic Layer: {s.get('layer_counts', {}).get('semantic', 0)}")
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Reflective Layer: {s.get('layer_counts', {}).get('reflective', 0)}")

        # Main Content: Search
        with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
            with ui.row().classes('w-full items-center gap-4'):
                search_input = ui.input(label='Ask RAE anything...', placeholder='Type your query...').classes('flex-grow')
                ui.button('Search', on_click=lambda: self.search(search_input.value)).props('elevated color=blue-9 rounded')

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
