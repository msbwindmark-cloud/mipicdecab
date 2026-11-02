from django.urls import path
from . import views

urlpatterns = [
    path('', views.consumo_list, name='consumo_list'),
    path('registrar/', views.consumo_create, name='consumo_create'),
    path('<int:pk>/', views.consumo_detail, name='consumo_detail'),
    path('<int:pk>/editar/', views.consumo_update, name='consumo_update'),
    path('<int:pk>/eliminar/', views.consumo_delete, name='consumo_delete'),
]
