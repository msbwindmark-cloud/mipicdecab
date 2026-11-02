from django.urls import path
from . import views

urlpatterns = [
    path('<int:caballo_id>/', views.seguimiento_list, name='seguimiento_list'),
    path('<int:caballo_id>/nuevo/', views.seguimiento_create, name='seguimiento_create'),
    path('eliminar/<int:pk>/', views.seguimiento_delete, name='seguimiento_delete'),
]
