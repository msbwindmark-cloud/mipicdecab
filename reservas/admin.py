from django.contrib import admin
from .models import ReservaPista


@admin.register(ReservaPista)
class ReservaPistaAdmin(admin.ModelAdmin):
    list_display = ['pista', 'fecha', 'hora_inicio', 'hora_fin', 'propietario', 'caballo', 'estado']
    list_filter = ['estado', 'fecha', 'pista']
    search_fields = ['propietario__nombre', 'propietario__apellidos', 'motivo']
    date_hierarchy = 'fecha'
