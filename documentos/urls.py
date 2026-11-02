from django.urls import path
from . import views

urlpatterns = [
    path('', views.documento_list, name='documento_list'),
    path('subir/', views.documento_subir, name='documento_subir'),
    path('create/', views.documento_create, name='documento_create'),
    path('<int:pk>/', views.documento_detail, name='documento_detail'),
    path('<int:pk>/editar/', views.documento_update, name='documento_update'),
    path('<int:pk>/eliminar/', views.documento_delete, name='documento_delete'),
]
