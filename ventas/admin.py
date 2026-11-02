from django.contrib import admin
from .models import VentaCaballo


@admin.register(VentaCaballo)
class VentaCaballoAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'precio_venta', 'precio_minimo', 'fecha_publicacion', 'fecha_venta', 'comprador', 'estado', 'dias_en_venta']
    list_filter = ['estado', 'fecha_publicacion']
    search_fields = ['caballo__nombre', 'comprador__nombre']
    date_hierarchy = 'fecha_publicacion'
