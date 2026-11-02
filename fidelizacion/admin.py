from django.contrib import admin
from .models import PuntosFidelizacion, MovimientoPuntos, Recompensa


@admin.register(PuntosFidelizacion)
class PuntosFidelizacionAdmin(admin.ModelAdmin):
    list_display = ['propietario', 'puntos_totales', 'puntos_canjeados', 'puntos_disponibles', 'fecha_actualizacion']
    search_fields = ['propietario__nombre', 'propietario__apellidos']


@admin.register(MovimientoPuntos)
class MovimientoPuntosAdmin(admin.ModelAdmin):
    list_display = ['propietario', 'tipo', 'puntos', 'concepto', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['propietario__nombre', 'concepto']
    date_hierarchy = 'fecha'


@admin.register(Recompensa)
class RecompensaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puntos_necesarios', 'activa']
    list_filter = ['activa']
    search_fields = ['nombre']
