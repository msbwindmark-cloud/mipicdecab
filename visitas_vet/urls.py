from django.urls import path
from . import views

urlpatterns = [
    path('', views.visita_list, name='visita_list'),
    path('programar/', views.visita_programar, name='visita_programar'),
    path('<int:pk>/', views.visita_detail, name='visita_detail'),
    path('<int:pk>/editar/', views.visita_update, name='visita_update'),
    path('<int:pk>/eliminar/', views.visita_delete, name='visita_delete'),
]
