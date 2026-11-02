from django.contrib import admin
from .models import Producto, MovimientoInventario


class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'stock_actual', 'stock_minimo', 'unidad', 'stock_bajo_display']
    list_filter = ['tipo']
    search_fields = ['nombre']
    inlines = [MovimientoInventarioInline]
    
    def stock_bajo_display(self, obj):
        if obj.stock_bajo:
            return 'SI'
        return 'NO'
    stock_bajo_display.short_description = 'Stock Bajo'


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo', 'cantidad', 'fecha', 'motivo']
    list_filter = ['tipo', 'fecha']
    search_fields = ['producto__nombre']
