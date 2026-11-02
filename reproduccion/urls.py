from django.urls import path
from . import views

urlpatterns = [
    path('', views.reproduccion_list, name='reproduccion_list'),
    path('crear/', views.reproduccion_create, name='reproduccion_create'),
    path('<int:pk>/', views.reproduccion_detail, name='reproduccion_detail'),
    path('<int:pk>/editar/', views.reproduccion_update, name='reproduccion_update'),
    path('<int:pk>/eliminar/', views.reproduccion_delete, name='reproduccion_delete'),
    path('control/', views.control_create, name='control_create'),
    path('control/<int:pk>/', views.control_detail, name='control_detail'),
    path('control/<int:pk>/editar/', views.control_update, name='control_update'),
    path('control/<int:pk>/eliminar/', views.control_delete, name='control_delete'),
]
