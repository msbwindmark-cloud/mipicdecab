from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.dashboard, name='dashboard'),
    path('landing/', views.landing, name='landing'),
    path('core/', include('core.urls')),
    path('caballos/', include('caballos.urls')),
    path('propietarios/', include('propietarios.urls')),
    path('facturacion/', include('facturacion.urls')),
    path('instalaciones/', include('instalaciones.urls')),
    path('calendario/', include('calendario.urls')),
    path('clases/', include('clases.urls')),
    path('inventario/', include('inventario.urls')),
    path('caja/', include('caja.urls')),
    path('tareas/', include('tareas.urls')),
    path('eventos/', include('eventos.urls')),
    path('reportes/', include('reportes.urls')),
    path('alimentacion/', include('alimentacion.urls')),
    path('medicacion/', include('medicacion.urls')),
    path('bitacora/', include('bitacora.urls')),
    path('empleados/', include('empleados.urls')),
    path('limpieza/', include('limpieza.urls')),
    path('reservas/', include('reservas.urls')),
    path('seguros/', include('seguros.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('gastos/', include('gastos_caballo.urls')),
    path('documentos/', include('documentos.urls')),
    path('visitas-vet/', include('visitas_vet.urls')),
    path('transporte/', include('transporte.urls')),
    path('reproduccion/', include('reproduccion.urls')),
    path('mantenimiento/', include('mantenimiento.urls')),
    path('fidelizacion/', include('fidelizacion.urls')),
    path('mensajeria/', include('mensajeria.urls')),
    path('ventas/', include('ventas.urls')),
    path('concursos/', include('concursos.urls')),
    path('desparasitacion/', include('desparasitacion.urls')),
    path('facturacion-recurrente/', include('facturacion_recurrente.urls')),
    path('cursos/', include('cursos.urls')),
    path('notificaciones/', include('notificaciones.urls')),
    path('reservas-online/', include('reservas_online.urls')),
    path('herrajes-avanzado/', include('herrajes_avanzado.urls')),
    path('encuestas/', include('encuestas.urls')),
    path('consumos/', include('consumos.urls')),
    path('residencias/', include('residencias.urls')),
    path('entrenamientos/', include('entrenamientos.urls')),
    path('logros/', include('logros.urls')),
    path('seguimiento/', include('seguimiento_fisico.urls')),
    path('mapa/', include('mapa_picadero.urls')),
    path('ranking/', include('ranking.urls')),
    path('timeline/', include('timeline_caballo.urls')),
    path('chat/', include('chat_flotante.urls')),
    path('portal/', include('portal_propietario.urls')),
    path('equest-ai/', include('equest_ai.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
