from django.urls import path
from . import views

urlpatterns = [
    path('', views.venta_list, name='venta_list'),
    path('publicar/', views.venta_publicar, name='venta_publicar'),
    path('create/', views.venta_create, name='venta_create'),
    path('<int:pk>/', views.venta_detail, name='venta_detail'),
    path('<int:pk>/editar/', views.venta_update, name='venta_update'),
    path('<int:pk>/eliminar/', views.venta_delete, name='venta_delete'),
]
