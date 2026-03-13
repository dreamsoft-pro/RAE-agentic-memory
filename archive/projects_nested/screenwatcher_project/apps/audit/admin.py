from django.contrib import admin
from apps.audit.models import AuditLog
from unfold.admin import ModelAdmin

@admin.register(AuditLog)
class AuditLogAdmin(ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'content_type', 'object_id', 'ip_address')
    list_filter = ('action', 'timestamp', 'content_type')
    search_fields = ('actor__username', 'object_id', 'description', 'ip_address')
    readonly_fields = ('timestamp', 'actor', 'action', 'content_type', 'object_id', 'changes', 'description', 'ip_address', 'target')
    
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
