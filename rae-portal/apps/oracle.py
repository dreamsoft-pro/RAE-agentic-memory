import asyncio
from nicegui import ui
from utils.api_client import RAESuiteClient

class OracleApp:
    def __init__(self, client: RAESuiteClient):
        self.client = client
        self.project = "default" # Standard context for metrics/logs
        self.results_container = None
        self.answer = ""
        self.status = "Idle"

    async def run_query(self, query: str, model: str, project: str):
        if not query: return
        self.status = "Thinking..."
        self.project = project
        self.answer = ""
        ui.notify(f"Oracle is analyzing {project} metrics...")
        self.update_display()
        
        # Call RAE with ANALYTICAL mode
        response = await self.client.execute_agent(
            prompt=query, 
            project=self.project, 
            model=model, 
            mode="analytical"
        )
        self.answer = response.get("answer", "No analysis could be performed.")
        self.status = "Idle"
        self.update_display()

    def update_display(self):
        if not self.results_container: return
        self.results_container.clear()
        with self.results_container:
            if self.status == "Thinking...":
                with ui.column().classes('w-full items-center py-12'):
                    ui.spinner('dots', size='lg', color='blue-9')
                    ui.label('Consulting Neural Manifold...').classes('text-blue-900 font-bold mt-4')
                return

            if self.answer:
                with ui.card().classes('w-full border-l-8 border-blue-900 shadow-md p-6'):
                    with ui.row().classes('items-center gap-2 mb-4'):
                        ui.icon('psychology', color='blue-9', size='md')
                        ui.label('ORACLE INSIGHT').classes('text-xl font-bold text-blue-900')
                    ui.markdown(self.answer).classes("text-sm leading-relaxed")

    def render(self, model_selector, source_selector):
        with ui.column().classes('w-full max-w-5xl mx-auto p-8'):
            ui.label('Order Entry Oracle').classes('text-3xl font-black text-blue-900 mb-2')
            ui.label('Production metrics and industrial intelligence.').classes('text-slate-500 mb-8')
            
            with ui.row().classes('w-full items-center gap-4 mb-12 bg-white p-6 rounded-2xl shadow-sm border'):
                query_input = ui.input(
                    label='Ask about production or assets...', 
                    placeholder='e.g. Compare speed of M01 and M02'
                ).classes('flex-grow text-lg')
                ui.button('QUERY', 
                    on_click=lambda: self.run_query(query_input.value, model_selector.value, source_selector.value)
                ).props('elevated color=blue-9 size=lg rounded')

            self.results_container = ui.column().classes('w-full')
            self.update_display()
