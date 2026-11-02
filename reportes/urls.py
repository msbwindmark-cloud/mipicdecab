from django.urls import path
from . import views

urlpatterns = [
    path('', views.reporte_mensual, name='reporte_mensual'),
    path('informe-semanal/', views.informe_semanal, name='informe_semanal'),
    path('simulador/', views.simulador, name='simulador'),
]
