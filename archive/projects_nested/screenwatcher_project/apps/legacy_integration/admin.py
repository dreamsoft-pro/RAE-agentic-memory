from django.contrib import admin
from .models import ConnectionProfile, Jobsdata, Printtemp

@admin.register(ConnectionProfile)
class ConnectionProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'host', 'database', 'user', 'use_central_config')
    list_filter = ('use_central_config',)
    search_fields = ('name', 'host', 'database')

@admin.register(Jobsdata)
class JobsdataAdmin(admin.ModelAdmin):
    list_display = ('jdnr', 'customer', 'linedesc', 'jobformat')
    search_fields = ('jdnr', 'customer')
    readonly_fields = [f.name for f in Jobsdata._meta.fields]

@admin.register(Printtemp)
class PrinttempAdmin(admin.ModelAdmin):
    list_display = ('id', 'jdnr', 'tiles', 'tilecounter', 'isprinted', 'dtime')
    list_filter = ('isprinted', 'machine')
    search_fields = ('jdnr', 'tiles')
    readonly_fields = [f.name for f in Printtemp._meta.fields]
