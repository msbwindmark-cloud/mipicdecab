from django.urls import path
from . import views

urlpatterns = [
    path('', views.limpieza_list, name='limpieza_list'),
    path('registrar/', views.registrar_limpieza, name='registrar_limpieza'),
    path('create/', views.limpieza_create, name='limpieza_create'),
    path('<int:pk>/', views.limpieza_detail, name='limpieza_detail'),
    path('<int:pk>/editar/', views.limpieza_update, name='limpieza_update'),
    path('<int:pk>/eliminar/', views.limpieza_delete, name='limpieza_delete'),
    path('programa/', views.programa_create, name='programa_create'),
    path('programa/<int:pk>/', views.programa_detail, name='programa_detail'),
    path('programa/<int:pk>/editar/', views.programa_update, name='programa_update'),
    path('programa/<int:pk>/eliminar/', views.programa_delete, name='programa_delete'),
]
