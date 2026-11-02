from django.contrib import admin
from .models import Medicamento, Tratamiento, AdministracionMedicamento


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo']
    list_filter = ['tipo']
    search_fields = ['nombre']


class AdministracionMedicamentoInline(admin.TabularInline):
    model = AdministracionMedicamento
    extra = 1


@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'medicamento', 'dosis', 'frecuencia', 'fecha_inicio', 'fecha_fin', 'estado', 'activo']
    list_filter = ['estado', 'medicamento__tipo', 'fecha_inicio']
    search_fields = ['caballo__nombre', 'medicamento__nombre', 'motivo']
    inlines = [AdministracionMedicamentoInline]
    date_hierarchy = 'fecha_inicio'


@admin.register(AdministracionMedicamento)
class AdministracionMedicamentoAdmin(admin.ModelAdmin):
    list_display = ['tratamiento', 'fecha', 'dado', 'usuario']
    list_filter = ['fecha', 'dado']
    search_fields = ['tratamiento__caballo__nombre']
