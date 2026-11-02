from django.contrib import admin
from .models import MovimientoCaja


@admin.register(MovimientoCaja)
class MovimientoCajaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'tipo', 'categoria', 'concepto', 'importe', 'forma_pago']
    list_filter = ['tipo', 'categoria', 'forma_pago', 'fecha']
    search_fields = ['concepto']
    date_hierarchy = 'fecha'
