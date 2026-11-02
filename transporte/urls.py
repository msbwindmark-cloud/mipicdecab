from django.urls import path
from . import views

urlpatterns = [
    path('', views.transporte_list, name='transporte_list'),
    path('programar/', views.transporte_programar, name='transporte_programar'),
    path('create/', views.transporte_create, name='transporte_create'),
    path('<int:pk>/', views.transporte_detail, name='transporte_detail'),
    path('<int:pk>/editar/', views.transporte_update, name='transporte_update'),
    path('<int:pk>/eliminar/', views.transporte_delete, name='transporte_delete'),
]
