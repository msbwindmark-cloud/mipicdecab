from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendario, name='calendario'),
    path('eventos/', views.eventos_json, name='eventos_json'),
]
