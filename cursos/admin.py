from django.contrib import admin
from .models import Curso, InscripcionCurso


class InscripcionInline(admin.TabularInline):
    model = InscripcionCurso
    extra = 1


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nivel', 'instructor', 'fecha_inicio', 'fecha_fin', 'plazas', 'plazas_disponibles', 'precio', 'activo']
    list_filter = ['nivel', 'activo', 'fecha_inicio']
    search_fields = ['nombre', 'instructor']
    inlines = [InscripcionInline]
    date_hierarchy = 'fecha_inicio'


@admin.register(InscripcionCurso)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['curso', 'alumno', 'caballo', 'estado', 'asistencia', 'porcentaje_asistencia', 'fecha_inscripcion']
    list_filter = ['estado', 'fecha_inscripcion']
    search_fields = ['alumno__nombre', 'curso__nombre']
