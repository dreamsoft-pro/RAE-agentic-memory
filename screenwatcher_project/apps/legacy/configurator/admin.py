"""
Admin registrations for configurator models.

Registers ``TrackedApplication`` and ``RegionOfInterest`` in the Django
administrative interface. The list display is customized for better usability.
"""
from __future__ import annotations

from django.contrib import admin
from .models import TrackedApplication, RegionOfInterest, Department, Line, Machine


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'department__name')


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'line')
    list_filter = ('line__department', 'line')
    search_fields = ('name', 'line__name')


@admin.register(TrackedApplication)
class TrackedApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'screenshot')
    search_fields = ('name',)


@admin.register(RegionOfInterest)
class RegionOfInterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'data_type', 'x1', 'y1', 'x2', 'y2')
    list_filter = ('data_type', 'application')
    search_fields = ('name', 'application__name')