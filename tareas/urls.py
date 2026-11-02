from django.urls import path
from . import views

urlpatterns = [
    path('', views.tarea_list, name='tarea_list'),
    path('crear/', views.tarea_create, name='tarea_create'),
    path('<int:pk>/completar/', views.tarea_completar, name='tarea_completar'),
    path('<int:pk>/', views.tarea_detail, name='tarea_detail'),
    path('<int:pk>/editar/', views.tarea_update, name='tarea_update'),
    path('<int:pk>/eliminar/', views.tarea_delete, name='tarea_delete'),
]
