"""
Admin registrations for the data forwarding app.
"""
from __future__ import annotations

from django.contrib import admin

from .models import ExternalSystem, RegionExternalSystem


@admin.register(ExternalSystem)
class ExternalSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'method')
    list_filter = ('method',)
    search_fields = ('name',)


@admin.register(RegionExternalSystem)
class RegionExternalSystemAdmin(admin.ModelAdmin):
    list_display = ('roi', 'external_system')
    list_filter = ('external_system',)
    search_fields = ('roi__name', 'external_system__name')