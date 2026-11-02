from django.contrib import admin
from .models import Residencia


@admin.register(Residencia)
class ResidenciaAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'propietario', 'tipo', 'fecha_inicio', 'fecha_fin', 'tarifa_mensual', 'dias_residencia', 'coste_total', 'estado', 'activa']
    list_filter = ['tipo', 'estado', 'fecha_inicio']
    search_fields = ['caballo__nombre', 'propietario__nombre']
    date_hierarchy = 'fecha_inicio'
