from django.urls import path
from . import views

urlpatterns = [
    path('', views.alimentacion_list, name='alimentacion_list'),
    path('registrar/', views.registrar_alimentacion, name='registrar_alimentacion'),
    path('<int:pk>/', views.registro_detail, name='registro_detail'),
    path('<int:pk>/editar/', views.registro_update, name='registro_update'),
    path('<int:pk>/eliminar/', views.registro_delete, name='registro_delete'),
]
