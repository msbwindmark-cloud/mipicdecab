from django.urls import path
from . import views

urlpatterns = [
    path('', views.mantenimiento_list, name='mantenimiento_list'),
    path('crear/', views.mantenimiento_create, name='mantenimiento_create'),
    path('<int:pk>/', views.mantenimiento_detail, name='mantenimiento_detail'),
    path('<int:pk>/editar/', views.mantenimiento_update, name='mantenimiento_update'),
    path('<int:pk>/eliminar/', views.mantenimiento_delete, name='mantenimiento_delete'),
]
