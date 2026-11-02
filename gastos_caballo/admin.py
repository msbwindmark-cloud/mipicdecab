from django.contrib import admin
from .models import GastoCaballo


@admin.register(GastoCaballo)
class GastoCaballoAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'categoria', 'concepto', 'importe', 'fecha', 'proveedor']
    list_filter = ['categoria', 'fecha']
    search_fields = ['caballo__nombre', 'concepto', 'proveedor']
    date_hierarchy = 'fecha'
