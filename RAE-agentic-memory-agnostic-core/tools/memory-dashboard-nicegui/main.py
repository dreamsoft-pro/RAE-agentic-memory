import os
from datetime import datetime
from typing import List

from nicegui import ui
from utils.api_client import RAEClient

# --- Configuration ---
DEFAULT_API_URL = os.getenv("RAE_API_URL", "http://localhost:8001")
DEFAULT_API_KEY = os.getenv("RAE_API_KEY", "default-key")
DEFAULT_TENANT = os.getenv("RAE_TENANT_ID", "default")
DEFAULT_PROJECT = os.getenv("RAE_PROJECT_ID", "default")


# --- State ---
class AppState:
    def __init__(self):
        self.client = RAEClient(
            DEFAULT_API_URL, DEFAULT_API_KEY, DEFAULT_TENANT, DEFAULT_PROJECT
        )
        self.stats = {"total": 0, "episodic": 0, "working": 0, "semantic": 0, "ltm": 0}
        self.recent_memories = []
        self.is_connected = False
        self.tenants = []
        self.projects = []
        self.current_tenant = DEFAULT_TENANT
        self.current_project = DEFAULT_PROJECT


state = AppState()


# --- ISO Audit Dialog ---
class AuditDialog(ui.dialog):
    def __init__(
        self, memory_id: str, current_content: str, current_tags: List[str], on_confirm
    ):
        super().__init__()
        self.memory_id = memory_id
        self.on_confirm = on_confirm

        with self, ui.card().classes("w-full max-w-2xl"):
            ui.label("🛡️ ISO 27001 Compliance Edit").classes(
                "text-xl font-bold text-primary"
            )
            ui.label("All changes are audited. Please provide a valid reason.").classes(
                "text-sm text-gray-500 mb-4"
            )

            with ui.row().classes("w-full gap-4 mb-4 bg-gray-50 p-2 rounded"):
                ui.input("Memory ID", value=memory_id).props("readonly").classes(
                    "w-1/3"
                )
                ui.input("Timestamp", value=datetime.now().isoformat()).props(
                    "readonly"
                ).classes("w-1/3")

            self.content_input = (
                ui.textarea("Content", value=current_content)
                .classes("w-full")
                .props("outlined")
            )
            self.tags_input = (
                ui.input("Tags (comma separated)", value=",".join(current_tags))
                .classes("w-full")
                .props("outlined")
            )

            ui.separator().classes("my-4")

            ui.label("Audit Log (Mandatory)").classes("font-bold")
            self.reason_input = ui.select(
                [
                    "Data Correction",
                    "PII Removal",
                    "Context Clarification",
                    "Erroneous Entry",
                ],
                label="Reason Code",
            ).classes("w-full")
            self.justification_input = (
                ui.input("Detailed Justification")
                .classes("w-full")
                .props("outlined required")
            )

            with ui.row().classes("w-full justify-end mt-4"):
                ui.button("Cancel", on_click=self.close).props("flat color=grey")
                ui.button("AUDIT & SAVE", on_click=self.save).props(
                    "color=red icon=security"
                )

    async def save(self):
        if not self.reason_input.value or not self.justification_input.value:
            ui.notify(
                "Reason and Justification are MANDATORY for ISO compliance.",
                type="negative",
            )
            return

        full_reason = f"[{self.reason_input.value}] {self.justification_input.value}"
        new_tags = [t.strip() for t in self.tags_input.value.split(",") if t.strip()]

        await self.on_confirm(
            self.memory_id, self.content_input.value, new_tags, full_reason
        )
        self.close()


# --- Background Tasks (Moved inside page for UI access) ---


