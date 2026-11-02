from django.contrib import admin
from .models import ZonaPicadero


@admin.register(ZonaPicadero)
class ZonaPicaderoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'estado', 'caballo', 'activo']
    list_filter = ['tipo', 'estado', 'activo']
    search_fields = ['nombre']
