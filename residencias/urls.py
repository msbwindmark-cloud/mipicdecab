from django.urls import path
from . import views

urlpatterns = [
    path('', views.residencia_list, name='residencia_list'),
    path('crear/', views.residencia_create, name='residencia_create'),
    path('<int:pk>/', views.residencia_detail, name='residencia_detail'),
    path('<int:pk>/editar/', views.residencia_update, name='residencia_update'),
    path('<int:pk>/eliminar/', views.residencia_delete, name='residencia_delete'),
]
