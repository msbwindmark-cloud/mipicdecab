from django.contrib import admin
from .models import Mantenimiento


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ['instalacion_tipo', 'box', 'pista', 'tipo', 'descripcion', 'fecha_reporte', 'fecha_inicio', 'fecha_fin', 'estado', 'coste', 'vencido']
    list_filter = ['instalacion_tipo', 'tipo', 'estado', 'fecha_reporte']
    search_fields = ['descripcion', 'realizado_por']
    date_hierarchy = 'fecha_reporte'
