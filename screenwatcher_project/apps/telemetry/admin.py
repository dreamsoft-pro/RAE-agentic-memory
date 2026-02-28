import json
from django.contrib import admin, messages
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from unfold.admin import ModelAdmin
from .models import TelemetryPoint, TelemetryHourlyRollup, MetricDefinition
from apps.registry.models import Machine
from apps.collector.forms import OfflineImportForm

@admin.register(MetricDefinition)
class MetricDefinitionAdmin(ModelAdmin):
    list_display = ('name', 'code', 'unit', 'json_key', 'aggregation')
    search_fields = ('name', 'code')
    list_filter = ('aggregation',)

@admin.register(TelemetryPoint)
class TelemetryPointAdmin(ModelAdmin):
    list_display = ('machine', 'timestamp', 'payload_preview')
    list_filter = ('timestamp', 'machine')
    search_fields = ('machine__code',)
    date_hierarchy = 'timestamp'
    
    # Unfold Global Actions
    actions_list = ["import_offline_button"]

    def import_offline_button(self, request):
        return redirect(reverse("admin:telemetry_telemetrypoint_import_offline"))
    
    import_offline_button.short_description = "Importuj dane Offline"
    import_offline_button.url_name = "telemetry_telemetrypoint_import_offline"

    def payload_preview(self, obj):
        return str(obj.payload)[:50] + "..." if len(str(obj.payload)) > 50 else str(obj.payload)

    # --- Import Logic ---
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import-offline/", self.admin_site.admin_view(self.import_offline), name="telemetry_telemetrypoint_import_offline"),
        ]
        return custom_urls + urls

    def import_offline(self, request):
        if request.method == "POST":
            form = OfflineImportForm(request.POST, request.FILES)
            if form.is_valid():
                jsonl_file = request.FILES["jsonl_file"]
                process_oee = form.cleaned_data["process_oee"]
                success_count, error_count = 0, 0
                
                from apps.oee.services import OEECalculator, DowntimeManager
                
                for line in jsonl_file:
                    try:
                        data = json.loads(line)
                        machine = Machine.objects.get(code=data.get("machine_code"))
                        tp = TelemetryPoint.objects.create(
                            machine=machine,
                            timestamp=data.get("timestamp"),
                            kind="telemetry_packet",
                            payload=data.get("metrics")
                        )
                        if process_oee:
                            OEECalculator.calculate_daily(machine, tp.timestamp.date())
                            status_val = data.get("metrics", {}).get("status")
                            if status_val:
                                DowntimeManager.process_status_change(machine, str(status_val), tp.timestamp)
                        success_count += 1
                    except Exception:
                        error_count += 1
                
                self.message_user(request, f"Zaimportowano {success_count} punktów. Błędy: {error_count}", messages.SUCCESS)
                return HttpResponseRedirect(reverse("admin:telemetry_telemetrypoint_changelist"))
        else:
            form = OfflineImportForm()

        context = {
            **self.admin_site.each_context(request),
            "form": form,
            "title": "Importuj dane Offline",
            "opts": self.model._meta,
        }
        return render(request, "admin/collector/import_offline.html", context)

@admin.register(TelemetryHourlyRollup)
class TelemetryHourlyRollupAdmin(ModelAdmin):
    list_display = ('machine', 'kind', 'timestamp', 'avg_value', 'count_points')
    list_filter = ('kind', 'timestamp', 'machine')