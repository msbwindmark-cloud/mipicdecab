from django.urls import path
from . import views

urlpatterns = [
    path('', views.bitacora_list, name='bitacora_list'),
    path('crear/', views.bitacora_create, name='bitacora_create'),
    path('<int:pk>/', views.bitacora_detail, name='bitacora_detail'),
    path('<int:pk>/editar/', views.bitacora_update, name='bitacora_update'),
    path('<int:pk>/eliminar/', views.bitacora_delete, name='bitacora_delete'),
]
