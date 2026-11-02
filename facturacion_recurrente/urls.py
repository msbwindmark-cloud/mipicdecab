from django.urls import path
from . import views

urlpatterns = [
    path('', views.recurrente_list, name='recurrente_list'),
    path('create/', views.recurrente_create, name='recurrente_create'),
    path('<int:pk>/', views.recurrente_detail, name='recurrente_detail'),
    path('<int:pk>/editar/', views.recurrente_update, name='recurrente_update'),
    path('<int:pk>/eliminar/', views.recurrente_delete, name='recurrente_delete'),
]
