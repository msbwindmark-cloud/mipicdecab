from django.contrib import admin
from .models import Consumo


@admin.register(Consumo)
class ConsumoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'fecha', 'lectura_anterior', 'lectura_actual', 'consumo', 'importe', 'coste_por_unidad', 'proveedor']
    list_filter = ['tipo', 'fecha']
    search_fields = ['proveedor', 'notas']
    date_hierarchy = 'fecha'
