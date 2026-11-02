from django.contrib import admin
from .models import Evento, ResultadoEvento


class ResultadoEventoInline(admin.TabularInline):
    model = ResultadoEvento
    extra = 1


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo', 'fecha', 'lugar']
    list_filter = ['tipo', 'fecha']
    search_fields = ['nombre', 'lugar']
    inlines = [ResultadoEventoInline]
    filter_horizontal = ['caballos', 'propietarios']


@admin.register(ResultadoEvento)
class ResultadoEventoAdmin(admin.ModelAdmin):
    list_display = ['evento', 'caballo', 'posicion', 'puntuacion']
    list_filter = ['evento']
    search_fields = ['caballo__nombre']
