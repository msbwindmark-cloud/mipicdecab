from django.contrib import admin
from .models import Propietario


@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'dni_cif', 'telefono', 'email', 'activo', 'fecha_alta']
    search_fields = ['nombre', 'apellidos', 'dni_cif', 'email']
    list_filter = ['activo', 'fecha_alta']
