"""
RAE-Lite Desktop UI.
Built with NiceGUI for a modern, reactive experience.
"""

import asyncio
import os

import httpx
from nicegui import events, ui

# Configuration
API_URL = "http://127.0.0.1:8765"

class RaeLiteUI:
    def __init__(self):
        self.results = []
        self.status = "Idle"
        self.stats = {}

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

    async def handle_upload(self, e: events.UploadEventArguments):
        content = e.content.read().decode('utf-8')
        filename = e.name

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/memories",
                    json={
                        "content": content,
                        "source": f"upload:{filename}",
                        "importance": 0.7,
                        "tags": ["uploaded", os.path.splitext(filename)[1][1:]]
                    }
                )
                if response.status_code == 200:
                    ui.notify(f"Stored: {filename}", type='positive')
                    await self.fetch_stats()
                else:
                    ui.notify(f"Failed to store: {response.text}", type='negative')
        except Exception as ex:
            ui.notify(f"Upload error: {ex}", type='negative')

    def update_results_display(self):
        results_container.clear()
        with results_container:
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

    def render(self):
        # Header
        with ui.header().classes('items-center justify-between bg-blue-900 text-white'):
            ui.label('RAE-Lite Desktop').classes('text-xl font-bold')
            ui.button(icon='refresh', on_click=self.fetch_stats).props('flat color=white')

        # Sidebar / Left Panel: Upload
        with ui.left_drawer(value=True).classes('bg-gray-50 border-r'):
            ui.label('Ingest Memories').classes('text-lg font-bold mb-4')
            ui.upload(on_upload=self.handle_upload, label='Drop files here', auto_upload=True).classes('w-full')

            ui.separator().classes('my-6')
            ui.label('Statistics').classes('text-md font-bold mb-2')
            with ui.column().classes('gap-1'):
                # Dynamic labels will be updated via binding or manual update
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Total Memories: {s.get('total_count', 0)}")
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Working Layer: {s.get('layer_counts', {}).get('working', 0)}")
                ui.label().bind_text_from(self, 'stats', backward=lambda s: f"Semantic Layer: {s.get('layer_counts', {}).get('semantic', 0)}")

        # Main Content: Search
        with ui.column().classes('w-full max-w-4xl mx-auto p-8'):
            with ui.row().classes('w-full items-center gap-4'):
                search_input = ui.input(label='Ask RAE anything...', placeholder='Type your query...').classes('flex-grow')
                ui.button('Search', on_click=lambda: self.search(search_input.value)).props('elevated color=blue-9 rounded')

            ui.separator().classes('my-8')

            global results_container
            results_container = ui.column().classes('w-full')
            self.update_results_display()

        # Initial data fetch
        asyncio.create_task(self.fetch_stats())

def init():
    rae_ui = RaeLiteUI()
    rae_ui.render()

if __name__ in {"__main__", "rae_lite.ui.app"}:
    init()
    ui.run(title="RAE-Lite Desktop", port=8080, reload=False)
