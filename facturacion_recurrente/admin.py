from django.contrib import admin
from .models import FacturaRecurrente


@admin.register(FacturaRecurrente)
class RecurrenteAdmin(admin.ModelAdmin):
    list_display = ['propietario', 'concepto', 'importe', 'frecuencia', 'dia_emision', 'fecha_inicio', 'fecha_fin', 'ultima_emision', 'activa', 'proxima_emision']
    list_filter = ['frecuencia', 'activa', 'fecha_inicio']
    search_fields = ['propietario__nombre', 'concepto']
    date_hierarchy = 'fecha_inicio'
