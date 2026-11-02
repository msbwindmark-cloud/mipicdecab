from django.urls import path
from . import views

urlpatterns = [
    path('', views.gasto_list, name='gasto_list'),
    path('crear/', views.gasto_create, name='gasto_create'),
    path('<int:pk>/', views.gasto_detail, name='gasto_detail'),
    path('<int:pk>/editar/', views.gasto_update, name='gasto_update'),
    path('<int:pk>/eliminar/', views.gasto_delete, name='gasto_delete'),
]
