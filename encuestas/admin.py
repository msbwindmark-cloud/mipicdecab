from django.contrib import admin
from .models import Encuesta, Pregunta, Respuesta, RespuestaPregunta


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1


@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'fecha_inicio', 'fecha_fin', 'activa', 'total_respuestas']
    list_filter = ['tipo', 'activa', 'fecha_inicio']
    search_fields = ['titulo', 'descripcion']
    inlines = [PreguntaInline]
    date_hierarchy = 'fecha_inicio'


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ['encuesta', 'texto', 'tipo', 'orden', 'obligatoria']
    list_filter = ['tipo', 'obligatoria']
    search_fields = ['texto']


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ['encuesta', 'propietario', 'fecha']
    list_filter = ['fecha']
    search_fields = ['propietario__nombre', 'encuesta__titulo']
    date_hierarchy = 'fecha'


@admin.register(RespuestaPregunta)
class RespuestaPreguntaAdmin(admin.ModelAdmin):
    list_display = ['respuesta', 'pregunta', 'respuesta_texto', 'respuesta_numero']
    search_fields = ['pregunta__texto']
