from django.contrib import admin
from .models import Transporte


@admin.register(Transporte)
class TransporteAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'tipo', 'fecha_salida', 'origen', 'destino', 'transportista', 'coste', 'estado']
    list_filter = ['tipo', 'estado', 'fecha_salida']
    search_fields = ['caballo__nombre', 'origen', 'destino', 'transportista']
    date_hierarchy = 'fecha_salida'
