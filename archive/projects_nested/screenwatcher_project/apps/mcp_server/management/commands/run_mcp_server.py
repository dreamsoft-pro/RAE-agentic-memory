import asyncio
import sys
from django.core.management.base import BaseCommand
from mcp.server.fastmcp import FastMCP
from asgiref.sync import sync_to_async
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

# Import Models
from apps.registry.models import Machine, Factory, Line
from apps.telemetry.models import TelemetryPoint, MetricDefinition
from apps.oee.models import DailyOEE
from apps.dashboards.models import Dashboard

class Command(BaseCommand):
    help = 'Runs the MCP (Model Context Protocol) Server for ScreenWatcher'

    def add_arguments(self, parser):
        parser.add_argument('--transport', type=str, default='stdio', help='Transport mode: stdio or sse')
        parser.add_argument('--host', type=str, default='0.0.0.0', help='Host for SSE transport')
        parser.add_argument('--port', type=int, default=8001, help='Port for SSE transport')

    def handle(self, *args, **options):
        mcp = FastMCP("ScreenWatcher MCP")

        # --- TOOLS ---

        @mcp.tool()
        async def list_machines() -> list[dict]:
            """Lists all active machines with their codes and names."""
            machines = await sync_to_async(list)(
                Machine.objects.filter(is_active=True).values('code', 'name', 'line__name')
            )
            return machines

        @mcp.tool()
        async def get_machine_details(code: str) -> dict:
            """Get detailed info about a machine."""
            try:
                machine = await Machine.objects.aget(code=code)
                # Helper for relations
                def get_details():
                    return {
                        "code": machine.code,
                        "name": machine.name,
                        "line": machine.line.name,
                        "department": machine.line.department.name,
                        "description": machine.description
                    }
                return await sync_to_async(get_details)()
            except Machine.DoesNotExist:
                return {"error": "Machine not found"}

        @mcp.tool()
        async def get_latest_telemetry(machine_code: str) -> dict:
            """Get the most recent telemetry point for a machine."""
            try:
                # Optimized query
                tp = await TelemetryPoint.objects.filter(machine__code=machine_code).order_by('-timestamp').afirst()
                if tp:
                    return {
                        "timestamp": tp.timestamp.isoformat(),
                        "payload": tp.payload
                    }
                return {"error": "No telemetry data"}
            except Exception as e:
                return {"error": str(e)}

        @mcp.tool()
        async def query_metrics_history(machine_code: str, metric_key: str, hours: int = 1) -> list[dict]:
            """
            Get historical data for a specific metric key (e.g., 'metrics.ink_drops') over the last N hours.
            Useful for analysis.
            """
            start_time = timezone.now() - timedelta(hours=hours)
            
            points = await sync_to_async(list)(
                TelemetryPoint.objects.filter(
                    machine__code=machine_code,
                    timestamp__gte=start_time
                ).order_by('timestamp').values('timestamp', 'payload')[:1000] # Limit
            )
            
            result = []
            keys = metric_key.split('.')
            
            for p in points:
                val = p['payload']
                try:
                    for k in keys:
                        if isinstance(val, dict): val = val.get(k)
                        else: val = None
                    if val is not None:
                        result.append({"time": p['timestamp'].isoformat(), "value": val})
                except:
                    continue
            return result

        @mcp.tool()
        async def list_dashboards() -> list[dict]:
            """Lists available dashboards (public or default)."""
            dashboards = await sync_to_async(list)(
                Dashboard.objects.filter(is_public=True).values('id', 'name')
            )
            return dashboards

        @mcp.tool()
        async def list_metrics() -> list[dict]:
            """Lists all defined metrics definitions."""
            metrics = await sync_to_async(list)(
                MetricDefinition.objects.all().values('name', 'code', 'unit', 'json_key')
            )
            return metrics

        # Run the server
        transport = options['transport']
        if transport == 'sse':
            host = options['host']
            port = options['port']
            self.stdout.write(f"Starting ScreenWatcher MCP Server via SSE on {host}:{port}...")
            
            try:
                import uvicorn
                uvicorn.run(mcp.sse_app, host=host, port=port)
            except ImportError:
                self.stderr.write("Error: 'uvicorn' is required for SSE transport but not installed.")
                self.stderr.write("Please add 'uvicorn' to requirements.txt or install it manually.")
                sys.exit(1)
        else:
            self.stdout.write("Starting ScreenWatcher MCP Server via stdio...")
            mcp.run()
