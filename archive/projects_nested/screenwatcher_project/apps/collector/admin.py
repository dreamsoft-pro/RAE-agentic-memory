from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import DataImport
from .services.ingestion import DataIngestionService

@admin.register(DataImport)
class DataImportAdmin(admin.ModelAdmin):
    list_display = ('machine', 'import_type', 'status_badge', 'created_at', 'processed_at')
    list_filter = ('status', 'import_type', 'machine', 'created_at')
    readonly_fields = ('processed_at', 'log', 'status_badge')
    actions = ['process_selected_files']

    def status_badge(self, obj):
        colors = {
            'pending': 'gray',
            'processing': 'blue',
            'completed': 'green',
            'failed': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == 'pending':
            # Sync processing for MVP (later move to Celery)
            self.message_user(request, f"Started processing {obj.import_file.name}...")
            DataIngestionService.process_import(obj)

    @admin.action(description='Process selected files again')
    def process_selected_files(self, request, queryset):
        for obj in queryset:
            obj.status = 'pending'
            obj.save()
            DataIngestionService.process_import(obj)
        self.message_user(request, f"Queued {queryset.count()} files for processing.")