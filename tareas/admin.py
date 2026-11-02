from django.contrib import admin
from .models import Tarea


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'caballo', 'asignado_a', 'prioridad', 'estado', 'fecha_limite', 'vencida']
    list_filter = ['prioridad', 'estado', 'fecha_limite']
    search_fields = ['titulo', 'descripcion']
    date_hierarchy = 'fecha_creacion'
