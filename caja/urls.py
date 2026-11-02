from django.urls import path
from . import views

urlpatterns = [
    path('', views.caja_list, name='caja_list'),
    path('liquidacion/', views.liquidacion_mensual, name='liquidacion_mensual'),
]
