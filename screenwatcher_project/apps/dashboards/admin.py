from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from .models import Dashboard, Widget, WidgetDefinition, WidgetSeries
from unfold.admin import ModelAdmin, StackedInline

class WidgetSeriesInline(StackedInline):
    model = WidgetSeries
    extra = 0
    tab = True

@admin.register(Dashboard)
class DashboardAdmin(ModelAdmin):
    list_display = ("name", "user", "is_public", "is_default", "view_link")

    def view_link(self, obj):
        url = reverse("dashboard-detail", kwargs={"dashboard_id": obj.id})
        return format_html('<a href="{}" style="font-weight:bold; color:#3b82f6;">OPEN DASHBOARD</a>', url)
    view_link.short_description = "Action"

    list_filter = ("is_public", "is_default")
    search_fields = ("name", "user__username")

@admin.register(Widget)
class WidgetAdmin(ModelAdmin):
    list_display = ("title", "widget_type", "dashboard")
    list_filter = ("widget_type",)
    inlines = [WidgetSeriesInline]

@admin.register(WidgetDefinition)
class WidgetDefinitionAdmin(ModelAdmin):
    list_display = ("name", "type_code", "is_active")
    list_filter = ("is_active",)
