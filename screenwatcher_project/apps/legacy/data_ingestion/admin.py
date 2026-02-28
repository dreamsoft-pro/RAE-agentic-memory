"""
Admin registrations for the data ingestion app.
"""
from __future__ import annotations

from django.contrib import admin
from .models import DataLog


@admin.register(DataLog)
class DataLogAdmin(admin.ModelAdmin):
    list_display = ('roi', 'timestamp', 'value')
    list_filter = ('roi',)
    search_fields = ('roi__name',)