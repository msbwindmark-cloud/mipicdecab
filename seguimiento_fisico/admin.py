from django.contrib import admin
from .models import RegistroFisico


@admin.register(RegistroFisico)
class RegistroFisicoAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'fecha', 'peso_kg', 'condicion_corporal', 'tono_muscular', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['caballo__nombre', 'observaciones']
    date_hierarchy = 'fecha'
    ordering = ['-fecha']
