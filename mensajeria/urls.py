from django.urls import path
from . import views

urlpatterns = [
    path('', views.mensajeria_list, name='mensajeria_list'),
    path('enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('mensaje/', views.mensaje_list, name='mensaje_list'),
    path('mensaje/crear/', views.mensaje_create, name='mensaje_create'),
    path('mensaje/<int:pk>/', views.mensaje_detail, name='mensaje_detail'),
    path('mensaje/<int:pk>/editar/', views.mensaje_update, name='mensaje_update'),
    path('mensaje/<int:pk>/eliminar/', views.mensaje_delete, name='mensaje_delete'),
]
