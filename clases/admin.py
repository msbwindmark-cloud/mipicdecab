from django.contrib import admin
from .models import Instructor, Clase, InscripcionClase


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellidos', 'telefono', 'email', 'activo']
    search_fields = ['nombre', 'apellidos']
    list_filter = ['activo']


class InscripcionClaseInline(admin.TabularInline):
    model = InscripcionClase
    extra = 1


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora_inicio', 'hora_fin', 'instructor', 'pista', 'nivel', 'plazas', 'precio']
    list_filter = ['fecha', 'nivel', 'instructor']
    search_fields = ['instructor__nombre']
    inlines = [InscripcionClaseInline]


@admin.register(InscripcionClase)
class InscripcionClaseAdmin(admin.ModelAdmin):
    list_display = ['clase', 'alumno', 'caballo', 'estado', 'fecha_inscripcion']
    list_filter = ['estado', 'fecha_inscripcion']
    search_fields = ['alumno__nombre', 'alumno__apellidos']
