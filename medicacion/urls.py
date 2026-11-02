from django.urls import path
from . import views

urlpatterns = [
    path('', views.medicacion_list, name='medicacion_list'),
    path('tratamiento/', views.tratamiento_create, name='tratamiento_create'),
    path('tratamiento/<int:pk>/', views.tratamiento_detail, name='tratamiento_detail'),
    path('tratamiento/<int:pk>/editar/', views.tratamiento_update, name='tratamiento_update'),
    path('tratamiento/<int:pk>/eliminar/', views.tratamiento_delete, name='tratamiento_delete'),
]
