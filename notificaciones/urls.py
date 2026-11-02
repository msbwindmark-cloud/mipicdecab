from django.urls import path
from . import views

urlpatterns = [
    path('', views.notificacion_list, name='notificacion_list'),
    path('crear/', views.notificacion_create, name='notificacion_create'),
    path('<int:pk>/', views.notificacion_detail, name='notificacion_detail'),
    path('<int:pk>/editar/', views.notificacion_update, name='notificacion_update'),
    path('<int:pk>/eliminar/', views.notificacion_delete, name='notificacion_delete'),
]
