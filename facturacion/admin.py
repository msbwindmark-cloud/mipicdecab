from django.contrib import admin
from .models import Factura, ConceptoFactura


class ConceptoFacturaInline(admin.TabularInline):
    model = ConceptoFactura
    extra = 1


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'propietario', 'fecha_emision', 'fecha_vencimiento', 'total', 'estado']
    list_filter = ['estado', 'fecha_emision']
    inlines = [ConceptoFacturaInline]
    search_fields = ['numero_factura', 'propietario__nombre', 'propietario__apellidos', 'propietario__dni_cif']
    date_hierarchy = 'fecha_emision'
