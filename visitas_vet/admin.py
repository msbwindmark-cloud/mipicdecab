from django.contrib import admin
from .models import VisitaVeterinaria


@admin.register(VisitaVeterinaria)
class VisitaVeterinariaAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'veterinario', 'tipo', 'fecha_programada', 'fecha_realizada', 'estado', 'coste', 'pendiente', 'vencida']
    list_filter = ['tipo', 'estado', 'fecha_programada']
    search_fields = ['caballo__nombre', 'veterinario', 'motivo']
    date_hierarchy = 'fecha_programada'
