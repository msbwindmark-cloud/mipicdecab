from django.contrib import admin
from .models import Empleado, HorarioEmpleado, Fichaje


class HorarioEmpleadoInline(admin.TabularInline):
    model = HorarioEmpleado
    extra = 1


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'puesto', 'telefono', 'fecha_contratacion', 'activo']
    list_filter = ['puesto', 'activo']
    search_fields = ['nombre', 'apellidos', 'telefono']
    inlines = [HorarioEmpleadoInline]


@admin.register(Fichaje)
class FichajeAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'tipo', 'fecha_hora', 'notas']
    list_filter = ['tipo', 'fecha_hora']
    search_fields = ['empleado__nombre', 'empleado__apellidos']
    date_hierarchy = 'fecha_hora'
