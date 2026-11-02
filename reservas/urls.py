from django.urls import path
from . import views

urlpatterns = [
    path('', views.reserva_list, name='reserva_list'),
    path('crear/', views.reserva_create, name='reserva_create'),
    path('<int:pk>/', views.reserva_detail, name='reserva_detail'),
    path('<int:pk>/editar/', views.reserva_update, name='reserva_update'),
    path('<int:pk>/eliminar/', views.reserva_delete, name='reserva_delete'),
]
