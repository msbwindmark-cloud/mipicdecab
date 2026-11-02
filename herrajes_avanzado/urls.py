from django.urls import path
from . import views

urlpatterns = [
    path('', views.herraje_list, name='herraje_list'),
    path('programar/', views.herraje_programar, name='herraje_programar'),
    path('<int:pk>/', views.herraje_detail, name='herraje_detail'),
    path('<int:pk>/editar/', views.herraje_update, name='herraje_update'),
    path('<int:pk>/eliminar/', views.herraje_delete, name='herraje_delete'),
]
