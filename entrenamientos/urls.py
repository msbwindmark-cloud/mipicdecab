from django.urls import path
from . import views

urlpatterns = [
    path('', views.entrenamiento_list, name='entrenamiento_list'),
    path('crear/', views.entrenamiento_create, name='entrenamiento_create'),
    path('<int:pk>/', views.entrenamiento_detail, name='entrenamiento_detail'),
    path('<int:pk>/editar/', views.entrenamiento_update, name='entrenamiento_update'),
    path('<int:pk>/eliminar/', views.entrenamiento_delete, name='entrenamiento_delete'),
]
