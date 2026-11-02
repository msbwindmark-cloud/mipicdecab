from django.contrib import admin
from .models import Seguro


@admin.register(Seguro)
class SeguroAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'tipo', 'compania', 'numero_poliza', 'fecha_inicio', 'fecha_vencimiento', 'importe', 'vencido']
    list_filter = ['tipo', 'compania', 'fecha_vencimiento']
    search_fields = ['caballo__nombre', 'numero_poliza', 'compania']
    date_hierarchy = 'fecha_vencimiento'
