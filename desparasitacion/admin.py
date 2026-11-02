from django.contrib import admin
from .models import PlanDesparasitacion, RegistroDesparasitacion


class RegistroInline(admin.TabularInline):
    model = RegistroDesparasitacion
    extra = 1


@admin.register(PlanDesparasitacion)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['caballo', 'tipo', 'producto', 'frecuencia', 'ultima_desparasitacion', 'proxima_desparasitacion', 'vencida', 'activo']
    list_filter = ['tipo', 'frecuencia', 'activo']
    search_fields = ['caballo__nombre', 'producto']
    inlines = [RegistroInline]


@admin.register(RegistroDesparasitacion)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ['plan', 'fecha', 'producto_usado', 'dosis', 'coste', 'realizado_por']
    list_filter = ['fecha']
    search_fields = ['plan__caballo__nombre', 'producto_usado']
    date_hierarchy = 'fecha'
