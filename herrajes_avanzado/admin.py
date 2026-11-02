from django.contrib import admin
from .models import VisitaHerrador, ProgramaHerraje


@admin.register(VisitaHerrador)
class VisitaHerradorAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'herrador', 'tipo', 'fecha_programada', 'fecha_realizada', 'tipo_herradura', 'coste', 'proximo_herraje', 'estado', 'vencida', 'pendiente']
    list_filter = ['tipo', 'estado', 'fecha_programada']
    search_fields = ['caballo__nombre', 'herrador']
    date_hierarchy = 'fecha_programada'


@admin.register(ProgramaHerraje)
class ProgramaHerrajeAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'frecuencia', 'ultima_visita', 'proxima_visita', 'herrador_preferido', 'activo', 'vencido']
    list_filter = ['frecuencia', 'activo']
    search_fields = ['caballo__nombre', 'herrador_preferido']
