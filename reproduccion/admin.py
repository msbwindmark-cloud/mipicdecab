from django.contrib import admin
from .models import Reproduccion, ControlGestacion


class ControlGestacionInline(admin.TabularInline):
    model = ControlGestacion
    extra = 1


@admin.register(Reproduccion)
class ReproduccionAdmin(admin.ModelAdmin):
    list_display = ['yegua', 'semental', 'tipo', 'fecha_cubricion', 'fecha_parto_estimada', 'fecha_parto_real', 'estado', 'dias_gestacion', 'coste']
    list_filter = ['tipo', 'estado', 'fecha_cubricion']
    search_fields = ['yegua__nombre', 'semental__nombre']
    inlines = [ControlGestacionInline]
    date_hierarchy = 'fecha_cubricion'


@admin.register(ControlGestacion)
class ControlGestacionAdmin(admin.ModelAdmin):
    list_display = ['reproduccion', 'fecha', 'semana_gestacion', 'peso_yegua', 'veterinario']
    list_filter = ['fecha']
    search_fields = ['reproduccion__yegua__nombre']
