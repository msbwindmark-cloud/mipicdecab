from django.urls import path
from . import views

urlpatterns = [
    path('', views.reserva_online_list, name='reserva_online_list'),
    path('crear/', views.reserva_online_create, name='reserva_online_create'),
    path('<int:pk>/', views.reserva_online_detail, name='reserva_online_detail'),
    path('<int:pk>/editar/', views.reserva_online_update, name='reserva_online_update'),
    path('<int:pk>/eliminar/', views.reserva_online_delete, name='reserva_online_delete'),
]
