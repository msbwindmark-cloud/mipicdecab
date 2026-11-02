from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapa_interactivo, name='mapa_picadero'),
    path('zona/<int:pk>/', views.zona_detalle, name='zona_detalle'),
]
