from django.urls import path
from . import views

urlpatterns = [
    path('', views.instalaciones, name='instalaciones'),
    path('mapa/', views.mapa_boxes, name='mapa_boxes'),
]
