from django.urls import path
from . import views

urlpatterns = [
    path('', views.seguro_list, name='seguro_list'),
    path('crear/', views.seguro_create, name='seguro_create'),
    path('<int:pk>/', views.seguro_detail, name='seguro_detail'),
    path('<int:pk>/editar/', views.seguro_update, name='seguro_update'),
    path('<int:pk>/eliminar/', views.seguro_delete, name='seguro_delete'),
]
