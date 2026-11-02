from django.contrib import admin
from .models import Proveedor, PedidoProveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'contacto', 'telefono', 'email', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre', 'contacto', 'telefono']


@admin.register(PedidoProveedor)
class PedidoProveedorAdmin(admin.ModelAdmin):
    list_display = ['proveedor', 'concepto', 'importe', 'fecha_pedido', 'fecha_entrega', 'estado']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['proveedor__nombre', 'concepto']
    date_hierarchy = 'fecha_pedido'
