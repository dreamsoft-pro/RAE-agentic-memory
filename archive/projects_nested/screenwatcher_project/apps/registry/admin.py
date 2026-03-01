from django.contrib import admin
from .models import Factory, Department, Line, Machine, Interface

@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'factory', 'created_at')
    list_filter = ('factory',)
    search_fields = ('name', 'code')

@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'created_at')
    list_filter = ('department__factory', 'department')
    search_fields = ('name', 'code')

class InterfaceInline(admin.TabularInline):
    model = Interface
    extra = 1

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'line', 'is_active', 'created_at')
    list_filter = ('line__department__factory', 'line__department', 'is_active')
    search_fields = ('name', 'code')
    inlines = [InterfaceInline]

@admin.register(Interface)
class InterfaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'machine', 'protocol', 'is_active')
    list_filter = ('protocol', 'is_active')
    search_fields = ('name', 'machine__code')