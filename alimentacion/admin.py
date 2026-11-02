from django.contrib import admin
from .models import PlanAlimentacion, RegistroAlimentacion


@admin.register(PlanAlimentacion)
class PlanAlimentacionAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'momento', 'alimento', 'cantidad', 'unidad', 'activo']
    list_filter = ['momento', 'activo']
    search_fields = ['caballo__nombre', 'alimento']


@admin.register(RegistroAlimentacion)
class RegistroAlimentacionAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'fecha', 'momento', 'dado', 'usuario']
    list_filter = ['fecha', 'momento', 'dado']
    search_fields = ['caballo__nombre']
    date_hierarchy = 'fecha'
