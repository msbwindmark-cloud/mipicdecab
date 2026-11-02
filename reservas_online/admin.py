from django.contrib import admin
from .models import ReservaOnline


@admin.register(ReservaOnline)
class ReservaOnlineAdmin(admin.ModelAdmin):
    list_display = ['pista', 'fecha', 'hora_inicio', 'hora_fin', 'propietario', 'caballo', 'tipo', 'estado', 'fecha_solicitud']
    list_filter = ['estado', 'tipo', 'fecha']
    search_fields = ['propietario__nombre', 'pista__nombre']
    date_hierarchy = 'fecha'