# --- UI Layout ---
@ui.page("/")
async def main_page():
    ui.colors(
        primary="#5898d4", secondary="#26a69a", accent="#9c27b0", positive="#21ba45"
    )

    # State specific to this client connection
    # We can use 'state' global for data cache, but UI updates need local scope

    # Header
    with ui.header().classes("items-center justify-between bg-slate-800 text-white"):
        ui.label("🧠 RAE Ops Center").classes("text-xl font-bold")
        with ui.row().classes("items-center gap-4"):
            # Context Display in Header
            header_tenant_label = ui.label(f"Tenant: {state.current_tenant}")
            header_project_label = ui.label(f"Project: {state.current_project}")
            connection_status = ui.icon("circle").classes("text-red-500")

    # Sidebar
    with ui.left_drawer(value=True).classes("bg-slate-50"):
        ui.label("Context Selector").classes("font-bold text-gray-600 mb-2")

        # Tenant/Project Selectors
        # Allow custom value (new=True) or start with None to avoid "Invalid value" error
        tenant_select = ui.select(
            options=[state.current_tenant], label="Tenant", value=state.current_tenant
        ).classes("w-full")
        # Removed bind_options due to AttributeError

        project_select = ui.select(
            options=[state.current_project],
            label="Project",
            value=state.current_project,
        ).classes("w-full")
        # Removed bind_options due to AttributeError

        async def on_context_change():
            state.current_tenant = tenant_select.value
            state.current_project = project_select.value

            # Update header
            header_tenant_label.text = f"Tenant: {state.current_tenant}"
            header_project_label.text = f"Project: {state.current_project}"

            await state.client.update_context(tenant_select.value, project_select.value)
            await local_refresh()  # Immediate refresh
            ui.notify(f"Switched to {state.current_tenant} / {state.current_project}")

        ui.button("Apply Context", on_click=on_context_change).classes("w-full mt-2")

        ui.separator().classes("my-4")
        ui.label("Connection").classes("font-bold text-gray-600 mb-2")
        api_url_input = ui.input("API URL", value=state.client.api_url).classes(
            "w-full"
        )

        async def reconnect():
            state.client.api_url = api_url_input.value
            if await state.client.check_connection():
                ui.notify("Connected", type="positive")
                state.is_connected = True
                connection_status.classes(remove="text-red-500", add="text-green-500")
                await local_refresh(full_reload=True)  # Force fetch metadata
            else:
                ui.notify("Connection Failed", type="negative")
                state.is_connected = False
                connection_status.classes(remove="text-green-500", add="text-red-500")

        ui.button("Reconnect", on_click=reconnect).classes("w-full mt-2")

    # Main Content
    with ui.column().classes("w-full p-4 gap-4"):

        # TABS Navigation
        with ui.tabs().classes("w-full") as tabs:
            tab_overview = ui.tab("Overview")
            tab_timeline = ui.tab("Timeline")
            tab_graph = ui.tab("Graph")
            tab_query = ui.tab("Query Lab")

        with ui.tab_panels(tabs, value=tab_overview).classes("w-full"):

            # --- OVERVIEW TAB ---
            with ui.tab_panel(tab_overview):
                # Stats Row
                with ui.row().classes("w-full gap-4"):
                    # Using labels that we will update manually in refresh loop
                    with ui.card().classes("w-1/6 bg-blue-50"):
                        ui.label("Total").classes("text-gray-600 font-bold")
                        lbl_total = ui.label("0").classes("text-3xl font-bold mt-2")

                    with ui.card().classes("w-1/6 bg-green-50"):
                        ui.label("Episodic").classes("text-gray-600 font-bold")
                        lbl_episodic = ui.label("0").classes("text-3xl font-bold mt-2")

                    with ui.card().classes("w-1/6 bg-orange-50"):
                        ui.label("Working").classes("text-gray-600 font-bold")
                        lbl_working = ui.label("0").classes("text-3xl font-bold mt-2")

                    with ui.card().classes("w-1/6 bg-purple-50"):
                        ui.label("Semantic").classes("text-gray-600 font-bold")
                        lbl_semantic = ui.label("0").classes("text-3xl font-bold mt-2")

                    with ui.card().classes("w-1/6 bg-slate-50"):
                        ui.label("LTM").classes("text-gray-600 font-bold")
                        lbl_ltm = ui.label("0").classes("text-3xl font-bold mt-2")

                # Workspace
                with ui.row().classes("w-full gap-4 h-full mt-4"):
                    # Live Feed
                    with ui.card().classes("w-1/3 h-full"):
                        ui.label("🔴 Live Feed").classes("font-bold text-lg mb-2")
                        feed_container = ui.column().classes("w-full gap-2")

                    # Search/Edit
                    with ui.card().classes("w-2/3 h-full"):
                        ui.label("🔍 Search & ISO Edit").classes(
                            "font-bold text-lg mb-2"
                        )
                        with ui.row().classes("w-full gap-2"):
                            search_input = ui.input("Search...").classes("flex-grow")

                            async def perform_search():
                                if not search_input.value:
                                    return
                                # Use v2 search with filters
                                results = await state.client.get_recent_memories(
                                    limit=20
                                )  # TODO: Use real search with query
                                search_results_container.clear()
                                with search_results_container:
                                    for res in results:
                                        with ui.row().classes(
                                            "w-full items-center justify-between p-2 hover:bg-gray-100 border-b"
                                        ):
                                            ui.label(
                                                res.get("content", "")[:60]
                                            ).classes("flex-grow")
                                            with ui.row():
                                                ui.chip(res.get("layer", "N/A")).props(
                                                    "dense"
                                                )
                                                ui.button(
                                                    icon="edit",
                                                    on_click=lambda r=res: open_audit_dialog(
                                                        r
                                                    ),
                                                ).props("flat dense round")

                            ui.button("Search", icon="search", on_click=perform_search)

                        search_results_container = ui.column().classes(
                            "w-full mt-4 h-96 overflow-y-auto"
                        )

            # --- TIMELINE TAB ---
            with ui.tab_panel(tab_timeline):
                ui.label("Coming Soon: Timeline Visualization").classes(
                    "text-2xl text-gray-400"
                )

            # --- GRAPH TAB ---
            with ui.tab_panel(tab_graph):
                ui.label("Coming Soon: 3D Knowledge Graph").classes(
                    "text-2xl text-gray-400"
                )

            # --- QUERY LAB TAB ---
            with ui.tab_panel(tab_query):
                ui.label("Query Laboratory (Szubar Mode Analysis)").classes(
                    "text-xl font-bold"
                )
                # Placeholder for /search/hybrid experimenter

    # --- Local Refresh Logic ---
    async def local_refresh(full_reload=False):
        if not state.is_connected:
            state.is_connected = await state.client.check_connection()
            full_reload = True

        if state.is_connected:
            if full_reload or not state.tenants:
                raw_tenants = await state.client.get_tenants()
                state.tenants = (
                    [t["id"] for t in raw_tenants] if raw_tenants else ["default"]
                )
                state.projects = await state.client.get_projects()

                # Update Selectors
                tenant_select.options = state.tenants
                tenant_select.update()
                project_select.options = state.projects
                project_select.update()

            # Update Stats
            new_stats = await state.client.get_stats()
            state.stats = new_stats
            lbl_total.text = str(new_stats.get("total", 0))
            lbl_episodic.text = str(new_stats.get("episodic", 0))
            lbl_working.text = str(new_stats.get("working", 0))
            lbl_semantic.text = str(new_stats.get("semantic", 0))
            lbl_ltm.text = str(new_stats.get("ltm", 0))

            # Update Recent Feed
            new_memories = await state.client.get_recent_memories(limit=10)
            state.recent_memories = new_memories

            feed_container.clear()
            with feed_container:
                for mem in state.recent_memories:
                    with ui.card().classes("w-full p-2 bg-gray-50 text-xs"):
                        ui.label(mem.get("content", "")[:80] + "...").classes(
                            "font-bold"
                        )
                        with ui.row().classes("text-gray-400 justify-between w-full"):
                            ui.label(mem.get("layer", "unknown"))
                            ui.label(mem.get("created_at", "")[:19])

    # --- Actions ---
    async def handle_iso_update(mid, content, tags, reason):
        success = await state.client.update_memory(
            mid, content, tags, reason, "dashboard-operator"
        )
        if success:
            ui.notify(f"Memory {mid} updated.", type="positive")
            await local_refresh()
        else:
            ui.notify("Update failed.", type="negative")

    def open_audit_dialog(memory):
        AuditDialog(
            memory_id=memory.get("id", "unknown"),
            current_content=memory.get("content", ""),
            current_tags=memory.get("tags", []),
            on_confirm=handle_iso_update,
        )

    # Background Loop
    ui.timer(3.0, local_refresh)


ui.run(title="RAE Ops Center", port=8501, show=False, reload=True)
