from django.contrib import admin
from .models import Concurso, ParticipacionConcurso


class ParticipacionInline(admin.TabularInline):
    model = ParticipacionConcurso
    extra = 1


@admin.register(Concurso)
class ConcursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha', 'lugar', 'disciplina', 'nivel', 'coste_inscripcion', 'premio']
    list_filter = ['disciplina', 'nivel', 'fecha']
    search_fields = ['nombre', 'lugar']
    inlines = [ParticipacionInline]
    date_hierarchy = 'fecha'


@admin.register(ParticipacionConcurso)
class ParticipacionAdmin(admin.ModelAdmin):
    list_display = ['concurso', 'caballo', 'propietario', 'posicion', 'puntuacion', 'clasificado', 'premio_ganado']
    list_filter = ['concurso', 'clasificado']
    search_fields = ['caballo__nombre', 'propietario__nombre']
